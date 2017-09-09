import subprocess

def shell(cmd, *args, **kwargs):
    """ Executes cmd in underlying shell. Returns stdout split in lines.
        If return code is not equal 0, subprocess.CalledProcessError exception is raised.
    """
    cmd = cmd.format(*args, **kwargs)
    ret = subprocess.check_output(cmd, shell=True)[:-1].decode()
    if ret:
        lines = ret.split('\n')
    else:
        lines = []
    return [line.rstrip('\r') for line in lines]
