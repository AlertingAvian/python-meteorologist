from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Python package to do a meteorologist\'s job.'
LONG_DESCRIPTION = 'Python package to get emergency alerts, forecasts, and severe weather outlooks.'

# Setting up
setup(
    name="python_meteorologist",
    version=VERSION,
    author="Patrick Maloney",
    author_email="alertingavian@vivaldi.net",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['geopy'],

    keywords=['python', 'weather', 'meteorology'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Weather",
        "License :: MIT License"
    ]
)
