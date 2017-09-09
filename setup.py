from setuptools import setup
import os

version = open(os.path.join(os.path.dirname(__file__), os.path.join('miscutils', 'VERSION'))).read().strip()

setup(
    name = 'miscutils',
    version = version,
    description = 'Miscellaneous utilities for general use.',
    author = 'Grzegorz Krason',
    author_email = 'grzegorz@krason.me',
    url = 'https://github.com/gergelyk/pymiscutils',
    download_url = 'https://github.com/gergelyk/pymiscutils/tarball/' + version,
    license = 'MIT',
    packages = ['miscutils'],
    package_data = {'': ['VERSION']},
    keywords = ['iterating', 'head', 'tail', 'listing', 'router', 'proxy', 'prompt', 'shell'],
    entry_points = {
        'console_scripts': ['pylisting=miscutils.tools.experimental.listing:main'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
)

