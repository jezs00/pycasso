import os
import glob
import random


class FileLoader:
    """
    A class used to provide file operations.

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
    """
    def __init__(self, path):
        self.path = path
        return

    def get_all_files(self):
        # returns path of all files in folder
        print(self.path + "\\*")
        return glob.glob(self.path + "\\*")

    def get_all_files_of_type(self, type):
        # returns path of all files in folder with extension 'type'
        # type value 'png' would include cat.png
        return glob.glob(self.path + "\\*." + type)

    def get_random_file(self):
        # returns path for a random file in the current path
        all_files = self.get_all_files()
        size = len(all_files)
        random.seed
        r = random.randint(0, size-1)
        return all_files[r]

    def get_random_file_of_type(self, type):
        # returns path for a random file in the current path with extension 'type'
        # type value 'png' could return cat.png
        all_files = self.get_all_files_of_type(type)
        size = len(all_files)
        random.seed
        r = random.randint(0, size-1)
        return all_files[r]

    # TODO make type functions that can take multiple types
    # TODO make function that just takes normal regex