all: pyx


pyx:
	python setup.py build_ext --inplace


clean:
	rm -f pyx/*so
	rm -f src/c/*.o
	rm -f src/c/*.so
	rm -f src/c/datex/*.o
	rm -f src/c/datex/*.so
	rm -f pyx/cc/*.o
	rm -f pyx/cc/*.so
	rm -f pyx/datex/*.so
	rm -f pyx/datex/*.o
	rm -f pyx/datex/cy_version09.c
	rm -f pyx/datex/_c_version01.c
	rm -rf build
