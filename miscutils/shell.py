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
    return lines

def copy_dir(src, dst):
    """ Copies src directory recursively on place of dst. If dst already exists, it will be removed first.
        This function uses following commands of Unix shell: rm, cp
    """
    shell("rm -fr {}", dst)
    shell("cp -r {} {}", src, dst)

def repl_in_paths(text, repl, top_dir='.'):
    """ Scans top_dir recursively to find given text in file/dir names. Then replaces this text by repl.
        This function uses following commands of Unix shell: find, mv
    """
    while True:
        to_rename = shell("find {} -name '*{}*' | head -n 1", top_dir, text)
        if not to_rename:
            break
        to_rename = to_rename[0]
        renamed = to_rename.replace(text, repl)
        shell("mv {} {}", to_rename, renamed)

def repl_in_files(text, repl, top_dir='.'):
    """ Scans top_dir recursively to find given text in the content of files. Then replaces this text by repl.
        This function uses following commands of Unix shell: grep, sed
    """
    to_modify = shell("grep -r {} {} | grep -o '^[^:]*'", text, top_dir)
    for file_path in to_modify:
        shell("sed -i 's/{}/{}/' {}", text, repl, file_path)

