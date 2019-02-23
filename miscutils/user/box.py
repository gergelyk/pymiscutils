
class Box:

    def __init__(self, target):
        super().__setattr__('_target', target)

    def _wrap(self, item):

        if isinstance(item, (dict, list)):
            return self.__class__(item)

        return item

    def __str__(self):
        return str(self._target)

    def __repr__(self):
        return f"{self.__class__.__name__}({self._target!r})"

    def __eq__(self, other):
        return self._target == other

    def __len__(self):
        return len(self._target)

    def __getattr__(self, key):
        try:
            return getattr(self._target, key)
        except AttributeError:
            return self[key]

    def __setattr__(self, key, val):
        self[key] = val

    def __delattr__(self, key):
        del self[key]

    def __getitem__(self, key):
        return self._wrap(self._target[key])

    def __setitem__(self, key, val):
        self._target[key] = val

    def __delitem__(self, key):
        del self._target[key]


