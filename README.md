# Code experiments


## Project layout

I've adopted a `src/`-based structure.
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
