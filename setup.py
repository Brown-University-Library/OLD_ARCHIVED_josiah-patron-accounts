from setuptools import setup, find_packages

setup(name='josiah-patron-accounts',
    version='0.3-dev',
    packages=find_packages(),
    install_requires=[ u'beautifulsoup4==4.3.2', u'requests==2.7.0' ],
)
