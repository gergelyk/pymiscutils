from inspect import signature, Parameter, _empty
from functools import wraps
from pytest import raises

class _ArgEmpty: pass
class _ArgDefault: pass

_arg_empty = _ArgEmpty()
_arg_default = _ArgDefault()

def permisive(func):
    """Relax function signature.

    * Wrapped function behaves like all the ars were of POSITIONAL_OR_KEYWORD type, e.g.:
        func = lambda x, /, y, *, z: x * y + z
        5 == permisive(func)(1, 2, 3)
        5 == permisive(func)(z=3, y=1, x=2)
        7 == permisive(func)(3, 1, y=2)

    * Arg of VAR_POSITIONAL type can be set using corresponding keyword, e.g.:
        e.g.
        func = lambda x, *ar: x * sum(ar)
        45 == permisive(func)(3, ar=(4, 5, 6))

    * Arg of VAR_KEYWORD can be set using corresponding keyword, e.g.:
        e.g.
        func = lambda x, **kw: x * sum(kw.values())
        assert 45 == permisive(func)(3, kw=dict(a=4, b=5, c=6))

    * Unnecessary args and kwargs are left unused, e.g.:
        e.g.
        func = lambda x, /, y, *, z: x * y + z
        assert 5 == permisive(func)(1, 2, 3, 4, 5) == 5
        assert 5 == permisive(func)(z=3, b=200, y=1, x=2, a=100) == 5

    * This also plays well with default values, e.g.:
        func = lambda x=10, /, y=20, *, z=30: x * y + z
        assert  32 == permisive(func)(1, 2)
        assert  13 == permisive(func)(z=3, y=1)
        assert 230 == permisive(func)()
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        params = signature(func).parameters.values()
        p_names = [p.name for p in params]
        p_kinds = [p.kind for p in params]
        remaining_args = list(args)
        remaining_kwargs = kwargs.copy()

        pos_arg_types = (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD)
        args_count = sum(p_kinds.count(arg_type) for arg_type in pos_arg_types)
        dst_args = [_arg_empty] * args_count
        dst_kwargs = {}

        # Populate default values
        for p_index, param in zip(range(args_count), params):
            if param.default is not _empty:
                dst_args[p_index] = _arg_default

        # Populate dst_args from kwargs
        pos_arg_names = [p.name for p in params if p.kind in pos_arg_types]
        for param_name in pos_arg_names:
            if param_name in remaining_kwargs:
                p_index = p_names.index(param_name)
                dst_args[p_index] = remaining_kwargs.pop(param_name)

        # Populate dst_args from args
        for p_index, alloc in enumerate(dst_args):
            if alloc in (_arg_empty, _arg_default):
                if remaining_args:
                    dst_args[p_index] = remaining_args.pop(0)
                else:
                    break

        if _arg_empty in dst_args:
            # An exception will be raised later as we don't populate all dst_args
            dst_args = dst_args[:dst_args.index(_arg_empty)]
        else:

            # Copy default values wherever applicable
            for p_index, (alloc, param) in enumerate(zip(dst_args, params)):
                if alloc is _arg_default:
                    dst_args[p_index] = param.default

            # Set var_positionals
            try:
                var_positional_name = p_names[p_kinds.index(Parameter.VAR_POSITIONAL)]
            except ValueError:
                pass # no var_positionals defined
            else:
                if var_positional_name in remaining_kwargs:
                    dst_args.extend(remaining_kwargs.pop(var_positional_name))
                else:
                    dst_args.extend(remaining_args)
                    remaining_args = ()

        # Set var_keyword
        try:
            var_keyword_name = p_names[p_kinds.index(Parameter.VAR_KEYWORD)]
        except ValueError:
            pass # no var_keyword defined
        else:
            if var_keyword_name in remaining_kwargs:
                dst_kwargs.update(remaining_kwargs.pop(var_keyword_name))

        # Populate dst_kwargs
        kw_arg_names = [p.name for p in params if p.kind is Parameter.KEYWORD_ONLY]
        for p_name in kw_arg_names:
            if p_name in remaining_kwargs:
                dst_kwargs[p_name] = remaining_kwargs.pop(p_name)
            elif remaining_args:
                dst_kwargs[p_name] = remaining_args.pop(0)

        # Unused args and kwargs: remaining_args, remaining_kwargs

        return func(*dst_args, **dst_kwargs)
    return wrapper



