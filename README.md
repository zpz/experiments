# experiments.py

Various Python experiments.
Currently the content is mainly related to inter-operations with other languages.
Other topics will appear over time. The content and strucuture of this repo may change at any time in any way.


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
