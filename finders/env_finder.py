import re
import os
import json
from .base import BaseFinder


class EnvFinder(BaseFinder):
    """
    Class to find all environment variables mentioned in a python script
    or package / directory.
    """

    JSON_TEMPLATE = ".env.example.json"
    ENV_TEMPLATE = ".env.example"

    _patterns = [
        re.compile(r"(?<=getenv\()\s*['\"][A-Z_]+"),
        re.compile(r"(?<=environ\.get\()\s*['\"][A-Z_]+")
    ]

    def __init__(self, string: str, out_path: str = None):
        super().__init__(string=string)

        if out_path is None:
            out_path = string

        if not os.path.isdir(out_path):
            raise ValueError("out_path must be a directory!")

        self._out_path = out_path

    @property
    def out_path(self) -> str:
        return self._out_path

    def dump_matches_json(self):
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
        json_path = os.path.join(self.out_path, self.JSON_TEMPLATE)
        with open(json_path, "w") as f:
            json.dump(matches, f)
            print("INFO: Variables dumped to %s" % json_path)

    def dump_matches_env(self):
        """
        Save the matches to an env.example file.

        :return:
        """

        matches = [m + "=" for m in self.find_matches()]
        env_path = os.path.join(self.out_path, self.ENV_TEMPLATE)
        with open(env_path, "w") as f:
            f.write("\n".join(matches))
            print("INFO: Variables dumped to %s" % env_path)

    def dump_matches_all(self):
        """
        Save the matches to both an .env.example and a .env.example.json.

        :return:
        """

        self.dump_matches_env()
        self.dump_matches_json()

