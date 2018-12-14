all:


# 'install' does not require `build` to be run first.
# It does everything and does not leave garbage files behind.
install: FORCE
	pip install --user .


# `build` may be useful because it prints out details
# of the compiling process.
build: FORCE
	python setup.py build


clean: FORCE
	rm -f pyx/*so
	rm -f src/c/datex/*.o
	rm -f src/c/datex/*.so
	rm -f src/cc/cc4py/*.so
	rm -f src/cc/datex/*.so
	rm -f src/pyx/cc/*.so
	rm -f src/pyx/datex/c/*.o
	rm -f src/pyx/datex/c/*.so
	rm -f src/pyx/datex/cc/*.o
	rm -f src/pyx/datex/cc/*.so
	rm -f src/pyx/datex/cy/_version09.c
	rm -f src/pyx/datex/cy/*.so
	rm -rf build dist
	pip uninstall pyx -y
	pip uninstall datex -y


FORCE:
