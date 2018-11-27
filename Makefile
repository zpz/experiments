all: pyx

pyx:
	python setup.py build_ext --inplace


clean:
	rm -f src/pyx/cpp/_cc11binds*.so
	rm -f src/pyx/datex/*.c src/pyx/datex/*.so