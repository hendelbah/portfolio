from datetime import datetime, timedelta


class Driver:
    """
    A class used to store and represent driver's racing statistics.

    It has such properties:

    * `code`: :class:`str` - driver's unique abbreviation code of 3 letters
    * `full_name`: :class:`str` - driver's first and last name
    * `car`: :class:`str` - name of driver's car
    * `lap_start`: :class:`datetime` - start time of best driver's lap
    * `lap_end`: :class:`datetime` - end time of best driver's lap
    * `lap_time`: :class:`timedelta` - Best driver's lap time, None if lap start or end wasn't specified
    """

    @property
    def code(self):
        """
        Driver's unique abbreviation code of 3 letters
        """
        return self._code

    @property
    def full_name(self):
        """
        Driver's first and last name
        """
        return self._full_name

    @property
    def car(self):
        """
        Name of driver's car
        """
        return self._car

    @property
    def lap_start(self):
        """
        Start time of best driver's lap, empty string if not initialized\n
        """
        return self._lap_start.isoformat(" ", "milliseconds") if self._lap_start else ""

    @property
    def lap_end(self):
        """
        End time of best driver's lap, empty string if not initialized\n
        """
        return self._lap_end.isoformat(" ", "milliseconds") if self._lap_end else ""

    @property
    def lap_time(self):
        """
        Best driver's lap time, empty string if lap start or end wasn't specified\n
        """
        # cut last 3 digits of microseconds to format properly
        return f"{self._lap_end - self._lap_start}"[:-3] if self._lap_end and self._lap_start else ""

    @property
    def index(self):
        """
        Drivers index in the statistics table
        """
        return self._index

    @index.setter
    def index(self, value: int):
        self._index = value

    def __init__(self):
        self._code = ''
        self._full_name = ''
        self._car = ''
        self._lap_start = None
        self._lap_end = None
        self._index = 0

    def __lt__(self, other):
        assert isinstance(other, self.__class__)
        return self.lap_time < other.lap_time

    def __eq__(self, other):
        assert isinstance(other, self.__class__)
        attributes = ['code', 'full_name', 'car', 'lap_start', 'lap_end', 'lap_time', 'index']
        return all([getattr(self, attr) == getattr(other, attr) for attr in attributes])

    def __str__(self):
        """
        Represent driver's own statistics
        """
        return (f'{self.index}. {self.full_name} - {self.car}\n'
                f'Best lap time: {self.lap_time}\n'
                f'Lap start : {self.lap_start}\n'
                f'Lap end   : {self.lap_end}')

    @classmethod
    def get_header(cls, name_column_width: int, car_column_width: int) -> str:
        """
        Get header for table representation via :meth:`as_table_row`\n
        :param name_column_width: width of 'full name' column
        :param car_column_width: width of 'car' column
        :return: header
        """
        return f"{'№':^3}|{'Full Name':^{name_column_width}}|{'Car':^{car_column_width}}|{'Lap Time':^12}"

    def as_table_row(self, name_width: int, car_width: int) -> str:
        """
        Represent self as a table row in a string format.\n
        There is  4 columns: `index`, `full_name`, `car`, `lap time`.\n
        For example:   '  1| Sebastian Vettel | FERRARI | 1:01:04.415'\n
        :param name_width: width of 'full name' column
        :param car_width: width of 'car' column
        :return: formatted string containing listed 4 columns
        """
        return (f"{self.index:>3}|{self.full_name:^{name_width}.{name_width}}|"
                f"{self.car:^{car_width}.{car_width}}|{self.lap_time:>12}")

    def update_data(self, code='', full_name='', car='', start_time='', end_time=''):
        """
        Update properties with given values\n
        :param str|None code: unique abbreviation code of 3 letters
        :param str|None full_name: first and last name
        :param str|None car: car name
        :param str|None start_time: datetime in string format %Y-%m-%d_%I:%M:%S.%f
        :param str|None end_time: so as start_time
        :raise ValueError: if code doesn't consist of 3 letters
        """
        if code:
            if len(code) != 3:
                raise ValueError("only 3 lettered code is allowed")
            else:
                self._code = code
        if full_name:
            self._full_name = full_name
        if car:
            self._car = car
        if start_time:
            self._lap_start = datetime.strptime(start_time, '%Y-%m-%d_%I:%M:%S.%f')
        if end_time:
            self._lap_end = datetime.strptime(end_time, '%Y-%m-%d_%I:%M:%S.%f')
