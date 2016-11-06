from IPython.core.magic import Magics, magics_class, line_magic
from pprint import pprint

@magics_class
class MyMagics(Magics):

    _with_log = []
    _with_stack = []
    
    @line_magic
    def enter(self, line):
        """Open context.
        
        Usage:
          %enter object
          
        Calls __enter__ on the object given as an argument. Returns value returned by __enter__. Object is put on stack.
        
        See also: %exit, %with_log, %with_clear
        """
        
        obj = self.shell.ev(line)
        ret = obj.__enter__()
        self._with_log.append(line)
        self._with_stack.append(obj)
        print('Item appended. Current with_stack:')
        self.print_with_stack()
        return ret
    
    @line_magic
    def exit(self, line):
        """Close context.
        
        Usage:
          %exit [index=-1] [type] [value] [tb]  
          
        Calls __exit__(type, value, tb) on the object from the stack. Object is removed from the stack.
        Index on the stack can be overwritten. Default is -1 which corresponds the the last item on the stack.
        type, value, tb are arguments that are passed to __exit__. Default values are 'None'.
        
        See also: %enter, %with_log, %with_clear
        """
        
        if not self._with_log:
            print('with_stack empty.')
            return
            
        if not line:
            line = '-1'
            
        line += ' None None None _'
        index_, type_, value_, tb_, _ = line.split(' ', 4)
        index = self.shell.ev(index_)
        type  = self.shell.ev(type_)
        value = self.shell.ev(value_)
        tb    = self.shell.ev(tb_)
        
        self._with_stack[index].__exit__(type, value, tb)
        self._with_stack.pop(index)
        self._with_log.pop(index)
        print('Item popped. Current with_stack:')
        self.print_with_stack()
        
    @line_magic
    def with_stack(self, line):
        """Disply stack of %enter/%exit commands.
        
        Usage:
          %with_stack
        
        See also: %enter, %exit, %with_clear
        """
        print('Current with_stack:')
        self.print_with_stack()
    
    @line_magic
    def with_clear(self, line):
        """Clears stack of %enter/%exit commands.
        
        Usage:
          %with_clear
        
        See also: %enter, %exit, %with_stack
        """
        self._with_log.clear()
        self._with_stack.clear()
        print('with_stack cleared.')
    
    def print_with_stack(self):
        if self._with_log:
            for i in range(len(self._with_log)):
                print('{}: {}'.format(i, self._with_log[i]))
        else:
            print('(empty)')
ip = get_ipython()
ip.register_magics(MyMagics)

