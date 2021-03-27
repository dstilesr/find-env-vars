# Pattern Finders

## Contents
* [About](#about)
* [Use Example](#use-example)
* [New Finders](#new-finders)


## About

This is a small python package containing classes that find certain patterns in
python files such as the environment variables used or the list of imports of
a package. This was done mainly as an excercise in the use of regular
expressions.

## Use Example
To run the environment variable finder from a python session, you can do it as
follows:
```python
import finders

project = "<some python project>"
envs = finders.EnvFinder(project)

print(envs.find_matches())
```

Additionally, you can find and dump the environment variables of a project running
the module directly from the terminal with:
```shell script
python -m finders <path-to-project>
```
You can also pass the path to the project by name as follows:
```shell
python -m finders --source_dir=<path-to-project>
```


## New Finders

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
