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

    _patterns = [
        re.compile(r"(?<=getenv\()\s*['\"][A-Z_]+"),
        re.compile(r"(?<=environ\.get\()\s*['\"][A-Z_]+")
    ]

    def __init__(self, path: str, out_path: str = ".env.example.json"):
        super().__init__(path=path)
        self._out_path = out_path

    @property
    def out_path(self) -> str:
        return self._out_path

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
