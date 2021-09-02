import pytest
from web_report.racing_report import *
from web_report.racing_report.common import *
from .data import *


@pytest.fixture
def driver_vettel():
    # full class instance
    vettel = Driver()
    vettel.update_data('SVF', 'Sebastian Vettel', 'FERRARI',
                       '2018-05-24_12:02:58.917', '2018-05-24_1:04:03.332')
    vettel.index = 5
    return vettel


@pytest.fixture
def driver_hamilton():
    # full class instance
    hamilton = Driver()
    hamilton.update_data('LHM', 'Lewis Hamilton', 'MERCEDES',
                         '2018-05-24_12:18:20.125', '2018-05-24_1:11:32.585')
    hamilton.index = 1
    return hamilton


@pytest.fixture
def driver_ricardo():
    # lap time fields aren't specified
    ricardo = Driver()
    ricardo.update_data('DRR', 'Daniel Ricciardo', 'RED BULL RACING TAG HEUER')
    return ricardo


@pytest.fixture
def dir_with_all_files(tmp_path):
    directory = tmp_path / 'tmp_data'
    directory.mkdir()
    (directory / 'abbreviations.txt').write_text(ABBREVIATIONS, 'utf-8')
    (directory / 'start.log').write_text(START, 'utf-8')
    (directory / 'end.log').write_text(END, 'utf-8')
    return directory


@pytest.fixture
def report_instance(dir_with_all_files):
    return Report(dir_with_all_files)
