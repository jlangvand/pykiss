"""
Setup module based on Setuptools
"""

import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name="pykiss",
    version="0.2.1",
    author="Orbit NTNU",
    author_email="cto@orbitntnu.com",
    description="Simple serial KISS library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jlangvand/pykiss",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Communications :: Ham Radio",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires='>=3.6',
    install_requires=['pyserial'],
    project_urls={
        "Orbit NTNU": "https://orbitntnu.com",
    },
)
