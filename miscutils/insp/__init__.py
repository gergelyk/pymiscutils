import inspect

def getdefault(func, argname):
    """Get default value of the argument called `argname` from signature of the function `func`."""
    if not isinstance(argname, str):
        raise RuntimeError(f"argname must be of str type.")

    spec = inspect.getfullargspec(func)

    # these attributes can be None
    spec_defaults = spec.defaults if spec.defaults else []
    spec_kwonlydefaults = spec.kwonlydefaults if spec.kwonlydefaults else {}

    if argname in spec.args:
        args_rev = spec.args[::-1]
        defs_rev = spec_defaults[::-1]
        idx = args_rev.index(argname)
        try:
            return defs_rev[idx]
        except IndexError:
            raise RuntimeError(f"Positional argument '{argname}' doesn't have default value.") from None

    elif argname in spec.kwonlyargs:
        if argname in spec_kwonlydefaults:
            return spec_kwonlydefaults[argname]
        else:
            raise RuntimeError(f"Keyword-only argument '{argname}' doesn't have default value.")
    elif argname in (spec.varargs, spec.varkw):
        raise RuntimeError(f"Argument '{argname}' doesn't have default value.")
    else:
        raise RuntimeError(f"Function '{func.__name__}' doesn't have '{argname}' argument.")

def gloloc():
    """Return dictionary which consists of items from globals() dict shadowed
    by items from locals() dict.
    """
    caller_frame_info = inspect.stack()[1]
    glo = caller_frame_info.frame.f_globals
    loc = caller_frame_info.frame.f_locals
    return {**glo, **loc}

class isaccess:
    """Creates an object, attributes of which say if given name is specjal/private/protected/public
    according to Python convention.
    """
    def __init__(self, name):
        self.special = name.startswith('__') and name.endswith('__')
        self.private = name.startswith('__') and not self.special
        self.protected = name.startswith('_') and not self.private and not self.special
        self.public = not self.special and not self.private and not self.protected

    def __str__(self):
        keys, values = zip(*vars(self).items())
        try:
            return keys[values.index(True)]
        except (ValueError, IndexError):
            # this should never happen
            raise RuntimeError(f"Access of '{name}' cannot be determined") from None
