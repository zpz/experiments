from setuptools import setup, Extension


extensions = [
    Extension('_cc11binds',
              sources=['src/py4cc/_cc11binds.cc'],
              extra_compile_args=['-std=c++11', '-O3'],
             )
]


setup(
    name='Python/C++ inter-op tester',
    version='0.1.0',
    packages=['py4cc'],
    ext_package='src/py4cc',
    ext_modules=extensions,
)
