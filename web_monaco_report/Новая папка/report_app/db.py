from report_app.driver import Driver
from peewee import *
from flask import current_app
from pathlib import Path, PurePath
from datetime import datetime
from collections import defaultdict
import re


class connection:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = current_app.config['DATABASE']
        self.db = SqliteDatabase(db_path)
        self.db.bind([Driver])

    def __enter__(self):
        self.db.connect()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()


def init_db():
    """Clear existing data and create new tables."""
    with connection() as db:
        db.drop_tables([Driver])
        db.create_tables([Driver])
        load_drivers_to_db(Path(current_app.static_folder) / 'report_data', db)


# Example: DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER
ABBR_RE = re.compile(r'[A-Z]{3}_[^_\n]+_[^_\n]+\b', re.UNICODE)
# Example: SVF2018-05-24_12:02:58.917
TIME_RE = re.compile(r'[A-Z]{3}\d{4}-\d\d-\d\d_\d\d?:\d\d:\d\d.\d{3,6}', re.UNICODE)


def load_drivers_to_db(data_dir, db):
    """
    Load data into Driver table from 3 files from given directory\n
    :param PurePath|str data_dir: directory to load from, should contain files abbreviations.txt, start.log, end.log.
    :param db: database
    """
    data_dir = Path(data_dir)
    if not data_dir.is_dir():
        raise FileNotFoundError(f'There is no such data_dir "{data_dir}"')
    for file_name in ['abbreviations.txt', 'start.log', 'end.log']:
        if not (data_dir / file_name).is_file():
            raise RuntimeError(f"File {file_name} is missing.")
    with (data_dir / "abbreviations.txt").open('r', encoding='utf-8') as file:
        abbreviations = ABBR_RE.findall(file.read())
    with (data_dir / "start.log").open('r', encoding='utf-8') as file:
        start = TIME_RE.findall(file.read())
    with (data_dir / "end.log").open('r', encoding='utf-8') as file:
        end = TIME_RE.findall(file.read())
    rows_dict = defaultdict(list)
    for item in abbreviations:
        row = item.split('_')
        rows_dict[row[0]] = row
    for item in start:
        time = datetime.strptime(item[3:], '%Y-%m-%d_%I:%M:%S.%f')
        rows_dict[item[:3]].append(time)
    for item in end:
        code = item[:3]
        time = datetime.strptime(item[3:], '%Y-%m-%d_%I:%M:%S.%f')
        rows_dict[code].append(time)
        rows_dict[code].append(Driver.calc_time(time, rows_dict[code][3]))
    rows_list = [row for row in rows_dict.values() if len(row) == 6]
    if len(rows_list) < len(rows_dict):
        print(f'Warning: dataset seems to be inconsistent')
    rows_list.sort(key=lambda d: d[5])
    fields = [Driver.code, Driver.full_name, Driver.car, Driver.lap_start, Driver.lap_end, Driver.lap_time]
    with db.atomic():
        Driver.insert_many(rows_list, fields).on_conflict_replace().execute()
