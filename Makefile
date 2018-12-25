all:


# 'install' does not require `build` to be run first.
# It does everything and does not leave garbage files behind.
install: FORCE
	python setup.py build_rust
	pip install --user .


# `build` may be useful because it prints out details
# of the compiling process.
build: FORCE
	python setup.py build


clean: FORCE
	rm -f src/python_ext/datex/cy/_version09.c
	rm -rf build dist
	rm -rf build
	rm -rf src/python/*egg-info
	rm -rf .pytest_cache
	pip uninstall pyx -y
	pip uninstall datex -y


FORCE:
