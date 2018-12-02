# pyx

Various Python experiments, mainly related to inter-operations with other languages.

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