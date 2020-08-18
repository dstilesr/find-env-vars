import os
from sys import argv, exit
from .env_finder import EnvFinder

# Validate arguments
if len(argv) < 2:
    print("ERROR")
    print("USAGE: ")
    print("python -m finders <directory path>")
    exit(1)

if not os.path.isdir(argv[1]):
    print("ERROR")
    print("Invalid path! Must point to a directory.")
    exit(1)

# Find and dump matches
finder = EnvFinder(argv[1])
finder.dump_matches_all()
print("INFO: DONE!")
