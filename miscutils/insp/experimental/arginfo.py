import inspect
from types import SimpleNamespace
from functools import wraps
from miscutils.insp import getdefault

class ArgInfo():
    """ Object of this class can be used as a decorator and also as an
    interface providing info about the args of decorated function.
    """

    _wrapper_ids = []

    @staticmethod
    def _find_argsprops():
        stack = inspect.stack()

        # level=0 is current frame,
        #       1 is the calling method,
        #       2 is wrapped func,
        #       3 is the first decorator
        for level in range(3, len(stack)):
            wrapper_frame = stack[level].frame
            if id(wrapper_frame.f_code) in ArgInfo._wrapper_ids:
                break
        else:
            raise RuntimeError("@arginfo decorator doesn't seem to be used.")

        return  wrapper_frame.f_locals['argsprops']

    def __getattr__(self, name):
        return ArgInfo._find_argsprops()[name]

    __getitem__ = __getattr__

    def __contains__(self, name):
        return name in ArgInfo._find_argsprops()

    def __iter__(self):
        yield from ArgInfo._find_argsprops()

    @staticmethod
    def __call__(func):

        class Argument(SimpleNamespace): pass

        spec = inspect.getfullargspec(func)

        @wraps(func)
        def wrapper(*args, **kwargs):

            # Get argnames
            argnames = set(spec.args + spec.kwonlyargs + list(kwargs))

            # Get defvals
            defvals = {}
            for argname in argnames:
                try:
                    val = getdefault(func, argname)
                    defvals[argname] = val
                except:
                    pass

            # Get argsset
            args_set = spec.args[:len(args)]
            kwargs_set = set(kwargs)
            argsset = {*args_set, *kwargs_set}

            # Get argvals
            argvals = defvals.copy()
            argvals.update( {argname: argval for argname, argval in zip(args_set, args) } )
            argvals.update(kwargs)

            # Combine everything in argprops
            def argprops(argname):
                props = Argument(isset = argname in argsset,
                                 value = argvals[argname])

                if argname in defvals:
                    props.defval = defvals[argname]

                return props

            argsprops = {argname: argprops(argname) for argname in argnames}

            return func(*args, **kwargs)

        ArgInfo._wrapper_ids.append(id(wrapper.__code__))

        return wrapper

arginfo = ArgInfo()


