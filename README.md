# experiments.py

Various Python experiments.
Currently the content is mainly related to inter-operations with other languages.
Other topics will appear over time.
There is no guarantee that the content and directory structure of this repo will be stable.

## Project layout

I've adopted a `src/`-based structure.
[This blogpost](https://hynek.me/articles/testing-packaging/) might be a good reference regarding this structure.

A critical detail in `setup.py` related to this structure is these two arguments:

```
setup(
    [...]
    package_dir={'': 'src/python'},
    packages=find_packages(where='src/python'),
    [...]
)
```

# Installation

Do this:

```
pip install --user .
```
