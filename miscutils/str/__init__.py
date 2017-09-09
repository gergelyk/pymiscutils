def lsub(string, old, new=''):
    """If `string` starts with `old` replace `old` with `new`. Return result."""
    if string.startswith(old):
        return new + string[len(old):]
    else:
        return string

def rsub(string, old, new=''):
    """If `string` ends with `old` replace `old` with `new`. Return result."""
    if old:
        if string.endswith(old):
            return string[:-len(old)] + new
        else:
            return string
    else:
        return string + new
