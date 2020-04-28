import re
from typing import Callable, List


class BaseFinder(object):
    """
    Abstract class to represent finder objects.
    """

    CLEANUP_REGEX = re.compile(r"[\s'\"]")
    PYTHON = re.compile(r"\.py$|\.pyx$")
    _method: Callable[[str], List[str]]
    _matches: List[str]
    _path: str

    @property
    def path(self) -> str:
        return self._path

    def find_matches(self) -> List[str]:
        """
        Finds all matches in the file/directory to which this object refers.

        :return: List of unique strings.
        """
        if self._matches is not None or len(self._matches) > 0:
            out = self._matches
        else:
            out = list(set(self._method(self._path)))
            out.sort()
            self._matches = out
        return out

