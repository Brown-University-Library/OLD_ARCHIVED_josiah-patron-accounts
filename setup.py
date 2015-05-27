from setuptools import setup, find_packages

setup(name='josiah-patron-accounts',
    version='0.2-dev',
    packages=find_packages(),
    install_requires=[ u'pyquery==1.2.9', u'requests==2.7.0' ],
)
