__author__ = 'antonibote'
from setuptools import setup, find_packages
import os
setup(
    name='pygoogle',
    version="1.0",
    description="Python library to Google services",
    long_description="some useful google services for language processing.",
    classifiers=[],
    keywords='google search',
    author='antonibote',
    author_email='antoni.bote@upc.edu',
    url='http://github.com/antonibote/pygoogle',
    license='MIT',
    packages=find_packages(),
    entry_points={
        # -*- Entry points: -*-
    },
    package_data={'': ['user-agents.txt', 'domains.txt']},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        "requests", "beautifulsoup4", "keyring", "pycryptodome"
    ],
)
