def task_build():

    return {
        'actions': ['python setup.py sdist'],
        'file_dep': [],
        'targets': [],
        'clean': ['rm -fr dist build *.egg-info __pycache__ .doit.db'],
        'verbosity': 2,
        }

def task_install():
    return {
        'actions': ['sudo pip3 install dist/miscutils-*.tar.gz',
                    'pip3 show miscutils'],
        'file_dep': [],
        'targets': [],
        'clean': [],
        'verbosity': 2,
        }

def task_uninstall():
    return {
        'actions': ['sudo pip3 uninstall miscutils -y'],
        'file_dep': [],
        'targets': [],
        'clean': [],
        'verbosity': 2,
        }

def task_pypi_register_test():
    """Updates meta info; note: ~/.pypirc must exist"""
    return {
        'actions': ['python setup.py register -r pypitest'],
        'file_dep': [],
        'targets': [],
        'clean': [],
        'verbosity': 2,
        }

def task_pypi_submit_test():
    """Creates release; note: ~/.pypirc must exist"""
    return {
        'actions': ['python setup.py sdist upload -r pypitest'],
        'file_dep': [],
        'targets': [],
        'clean': [],
        'verbosity': 2,
        }

def task_pypi_register_live():
    """Updates meta info; note: ~/.pypirc must exist"""
    return {
        'actions': ['python setup.py register -r pypi'],
        'file_dep': [],
        'targets': [],
        'clean': [],
        'verbosity': 2,
        }

def task_pypi_submit_live():
    """Creates release; note: ~/.pypirc must exist"""
    return {
        'actions': ['python setup.py sdist upload -r pypi'],
        'file_dep': [],
        'targets': [],
        'clean': [],
        'verbosity': 2,
        }

def task_test_code():
    return {
        'actions': ['export PYTHONPATH=$PYTHONPATH:. && py.test tests'],
        'file_dep': [],
        'targets': [],
        'clean': [],
        'verbosity': 2,
        }


