from .fixtures import *
from datetime import datetime, timedelta


class TestedDriver:
    attributes = [
        ('code', 'SVF'),
        ('full_name', 'Sebastian Vettel'),
        ('car', 'FERRARI'),
        ('lap_start', '2018-05-24 00:02:58.917'),
        ('lap_end', '2018-05-24 01:04:03.332'),
        ('lap_time', '1:01:04.415'),
        ('index', 5),
        ('_lap_start', datetime(2018, 5, 24, 0, 2, 58, 917000)),
        ('_lap_end', datetime(2018, 5, 24, 1, 4, 3, 332000)),
    ]

    @pytest.mark.parametrize('attribute, value', attributes)
    def test_properties(self, driver_vettel, attribute, value):
        assert getattr(driver_vettel, attribute) == value

    def test_incomplete_instance(self, driver_ricardo):
        assert driver_ricardo.lap_time == ''
        driver_ricardo.update_data(start_time='2018-05-24_12:14:12.054',
                                   end_time='2018-05-24_1:11:24.067')
        assert driver_ricardo.lap_start == '2018-05-24 00:14:12.054'
        assert driver_ricardo.lap_end == '2018-05-24 01:11:24.067'
        assert driver_ricardo.lap_time == '0:57:12.013'
        assert driver_ricardo.index == 0

    as_table_row_cases = [
        ([30, 20], '  5|       Sebastian Vettel       |      FERRARI       | 1:01:04.415'),
        ([5, 5], '  5|Sebas|FERRA| 1:01:04.415'),
        ([7, 10], '  5|Sebasti| FERRARI  | 1:01:04.415'),
    ]

    @pytest.mark.parametrize("args, result_string", as_table_row_cases)
    def test_as_table_row(self, driver_vettel, args, result_string):
        assert driver_vettel.as_table_row(*args) == result_string

    def test_get_header(self):
        assert Driver.get_header(19, 27) + '\n' == HEADER

    def test_comparison(self, driver_vettel, driver_hamilton):
        assert driver_vettel == driver_vettel
        assert driver_hamilton != driver_vettel
        assert driver_hamilton < driver_vettel
        with pytest.raises(AssertionError):
            # noinspection PyUnusedLocal
            less_then_five = driver_hamilton < 5
        with pytest.raises(AssertionError):
            # noinspection PyUnusedLocal
            equals_six = driver_vettel == 6

    def test_str(self, driver_hamilton):
        assert str(driver_hamilton) == LEWIS

    def test_update_data_raises(self, driver_vettel):
        with pytest.raises(ValueError) as exc_info:
            driver_vettel.update_data(code='QWERTY')
        assert exc_info.value.args[0] == "only 3 lettered code is allowed"
