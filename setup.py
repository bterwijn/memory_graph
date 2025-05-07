# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description_from_readme = (this_directory / "README.md").read_text()

setup(
    name = 'memory_graph',
    version = '0.3.22',
    description = 'Generate intuitive graphs of your Python data, great for debugging and understanding complex relationships.',
    long_description = long_description_from_readme,
    long_description_content_type = 'text/markdown',
    readme = 'README.md',
    url = 'https://github.com/bterwijn/memory_graph',
    author = 'Bas Terwijn',
    author_email = 'bterwijn@gmail.com',
    license = 'BSD 2-clause',
    packages = ['memory_graph'],
    install_requires = ['graphviz'],

    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  
        'Programming Language :: Python :: 3',
        'Topic :: Education',
        'Topic :: Software Development :: Debuggers',
    ],
)
