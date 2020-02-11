# miscutils

These are miscellaneous python utilities for general use. This package includes following submodules:

* **dbg** - Debugging utilities.
* **func** - Utilities related to functions.
* **insp** - Utilities for inspecting the code.
* **io** - Interacting with input/output of python script.
* **iter** - Interacting with iterators and collections.
* **os** - Operating system related utilities.
* **str** - Handling strings.
* **tools** - Not the code, but utilities for programmers.
* **user** - User data processing.

## Developing

Start from preparing venv:

```sh
python3.7 -m poetry install
```

## Building Docs

Update `.rst` manually. Then:

```sh
python3.7 -m poetry run make -C docs html
```

## Testing

```sh
python3.8 -m poetry run pytest tests
```

## Releasing

Update version in `pyproject.toml`. Then:

```sh
python3.7 -m poetry build
git tag X.Y.Z
git push
git push --tags
python3.7 -m poetry publish
```

log into readthedocs.io and trigger a Build

## References

[Documentation](http://pymiscutils.readthedocs.io/)

[Source code](https://github.com/gergelyk/pymiscutils/)

[Package](https://pypi.python.org/pypi/miscutils/)
