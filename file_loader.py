import logging
import glob
import random
import re


class FileLoader:
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
    """

    def __init__(self, path):
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
        logging.info(split)
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
    def get_lines(path):
        lines = []
        with open(path) as file:
            for line in file:
                lines.append(line)
        return lines

    @staticmethod
    def get_random_line(path):  # TODO: more unit tests!
        lines = FileLoader.get_lines(path)
        size = len(lines)
        if size == 0:
            return
        random.seed()
        r = random.randint(0, size - 1)
        return lines[r]

    # TODO make type functions that can take multiple types
    # TODO make function that just takes normal regex
