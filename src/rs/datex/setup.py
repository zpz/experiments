import sys

from setuptools import setup
from setuptools_rust import RustExtension, Binding, Strip
import toml


cfg = toml.load('Cargo.toml')
package_meta = cfg['package']

setup(
    name="datex",
    version=package_meta['version'],
    author=package_meta['authors'][0],
    packages=["datex"],
    rust_extensions=[
        RustExtension(
            "datex.datex",
            "Cargo.toml",
            binding=Binding.PyO3,
            strip=Strip.Debug,
        ),
    ],
    include_package_data=True,
    zip_safe=False,
)
