from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy
from cffi import FFI


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

cc_options = ['--std=c++17', '-O3']


cc_extensions = [
    Extension(
        'cc._cc11binds',
        sources=['src/pyx/cc/_cc11binds.cc'],
        extra_compile_args=cc_options,
        ),
    Extension(
        'datex.cc_version01',
        sources=['src/pyx/datex/cc_version01.cc'],
        extra_compile_args=cc_options,
        ),
    Extension(
        'datex.cc_version02',
        sources=['src/pyx/datex/cc_version02.cc'],
        extra_compile_args=cc_options,
        ),
    Extension(
        'datex.cc_version03',
        sources=['src/pyx/datex/cc_version03.cc'],
        extra_compile_args=cc_options + ['-Isrc/cc/datex'],
        ),
    Extension(
        'datex.cc_version04',
        sources=['src/pyx/datex/cc_version04.cc'],
        extra_compile_args=cc_options + ['-Isrc/cc/libdatex'],
        # runtime_library_dirs=['/home/docker-user/work/src/py-extensions/src/cc/libdatex'],
        # libraries=['datex'],
        ),
    ]

# Failed to make `runtime_library_dirs` work.
# Set `LD_LIBRARY_PATH` when running Python, or install shared libs in system location.


cy_extensions = cythonize([
    Extension(
        'datex.cy_version09', 
        sources=['src/pyx/datex/cy_version09.pyx'],
        include_dirs=[numpy_include_dir,],
        define_macros=[('CYTHON_TRACE', '1' if debug else '0')],
        extra_compile_args=['-O3'],
        ),
    ],
    **cy_options
    )


setup(
    name='Python extensions in other languages',
    version='0.1.0',
    packages=['pyx'],
    ext_package='src/pyx',
    ext_modules=cc_extensions + cy_extensions,
    # cffi_package='src/pyx',
    cffi_modules=['_build/_c_version01_build.py:ffibuilder'],
)
