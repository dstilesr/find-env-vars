import re
import os
import json
from typing import List
from .common import BaseFinder


class EnvFinder(BaseFinder):
    """
    Class to find all environment variables mentioned in a python script
    or package / directory.
    """

    GETENV_REGEX = re.compile(r"(?<=getenv\()\s*['\"][A-Z_]+")
    ENVIRON_REGEX = re.compile(r"(?<=environ\.get\()\s*['\"][A-Z_]+")

    def __init__(self, path: str, out_path: str = ".env.example.json"):

        if os.path.isdir(path):
            self._method = self.find_in_directory
        elif self.PYTHON.search(path) is not None:
            self._method = self.find_in_file
        else:
            raise ValueError("Path must be a python file or a directory!")

        self._path = path
        self._out_path = out_path
        self._matches = []

    @property
    def out_path(self) -> str:
        return self._out_path

    @classmethod
    def find_in_string(cls, string: str) -> List[str]:
        """
        Finds all matches in the given string (contents of a file).

        :param string:
        :return:
        """
        matches = (
            cls.ENVIRON_REGEX.findall(string)
            + cls.GETENV_REGEX.findall(string)
        )
        return [cls.CLEANUP_REGEX.sub("", m) for m in matches]

    @classmethod
    def find_in_file(cls, filepath: str) -> List[str]:
        """

        :param filepath:
        :return:
        """

        if not os.path.isfile(filepath):
            raise ValueError("File does not exist!")

        with open(filepath, "r") as f:
            contents = f.read()

        return cls.find_in_string(contents)

    @classmethod
    def find_in_directory(
            cls,
            directory: str) -> List[str]:
        """
        Finds all matches in the python files of the given directory and its
        child directories.

        :param directory: Path to a directory.
        :return:
        """
        out = []
        for fp in os.listdir(directory):
            full_path = os.path.join(directory, fp)

            if os.path.isdir(full_path):
                if cls.is_python_package(full_path):
                    out += cls.find_in_directory(full_path)

            elif cls.PYTHON.search(full_path) is not None:
                out += cls.find_in_file(full_path)

        return out

    @staticmethod
    def is_python_package(directory: str) -> bool:
        return "__init__.py" in os.listdir(directory)

    def dump_matches(self):
        """
        Saves the matches to a json example template.

        :return:
        """
        matches = [
            {
                "key": m,
                "value": "",
                "description": ""
            }
            for m in self.find_matches()
        ]
        with open(self._out_path, "w") as f:
            json.dump(matches, f)
            print("INFO: Variables dumped to %s" % self._out_path)
