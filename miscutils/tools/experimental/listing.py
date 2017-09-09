import inspect
import sys
import os
import traceback
from pprint import pformat

def execute(code, glo, loc):
    try:
        cell = eval(code, glo, loc)
        error = False
    except SyntaxError:
        error = True

    if error:
        exec(code, glo, loc)
        cell = None

    return cell

def print_code(code):
    lines = [line for line in code.splitlines() if line.strip()]
    for line in lines:
        if line[:1] in ' \t':
            print('...', line)
        else:
            print('>>>', line)

def print_cell(cell, cell_width, cell_height, compact):
    cell_height = max(cell_height, 3)
    text = pformat(cell, width=cell_width, compact=compact)
    lines = text.splitlines()

    if len(lines) > cell_height:
        lines = lines[:cell_height-2] + [' ...'] + lines[-1:]

    print('\n'.join(lines))

def read_code(filename, silent_until, verbose_from):
    # silent_until, verbose_from numbers lines from 1

    with open(filename) as f:
        text = f.read()

    silent_lines = text.splitlines()[:silent_until-1]
    silent_code = '\n'.join(silent_lines).strip()

    verbose_lines = text.splitlines()[verbose_from-1:]
    verbose_code = '\n'.join(verbose_lines).strip()

    return silent_code, verbose_code

def listing_here(cell_width=80, cell_height=10, compact=True):
    """Print listing considering everything before the line where this function is called as silent code
    and everything after the line where this function is called as verbose code.
    """
    frame = inspect.stack()[-1]
    # frame.lineno numbers lines from 1
    silent_code, verbose_code = read_code(frame.filename, frame.lineno, frame.lineno+1)
    listing(silent_code, verbose_code, cell_width, cell_height, compact)

def listing_file(filename, first_line=1, cell_width=80, cell_height=10, compact=True):
    """Print listing of the code in the file specified by filename. first_line defines the first
    line of verbose code. Everything above is considered as silent code.
    """
    # first_line numbers lines from 1
    silent_code, verbose_code = read_code(filename, first_line, first_line)
    listing(silent_code, verbose_code, cell_width, cell_height, compact)

def listing(silent_code, verbose_code, cell_width=80, cell_height=10, compact=True):
    """First silently executes code provided in silent_code. Then executes code provided in verbose_code
    printing listing at the same time.
    """
    verbose_lines = verbose_code.splitlines()
    glo = {}
    loc = {}
    buf = verbose_lines[:1] # Initialize with the firs line.

    # Execute silent code.
    exec(silent_code, glo, loc)

    # If there is anything to execute, add a dummy line which will trigger execution of the last
    # block of code. Dummy line will never be executed.
    if verbose_lines:
        verbose_lines = verbose_lines[1:] + ['dummy']

    for line in verbose_lines:
        if line[:1] not in ' \t':
            code_block = '\n'.join(buf)
            print_code(code_block)
            cell = execute(code_block, glo, loc)
            if cell != None:
                print_cell(cell, cell_width, cell_height, compact)
            buf.clear()

        buf.append(line)

    exit(0)

def main():
    try:
        defaults = ['', 1, 80, 10, True]
        args = sys.argv[1:] + defaults[len(sys.argv)-1:]
        filename, first_line, cell_width, cell_height, compact = args
        first_line = int(first_line)
        cell_width = int(cell_width)
        cell_height = int(cell_height)
        compact = compact!='False'
        listing_file(filename, first_line, cell_width, cell_height, compact)
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        if len(traceback.extract_tb(exc_tb)) >= 4:
            traceback.print_exc()
        else:
            sys.stderr.write(str(ex))
            sys.stderr.flush()
            print()
        print()
        print('pylisting - executes selected script in python interpreter and prints listing of the code together wiht the partial results.')
        print()
        print('Syntax: pylisting filename [first_line=1 [cell_width=80 [cell_height=10 [compact=True]]]]')        

if __name__=='__main__':
    main()

# Known issues:
#
# __file__ in eval()/exec() becames undefined
#
# Arrays defined in multiple lines which start from beginning of the line raise an exception. Ex.
# a = [
# 1,
# 2,
# 3,
# ]
#


