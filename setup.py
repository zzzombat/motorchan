# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

requires = [
    'tornado',
    'motor',
    'wtforms',
    'tornadotools',  # require libcurl4-openssl-dev
    'tornado-utils',
    'webassets',
    'jsmin',
    'jsonschema',
    'python-dateutil',
]

setup(
    name='motorchan',
    version='0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'motorchan = motorchan:run',
            'motorchan-initdb = motorchan.initdb:main',
        ],
    },
    test_suite='tests',
)
