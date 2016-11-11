from setuptools import setup
import os

top_dir, _ = os.path.split(os.path.abspath(__file__))

with open(os.path.join(top_dir, 'VERSION')) as f:
    version = f.readline().strip()

setup(
    name = 'miscutils',
    version = version,
    description = 'Miscellaneous utilities for general use.',
    author = 'Grzegorz Krason',
    author_email = 'grzegorz@krason.biz',
    url = 'https://github.com/gergelyk/pymiscutils',
    download_url = 'https://github.com/gergelyk/pymiscutils/tarball/' + version,
    license = 'MIT',
    packages = ['miscutils'],
    package_data = {'': ['../VERSION']},
    keywords = ['iterating', 'head', 'tail', 'listing', 'router', 'proxy', 'prompt', 'shell'],
    classifiers = [],
    entry_points = {
        'console_scripts': ['pylisting=miscutils.listing:main'],
    },
)

