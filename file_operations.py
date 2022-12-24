import logging
import glob
import os
import random
import re
import shutil


class FileOperations:
    """
    A class used to provide file operations for pycasso.

    Attributes
    ----------
    path:string
        path for file operations

    Methods
    -------
    get_all_files():
        returns path of all files in folder

    get_all_files_of_type(type):
        returns path of all files in folder with extension 'type'
        type value 'png' would include cat.png

    get_random_file()
        returns path for a random file in the current path

    get_random_file_of_type(type):
        returns path for a random file in the current path with extension 'type'
        type value 'png' could return cat.png

    get_lines(path)
        returns every line as a separate item in an array from a text file located at 'path'

    get_random_line(path)
        returns a random line from file located at 'path'

    backup_file(primary_path, backup_path)
        if primary_path does not exist, copies file at backup_path to primary_path.
        returns primary_path if operation worked, otherwise returns None if both paths do not exist

    get_full_path(path)
        Returns full file system path of path relative to config_wrapper.py file.


    parse_text(text)
        String parsing method that pulls out text with random options in it
    """

    def __init__(self, path=os.path.dirname(os.path.abspath(__file__))):
        self.path = path
        return

    def get_all_files(self):
        # returns path of all files in folder
        return glob.glob(self.path + "/*")

    def get_all_files_of_type(self, file_type):
        # returns path of all files in folder with extension 'type'
        # type value 'png' would include cat.png
        return glob.glob(self.path + "/*." + file_type)

    def get_random_file(self):
        # returns path for a random file in the current path
        all_files = self.get_all_files()
        size = len(all_files)
        # TODO: handle if no files
        random.seed()
        r = random.randint(0, size - 1)
        return all_files[r]

    def get_random_file_of_type(self, file_type):
        # returns path for a random file in the current path with extension 'type'
        # type value 'png' could return cat.png
        all_files = self.get_all_files_of_type(file_type)
        size = len(all_files)
        if size == 0:
            return
        random.seed()
        r = random.randint(0, size - 1)
        return all_files[r]

    @staticmethod
    def get_artist_name(text, regex):
        # returns artist name within a string from a file name based on 'regex'
        # assumes artist name comes LAST
        split = re.split(regex, text)
        # handle list
        if len(split) < 2:
            return text
        return split[1]

    @staticmethod
    def get_title_and_artist(text, preamble_regex, artist_regex, file_extension):
        # returns tuple (title, artist name) within a string from a file name
        # preamble_regex should cut any text before the title
        # artist_regex should cut any text in between title and artist
        # assumes title comes after some preamble, artist name comes LAST
        # returns (text, "") on failure

        split = re.split(preamble_regex + "|" + artist_regex + "|\\." + file_extension, text)
        # handle list
        if len(split) < 4:
            tup = (text, "")
            return tup

        tup = (split[1], split[2])
        return tup

    @staticmethod
    def remove_text(text, remove):
        # removes text from string for all strings in 'remove'
        regex = ""
        for r in remove:
            regex = regex + r + "|"
        # remove last |
        regex = regex.rstrip('|')
        text = re.sub(regex, "", text)
        return text

    @staticmethod
    def get_lines(path, encoding='utf-8'):
        lines = []
        with open(path, encoding=encoding) as file:
            for line in file:
                lines.append(line.strip())
        return lines

    @staticmethod
    def get_random_line(path):
        lines = FileOperations.get_lines(path)
        size = len(lines)
        if size == 0:
            return
        random.seed()
        r = random.randint(0, size - 1)
        return lines[r]

    @staticmethod
    def backup_file(primary_path, backup_path):
        if os.path.exists(primary_path):
            return primary_path
        elif os.path.exists(backup_path):
            logging.info(f"{primary_path} does not exist. Copying {backup_path} to {primary_path}")
            shutil.copy2(backup_path, primary_path)
            return primary_path
        return None

    def get_full_path(self, path):
        full_path = os.path.join(self.path, path)
        return full_path

    @staticmethod
    def parse_text(text):
        # Get everything inside brackets
        brackets = re.findall(r"\(.*?\)", text)
        for bracket in brackets:
            # Get random item
            bracket = bracket.replace('(', '').replace(')', '')
            random.seed()
            option = random.choice(bracket.split('|'))
            # Substitute brackets
            text = re.sub(r"\(.*?\)", option, text, 1)
        return text
