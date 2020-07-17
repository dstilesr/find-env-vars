# README

# Contents
* [About](#about)
* [Use Example](#use-example)
* [New Finders](#new-finders)


# About

This is a small python package containing classes that find certain patterns in
python files such as the environment variables used or the list of imports of
a package. This was done mainly as an excercise in the use of regular
expressions.

# Use Example

```python
import finders

project = "<some python project>"
envs = finders.EnvFinder(project)

print(envs.find_matches())
```

# New Finders

In order to create a new pattern finder you can simply create a subclass of
`BaseFinder` and store the list of patterns you want to match in the class
constant `_patterns`. For example, to find words ending in Q or q in a
paragraph you could do the following:
```python
import re
from finders.base import BaseFinder

class EndQFinder(BaseFinder):
    """
    Find words ending in Q or q.
    """

    _patterns = [
        re.compile(r"[a-zA-Z]*[qQ](?![a-zA-Z])")
    ]

```
