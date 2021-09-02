import pytest
from src.unique_characters.util import find_unique_characters
from src.unique_characters.__main__ import main
import sys


class TestingUniqueCharacters:
    cases = [("asd", ['a', 's', 'd']),
             ("adsrgfdzfgdhe", ['a', 's', 'r', 'z', 'h', 'e']),
             ("aaaaaa", []),
             ("", [])]

    @pytest.mark.parametrize("input_string, result", cases)
    def test_value(self, input_string, result):
        assert find_unique_characters(input_string) == result

    @pytest.mark.parametrize("argument", [5, [3], True])
    def test_raises_type_error(self, argument):
        with pytest.raises(TypeError):
            find_unique_characters(argument)


class TestingCLI:
    cases = [('asd', '"asd" => 3\na, s, d are present once.\n'),
             ('aassd', '"aassd" => 1\nd is present once.\n'),
             ('aaasdfff', '"aaasdfff" => 2\ns, d are present once.\n'),
             ('aaaa', '"aaaa" => 0\nNo characters are present once.\n'),
             ('', '"" => 0\nNo characters are present once.\n')]

    @pytest.fixture
    def tmp_file(self, tmp_path):
        return tmp_path / "tmp_file.txt"

    @pytest.mark.parametrize("string_arg, expected_output", cases)
    def test_string_arg(self, monkeypatch, capsys, string_arg, expected_output):
        monkeypatch.setattr(sys, "argv", ['__main__.py', '--string', string_arg])
        main()
        captured = capsys.readouterr()
        assert captured.out == expected_output

    @pytest.mark.parametrize("file_content, expected_output", cases)
    def test_file_arg(self, monkeypatch, capsys, tmp_file, file_content, expected_output):
        tmp_file.write_text(file_content)
        monkeypatch.setattr(sys, "argv", ['__main__.py', '--file', str(tmp_file)])
        main()
        captured = capsys.readouterr()
        assert captured.out == expected_output

    def test_file_priority_over_string(self, monkeypatch, capsys, tmp_file):
        case = self.cases[1]
        tmp_file.write_text(case[0])
        sys_argv = ['__main__.py', '--file', str(tmp_file), '--string', 'zxc']
        monkeypatch.setattr(sys, "argv", sys_argv)
        main()
        captured = capsys.readouterr()
        assert captured.out == case[1]
