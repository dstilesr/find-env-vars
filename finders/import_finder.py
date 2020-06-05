import re
from .base import BaseFinder


class ImportFinder(BaseFinder):

    _patterns = [
        re.compile(r"(?<=from)\s*[a-z][a-zA-Z0-9_]+(?=[\.\s])"),
        re.compile(r"(?<=import)\s*[a-z][a-zA-Z0-9_]+(?=[\.\s])")
    ]



