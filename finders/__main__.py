import os
import fire
from .env_finder import EnvFinder


def find_env_variables(source_dir: str = "."):
    """
    Find the names of all environment variables used in a python project and
    save the results to a .env.example and a json file.
    :param source_dir: Directory of the project to be searched.
    :return: None
    """
    if not os.path.isdir(source_dir):
        raise FileNotFoundError(
            "The path '%s' is not a directory!" % source_dir
        )

    finder = EnvFinder(source_dir)
    finder.dump_matches_all()


# Launch with Fire
fire.Fire(find_env_variables)
