all: libdatex pyx

pyx:
	python setup.py build_ext --inplace


libdatex:
	(cd src/cc/libdatex && make)


clean:
	rm -f src/c/*.o
	rm -f src/c/*.so
	rm -f src/pyx/*so
	rm -f src/pyx/cc/*.so
	rm -f src/pyx/datex/*.so
	rm -f src/pyx/datex/*.o
	rm -f src/pyx/datex/cy_version09.c
	rm -f src/pyx/datex/_c_version01.c
	rm -f src/cc/libdatex/*.so
	rm -f src/c/datex/*.o
	(cd src/cc/libdatex && make clean)
