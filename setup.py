from setuptools import setup

setup(
    name = 'miscutils',
    version = '0.10',
    description = 'Miscellaneous utilities for general use.',
    author = 'Grzegorz Krason',
    author_email = 'grzegorz@krason.biz',
    url = 'https://github.com/gergelyk/pymiscutils',
    download_url = 'https://github.com/gergelyk/pymiscutils/tarball/0.10',
    license = 'MIT',
    packages = ['miscutils'],
    keywords = ['iterating', 'head', 'tail', 'listing', 'router', 'proxy', 'prompt', 'shell'],
    classifiers = [],
    entry_points = {
        'console_scripts': ['pylisting=miscutils.listing:main'],
    },
)

