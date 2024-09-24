from setuptools import setup, find_packages

setup(
    name='Glassdoor',
    version='2.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = glassdoor.settings']},
)
