# Unit tests for file_operations.py
import os
from file_operations import FileOperations


def test_get_all_files():
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_file_operations_content")
    test_file = FileOperations(directory)
    result = test_file.get_all_files()
    expected = [os.path.join(directory, "lines.txt"),
                os.path.join(directory, "test.png"),
                os.path.join(directory, "test_file.txt")]
    assert all(item in expected for item in result)
    assert len(result) == 3


def test_get_all_files_of_type():
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_file_operations_content")
    test_file = FileOperations(directory)
    result = test_file.get_all_files_of_type("png")
    expected = os.path.join(directory, "test.png")
    assert result[0] == expected
    assert len(result) == 1


def test_get_random_file():
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_file_operations_content")
    test_file = FileOperations(directory)
    result = test_file.get_random_file()
    expected = [os.path.join(directory, "lines.txt"),
                os.path.join(directory, "test.png"),
                os.path.join(directory, "test_file.txt")]
    assert result in expected


def test_get_random_file_of_type():
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_file_operations_content")
    test_file = FileOperations(directory)
    result = test_file.get_random_file_of_type("txt")
    expected = [os.path.join(directory, "lines.txt"),
                os.path.join(directory, "test_file.txt")]
    assert result in expected


def test_get_artist_name():
    text = "DALL·E 2022-07-11 07.31.17 - cool bird wearing glasses in the style of lichtenstein, digital art.png"
    regex = " in the style of "
    expected = "lichtenstein, digital art.png"
    result = FileOperations.get_artist_name(text, regex)
    assert result == expected


def test_get_title_and_artist():
    text = "DALL·E 2022-07-11 07.31.17 - cool bird wearing glasses in the style of lichtenstein, digital art.png"
    preamble_regex = " .* - "
    artist_regex = " in the style of "
    file_extension = "png"
    expected = ("cool bird wearing glasses", "lichtenstein, digital art")
    result = FileOperations.get_title_and_artist(text, preamble_regex, artist_regex, file_extension)
    assert result == expected


def test_remove_text():
    text = "DALL·E 2022-07-11 07.31.17 - cool bird wearing glasses in the style of lichtenstein, digital art.png"
    remove = [", digital art", "in the style of ", "DALL·E "]
    expected = "2022-07-11 07.31.17 - cool bird wearing glasses lichtenstein.png"
    result = FileOperations.remove_text(text, remove)
    assert result == expected


def test_get_lines():
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_file_operations_content")
    path = os.path.join(directory, "lines.txt")
    result = FileOperations.get_lines(path)
    expected = ["first_line", "second_line", "third_line"]
    assert result == expected


def test_get_random_line():
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_file_operations_content")
    path = os.path.join(directory, "lines.txt")
    result = FileOperations.get_random_line(path)
    expected = ["first_line", "second_line", "third_line"]
    assert result in expected


def test_backup_file_both_exist():
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_file_operations_content")
    primary_path = os.path.join(directory, "lines.txt")
    backup_path = os.path.join(directory, "lines.txt")
    result = FileOperations.backup_file(primary_path, backup_path)
    expected = primary_path
    assert result == expected


def test_backup_file_no_primary():
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_file_operations_content")
    temp_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_temp")
    primary_path = os.path.join(temp_directory, "new_file.txt")
    backup_path = os.path.join(directory, "lines.txt")

    # Cleanup files before
    if os.path.exists(primary_path):
        os.remove(primary_path)

    result = FileOperations.backup_file(primary_path, backup_path)
    expected = primary_path
    assert os.path.exists(expected)
    assert result == expected

    # Cleanup files after
    if os.path.exists(primary_path):
        os.remove(primary_path)


def test_backup_file_fail():
    temp_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_temp")
    primary_path = os.path.join(temp_directory, "new_file.txt")
    backup_path = os.path.join(temp_directory, "non_existent.txt")

    # Cleanup files before
    if os.path.exists(primary_path):
        os.remove(primary_path)
    if os.path.exists(backup_path):
        os.remove(backup_path)

    result = FileOperations.backup_file(primary_path, backup_path)
    expected = None
    assert result == expected

    # Cleanup files after
    if os.path.exists(primary_path):
        os.remove(primary_path)
    if os.path.exists(backup_path):
        os.remove(backup_path)


def test_get_full_path():
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_file_operations_content")
    test_file = FileOperations(directory)
    result = test_file.get_full_path("test.png")
    expected = os.path.join(directory, "test.png")
    assert result == expected


def test_parse_text():
    text = "part1 (option1|option2) part3"
    result = FileOperations.parse_text(text)
    expected = ["part1 option1 part3", "part1 option2 part3"]
    assert result in expected
