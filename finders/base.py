import re
import os
from typing import Callable, List


class BaseFinder(object):
    """
    Abstract class to represent finder objects.
    """

    CLEANUP_REGEX = re.compile(r"[\s'\"]")
    PYTHON = re.compile(r"\.py$|\.pyx$")
    _patterns: List[re.Pattern]
    _method: Callable[[str], List[str]]
    _matches: List[str]
    _path: str

    def __init__(self, path: str):
        if os.path.isdir(path):
            self._method = self.find_in_directory
        elif self.PYTHON.search(path) is not None:
            self._method = self.find_in_file
        else:
            raise ValueError("Path must be a python file or a directory!")

        self._path = path
        self._matches = []

    @property
    def path(self) -> str:
        return self._path

    @property
    def patterns(self) -> List[re.Pattern]:
        return self._patterns

    @staticmethod
    def is_python_package(directory: str) -> bool:
        return "__init__.py" in os.listdir(directory)

    @classmethod
    def find_in_string(cls, string: str) -> List[str]:
        """
        Finds all matches in the given string (contents of a file).

        :param string:
        :return:
        """
        matches = []
        for p in cls._patterns:
            matches += p.findall(string)
        return [cls.CLEANUP_REGEX.sub("", m) for m in matches]

    @classmethod
    def find_in_file(cls, filepath: str) -> List[str]:
        """

        :param filepath:
        :return:
        """

        if not os.path.isfile(filepath):
            raise FileNotFoundError("File does not exist!")

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

    def find_matches(self) -> List[str]:
        """
        Finds all matches in the file/directory to which this object refers.

        :return: List of unique strings.
        """
        if self._matches is not None and len(self._matches) > 0:
            out = self._matches
        else:
            out = list(set(self._method(self._path)))
            out.sort()
            self._matches = out
        return out

