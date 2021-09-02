from .driver import Driver
from .common import *
from pathlib import Path
from collections import defaultdict
from typing import Literal
import re


class Report:
    """
    A class used to build and represent racing report.
    On initialization gets and normalizes data from files, builds a report.
    It can be accessed it via `drivers` property.
    `ascending` property can be set to bool to define order in wich `drivers` is sorted

    Properties:

    drivers : :class:`list` [:class:`Driver`]
        Sorted list of drivers in order corresponding to `ascending` property
    ascending : :class:`bool`
        defines order of displaying drivers either ascending if True or descending if False

    Public methods:

    check_dir(directory) -> :class:`Path` : static
        Check if given directory is valid for report building.
        Raise certain exception if check is failed, or return corresponding :class:`Path` object
    find_driver(value: :class:`str`, key: :class:`Literal` ['name', 'code']) -> :class:`Driver`:
        Find :class:`Driver` instance by key value
    """

    # DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER
    ABBR_RE = re.compile(r'[A-Z]{3}_[^_\n]+_[^_\n]+\b', re.UNICODE)
    # SVF2018-05-24_12:02:58.917
    TIME_RE = re.compile(r'[A-Z]{3}\d{4}-\d\d-\d\d_\d\d?:\d\d:\d\d.\d{3,6}', re.UNICODE)

    @property
    def drivers(self):
        """
        List of :class:`Driver` sorted in ascending or descending order, main data
        """
        return self._sorted_drivers_asc if self.ascending else self._sorted_drivers_desc

    @property
    def ascending(self):
        return self._ascending

    @ascending.setter
    def ascending(self, value: bool):
        self._ascending = value

    def __init__(self, directory, ascending=True):
        """
        :param Path|str directory: path to a directory with datafiles to build an instance
        :param bool ascending: drivers will be displayed in order either ascending or descending if False
        """
        self._name_max_len = 0
        self._car_max_len = 0
        self._sorted_drivers_asc = []
        self._sorted_drivers_desc = []
        self._drivers_code_map = {}
        self._drivers_name_map = {}
        self._ascending = ascending
        self._load_drivers(directory)

    def _load_drivers(self, directory):
        """
        Load data from 3 files from given directory\n
        :param directory: should contain files abbreviations.txt, start.log, end.log.
        """
        directory = self.check_dir(directory)
        abbreviation_list = self._extract_data(directory / "abbreviations.txt", 'a')
        start_list = self._extract_data(directory / "start.log", 't')
        end_list = self._extract_data(directory / "end.log", 't')
        # using dict with codes(abbreviations) as keys
        # because all data strings start with these codes
        drivers_dict = defaultdict(Driver)
        self._name_max_len = 0
        self._car_max_len = 0
        for item in abbreviation_list:
            items = item.split('_')
            # find longest driver's full_name an car for table alignment
            if len(items[1]) > self._name_max_len:
                self._name_max_len = len(items[1])
            if len(items[2]) > self._car_max_len:
                self._car_max_len = len(items[2])
            drivers_dict[items[0]].update_data(*items)
        for item in start_list:
            drivers_dict[item[:3]].update_data(start_time=item[3:])
        for item in end_list:
            drivers_dict[item[:3]].update_data(end_time=item[3:])
        drivers_list = [driver for driver in drivers_dict.values() if driver.lap_time]
        if len(drivers_list) < len(drivers_dict):
            print(f'{Styles.WARNING}Warning: dataset seems to be inconsistent{Styles.RESET}')
        self._sort_drivers(drivers_list)
        # for faster performance
        self._sorted_drivers_asc = drivers_list
        self._sorted_drivers_desc = list(reversed(drivers_list))
        self._drivers_code_map = {driver.code: driver for driver in self._sorted_drivers_asc}
        self._drivers_name_map = {driver.full_name.casefold(): driver for driver in self._sorted_drivers_asc}

    @classmethod
    def _extract_data(cls, file, pattern='a') -> list[str]:
        """
        Read given file, search for matching strings with regex pattern\n
        :param Path file: path to datafile
        :param str pattern: 't' for time pattern, 'a' for abbreviation pattern
        :return: list of matching strings
        :raise ValueError: if pattern is invalid
        """
        if pattern not in ['a', 't']:
            raise ValueError(f"Invalid pattern: '{pattern}'")
        pattern = cls.TIME_RE if pattern == 't' else cls.ABBR_RE
        with file.open('r', encoding='utf-8') as file:
            content = pattern.findall(file.read())
        return content

    @staticmethod
    def _sort_drivers(drivers_list: list[Driver]):
        """
        Sort drivers list and set corresponding indexes for each driver\n
        :return: sorted given list
        """
        drivers_list.sort()
        for index in range(len(drivers_list)):
            drivers_list[index].index = index + 1

    def __str__(self):
        """
        Represent report as a table of drivers statistics, sorted by lap time
        :return: statistics table
        """
        name_width = self._name_max_len + 2  # for prettier table look
        car_width = self._car_max_len + 2
        row_list = []
        sep_index = 15 if self.ascending else 16
        for driver in self.drivers:
            row_list.append(driver.as_table_row(name_width, car_width))
            if driver.index == sep_index:
                row_list.append('_' * len(row_list[0]))
        header = Driver.get_header(name_width, car_width)
        return header + '\n' + '\n'.join(row_list)

    @staticmethod
    def check_dir(directory) -> Path:
        """
        Check if given directory is valid and contains files: `abbreviations.txt`, `start.log`, `end.log`.
        Raise certain exception if check is failed, or return corresponding :class:`Path` object\n
        :raise FileNotFoundError: if directory doesn't exist
        :raise IncompleteDataError: if directory doesn't contain abbreviations.txt, start.log and end.log
        :param Path|str directory: a directory path
        :return: given directory as Path
        """
        directory = Path(directory)
        if not directory.is_dir():
            raise FileNotFoundError(f'There is no such directory "{directory}"')
        for file_name in ['abbreviations.txt', 'start.log', 'end.log']:
            if not (directory / file_name).is_file():
                raise IncompleteDataError(f"File {file_name} is missing.")
        return directory

    def find_driver(self, value: str, key: Literal['name', 'code']) -> Driver:
        """
        Find :class:`Driver` instance by key value\n
        :param str value: value for search
        :param str key: key for search
        :return: corresponding Driver instance
        :raise SearchError: if search failed
        """
        if key == 'name':
            result = self._drivers_name_map.get(value.casefold())
        elif key == 'code':
            result = self._drivers_code_map.get(value)
        else:
            result = None
        if result is None:
            raise SearchError('Driver is not found.')
        else:
            return result
