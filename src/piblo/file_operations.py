#!/usr/bin/python3
# -*- coding:utf-8 -*-

import glob
import logging
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

    get_first_line(path)
        returns the first line from a text file located at 'path'

    get_random_line(path)
        returns a random line from file located at 'path'

    backup_file(primary_path, backup_path)
        if 'primary_path' does not exist, copies file at 'backup_path' to 'primary_path'.
        returns 'primary_path' if operation worked, otherwise returns None if both paths do not exist

    get_full_path(path)
        Returns full file system path of path relative to config_wrapper.py file.

    parse_text(text)
        String parsing method that pulls out text with random options in it

    parse_weighted_lines(weighted_lines)
        Takes a list of strings 'weighted_lines' and parses leading integers in the string before a ':' character.
        Adds that integers amount that line to the list
        Returns the updated list of strings
    """

    def __init__(self, path=os.getcwd()):
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
        if size == 0:
            logging.warning(f"Unable to find any files in '{self.path}'")
            return
        random.seed()
        r = random.randint(0, size - 1)
        return all_files[r]

    def get_random_file_of_type(self, file_type):
        # returns path for a random file in the current path with extension 'type'
        # type value 'png' could return cat.png
        all_files = self.get_all_files_of_type(file_type)
        size = len(all_files)
        if size == 0:
            logging.warning(f"Unable to find any files of type '{file_type}' in '{self.path}'")
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
    def get_first_line(path):
        lines = FileOperations.get_lines(path)
        lines = FileOperations.parse_weighted_lines(lines)
        size = len(lines)
        if size == 0:
            logging.warning(f"No lines to parse found in file {path}")
            return
        return lines[0]

    @staticmethod
    def get_random_line(path):
        lines = FileOperations.get_lines(path)
        lines = FileOperations.parse_weighted_lines(lines)
        size = len(lines)
        if size == 0:
            logging.warning(f"No lines to parse found in file {path}")
            return
        random.seed()
        r = random.randint(0, size - 1)
        return lines[r]

    @staticmethod
    def backup_file(primary_path, backup_path):
        try:
            if os.path.exists(primary_path):
                return primary_path
            elif os.path.exists(backup_path):
                logging.info(f"{primary_path} does not exist. Copying {backup_path} to {primary_path}")
                shutil.copy2(backup_path, primary_path)
                return primary_path
            logging.warning(f"Unable to find file at '{primary_path}' or at backup path '{backup_path}'")
            return primary_path
        except FileNotFoundError:
            logging.warning(f"Unable to find file at '{primary_path}' or at backup path '{backup_path}'")
            return primary_path

    def get_full_path(self, path):
        full_path = os.path.join(self.path, path)
        return full_path

    @staticmethod
    def parse_text(text, bracket_one="(", bracket_two=")"):
        # Get everything inside brackets
        regex = fr"\{bracket_one}.*?\{bracket_two}"
        brackets = re.findall(regex, text)
        for bracket in brackets:
            # Get random item
            bracket = bracket.replace(bracket_one, '').replace(bracket_two, '')
            random.seed()
            options = FileOperations.parse_weighted_lines(bracket.split('|'))
            option = random.choice(options)
            # Substitute brackets
            text = re.sub(regex, option, text, 1)
        return text

    @staticmethod
    def parse_weighted_lines(weighted_lines):
        lines = []
        # Find any colons at the start of the line, use preceding text if it's an integer
        for line in weighted_lines:
            amount = 1
            split = line.split(':', maxsplit=1)
            # If there is a valid colon, split it on the first one, add it that many times to list
            if len(split) > 1 and split[0].isdigit():
                amount = int(split[0])
                line = split[1]
            for i in range(amount):
                lines.append(line)
        return lines

    @staticmethod
    def extract_number(path):
        try:
            # assume everything after `_` is a number
            return int(path.rpartition('_')[-1])
        except ValueError:
            # not everything was a number, skip this directory
            return None
        return

    @staticmethod
    def version_file(file_path):
        # Use glob to backup https://stackoverflow.com/questions/38885370/rename-backup-old-directory-in-python
        if os.path.exists(file_path):
            backups = glob.glob(file_path + '_[0-9]*')

            backup_numbers = (FileOperations.extract_number(b) for b in backups)
            try:
                next_backup = max(filter(None, backup_numbers)) + 1
            except ValueError:
                # no backup files
                next_backup = 1

        new_path = file_path + '_{:d}'.format(next_backup)

        os.rename(file_path, new_path)
        return new_path
