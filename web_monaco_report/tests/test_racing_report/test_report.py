from .fixtures import *


class TestedReport:

    def test_init(self, report_instance):
        assert report_instance.ascending
        assert len(report_instance.drivers) == 19
        assert report_instance.drivers[0].as_table_row(15, 10) == '  1|Lewis Hamilton | MERCEDES | 0:53:12.460'
        assert report_instance.drivers[5].as_table_row(15, 10) == '  6|Valtteri Bottas| MERCEDES | 1:01:12.434'
        assert str(report_instance.drivers[7]) == ('8. Kimi Räikkönen - FERRARI\n'
                                                   'Best lap time: 1:01:12.639\n'
                                                   'Lap start : 2018-05-24 00:03:01.250\n'
                                                   'Lap end   : 2018-05-24 01:04:13.889')

    def test_not_complete_data(self, dir_with_all_files, capsys):
        (dir_with_all_files / 'start.log').write_text(START[:300])
        report = Report(dir_with_all_files)
        assert len(report.drivers) == 11
        captured = capsys.readouterr()
        assert captured.out == f"{Styles.WARNING}Warning: dataset seems to be inconsistent{Styles.RESET}\n"

    def test_str(self, report_instance):
        assert str(report_instance) == HEADER + RESULT
        report_instance.ascending = False
        assert str(report_instance) == HEADER + '\n'.join(reversed(RESULT.splitlines()))

    def test_extract_data(self, dir_with_all_files):
        with pytest.raises(ValueError) as exc_info:
            Report._extract_data(dir_with_all_files, "zxc")
        assert exc_info.value.args[0] == "Invalid pattern: 'zxc'"
        abbr_file = dir_with_all_files / "abbreviations.txt"
        assert Report._extract_data(abbr_file) == ABBREVIATIONS.splitlines()
        start_file = dir_with_all_files / "start.log"
        assert Report._extract_data(start_file, 't') == START.splitlines()

    def test_find_driver(self, driver_vettel, driver_hamilton, report_instance):
        assert driver_vettel == report_instance.find_driver('sebastian vettel', "name")
        assert driver_vettel == report_instance.find_driver('seBastIan vEtTEL', "name")
        assert driver_hamilton == report_instance.find_driver('Lewis Hamilton', "name")
        assert driver_vettel == report_instance.find_driver('SVF', "code")
        assert driver_hamilton == report_instance.find_driver('LHM', "code")

    driver_not_found_cases = [
        ('oleg', 'name'),
        ('ZXC', 'code'),
        ('LHM', 'foo'),
    ]

    @pytest.mark.parametrize('value, key', driver_not_found_cases)
    def test_driver_nof_found(self, report_instance, value, key):
        with pytest.raises(SearchError) as exc_info:
            report_instance.find_driver(value, key)
        assert exc_info.value.args[0] == "Driver is not found."

    def test_invalid_dir(self):
        with pytest.raises(TypeError) as exc_info:
            # noinspection PyTypeChecker,PyUnusedLocal
            r = Report([1])
        assert exc_info.value.args[0] == "expected str, bytes or os.PathLike object, not list"

    def test_dir_doesnt_exist(self, dir_with_all_files):
        with pytest.raises(FileNotFoundError):
            # noinspection PyUnusedLocal
            r = Report(dir_with_all_files / 'new_dir')

    def test_not_enough_files(self, dir_with_all_files):
        (dir_with_all_files / 'end.log').unlink()
        with pytest.raises(IncompleteDataError) as exc_info:
            # noinspection PyUnusedLocal
            r = Report(dir_with_all_files)
        assert exc_info.value.args[0] == 'File end.log is missing.'
