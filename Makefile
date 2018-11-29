all: libdatex pyx

pyx:
	python setup.py build_ext --inplace


libdatex:
	(cd src/cc/libdatex && make)


clean:
	rm -f src/pyx/cpp/_cc11binds*.so
	rm -f src/pyx/datex/*.so
	rm -f src/pyx/datex/cy_version09.c
	rm -f src/cc/libdatex/*.so
	(cd src/cc/libdatex && make clean)
