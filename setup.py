from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import numpy
from cffi import FFI
from setuptools_rust import RustExtension, Binding, Strip


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

cy_extensions = cythonize([
    Extension(
        'datex.cy._version09', 
        sources=['src/python_ext/datex/cy/_version09.pyx'],
        include_dirs=[numpy_include_dir,],
        define_macros=[('CYTHON_TRACE', '1' if debug else '0')],
        extra_compile_args=['-O3', '-Wall'],
        ),
    ],
    **cy_options
    )


cc_options = ['--std=c++17', '-O3', '-Wall', '-Wextra', '-Wfatal-errors']

cc_extensions = [
    Extension(
        'pycc._cc11binds',
        sources=['src/python/pycc/_cc11binds.cc'],
        extra_compile_args=cc_options,
        ),
    Extension(
        'datex.cc.version01',
        sources=['src/python_ext/datex/cc/version01.cc',
                 'src/cc/datex/cc_version01.cc'],
        include_dirs=['src/cc'],
        extra_compile_args=cc_options,
        ),
    Extension(
        'datex.cc.version02',
        sources=['src/python_ext/datex/cc/version02.cc',
                 'src/cc/datex/cc_version01.cc'],
        include_dirs=['src/cc'],
        extra_compile_args=cc_options,
        ),
    ]

# If need to load a shared library at run-time,
# set `LD_LIBRARY_PATH` when running Python, or install the shared libs in system location.
# There is a `runtime_library_dirs` argument to `Extension` that seems relevant
# but I failed to make it work.


cffi_extensions = [
    'src/python_ext/datex/c/_version01_build.py:ffibuilder',
    ]


rust_extensions = [
    RustExtension(
        "datex.rs.version01",
        "src/python_ext/datex/rs/Cargo.toml",
        binding=Binding.PyO3,
        strip=Strip.Debug,
    ),
]


setup(
    name='pyx',
    version='0.1.0',
    package_dir={'': 'src/python'},
    packages=find_packages(where='src/python'),
    ext_modules=cc_extensions + cy_extensions,
    cffi_modules=cffi_extensions,
    rust_extensions=rust_extensions,
    include_package_data=True,
    zip_safe=False,
)
