from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

debug = False

numpy_include_dir = numpy.get_include()

cy_options = {
    'annotate': debug,
    'compiler_directives': {
        'profile': debug,
        'linetrace': debug,
        'wraparound': debug,
        'boundscheck': debug,
        'initializedcheck': debug,
        'language_level': 3,
    },
}

cpp_extensions = [
    Extension('cpp._cc11binds',
              sources=['src/pyx/cpp/_cc11binds.cc'],
              extra_compile_args=['-std=c++17', '-O3'],
             ),
]

cy_extensions = [
    Extension(
        'datex.version04', ['src/pyx/datex/version04.pyx'],
        include_dirs=[numpy_include_dir,],
        define_macros=[('CYTHON_TRACE', '1' if debug else '0')],
        extra_compile_args=['-O3'],
        ),
]


setup(
    name='Python extensions in other languages',
    version='0.1.0',
    packages=['pyx'],
    ext_package='src/pyx',
    ext_modules=cpp_extensions + cythonize(cy_extensions, **cy_options),
)
