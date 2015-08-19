from __future__ import unicode_literals
from setuptools import setup, find_packages

setup(name='josiah-patron-accounts',
    version='0.6-dev',
    packages=find_packages(),
    install_requires=[ 'beautifulsoup4==4.3.2', 'requests==2.7.0' ],
)
