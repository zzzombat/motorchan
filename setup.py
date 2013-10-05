# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os, sys
sys.path.insert(0, 'src')
import motorchan

requires = [
    'tornado',
    'motor',
]

setup(
    name='motorchan',
    version=motorchan.__version__,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'motorchan = motorchan:run',
        ],
    },
)
