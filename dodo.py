PACKAGE = '_PACKAGE_NAME_'

def task_prepenv():
    """Prepare environment for other commands."""
    return {
        'actions': [],
        'file_dep': [],
        'task_dep': [],
        'targets': [],
        'clean': ['rm -fr __pycache__ {}/__pycache__ .doit.db .cache'.format(PACKAGE)],
        'verbosity': 2,
        }

def task_build():
    """Build Python package."""
    return {
        'actions': ['python setup.py sdist'],
        'file_dep': [],
        'task_dep': ['prepenv'],
        'targets': [],
        'clean': ['rm -fr dist build *.egg-info'],
        'verbosity': 2,
        }

def task_test():
    """Test Python code."""
    return {
        'actions': ['export PYTHONPATH=$PYTHONPATH:. && py.test tests'],
        'file_dep': [],
        'task_dep': ['prepenv'],
        'targets': [],
        'clean': ['rm -fr tests/__pycache__'],
        'verbosity': 2,
        }

def task_install():
    """(Re)install package in the system."""
    return {
        'actions': ['sudo pip3 install dist/{}-*.tar.gz --upgrade'.format(PACKAGE),
                    'pip3 show {}'.format(PACKAGE)],
        'file_dep': [],
        'task_dep': ['prepenv'],
        'targets': [],
        'clean': [],
        'verbosity': 2,
        }

def task_uninstall():
    """Uninstall package from the system."""
    return {
        'actions': ['sudo pip3 uninstall {} -y'.format(PACKAGE)],
        'file_dep': [],
        'task_dep': ['prepenv'],
        'targets': [],
        'clean': [],
        'verbosity': 2,
        }

def task_pypi_register_test():
    """Updates meta info; note: ~/.pypirc must exist"""
    return {
        'actions': ['python setup.py register -r pypitest'],
        'file_dep': [],
        'task_dep': ['prepenv'],
        'targets': [],
        'clean': [],
        'verbosity': 2,
        }

def task_pypi_submit_test():
    """Creates release; note: ~/.pypirc must exist"""
    return {
        'actions': ['python setup.py sdist upload -r pypitest'],
        'file_dep': [],
        'task_dep': ['prepenv'],
        'targets': [],
        'clean': [],
        'verbosity': 2,
        }

def task_pypi_register_live():
    """Updates meta info; note: ~/.pypirc must exist"""
    return {
        'actions': ['python setup.py register -r pypi'],
        'file_dep': [],
        'task_dep': ['prepenv'],
        'targets': [],
        'clean': [],
        'verbosity': 2,
        }

def task_pypi_submit_live():
    """Creates release; note: ~/.pypirc must exist"""
    return {
        'actions': ['python setup.py sdist upload -r pypi'],
        'file_dep': [],
        'task_dep': ['prepenv'],
        'targets': [],
        'clean': [],
        'verbosity': 2,
        }

def task_docs_build():
    """Builds documentation."""
    return {
        'actions': ['cd docs && make html'],
        'file_dep': [],
        'task_dep': ['prepenv'],
        'targets': [],
        'clean': ['rm -fr docs/build'],
        'verbosity': 2,
        }

