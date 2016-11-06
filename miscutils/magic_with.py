from IPython import get_ipython
from IPython.core.magic import Magics, magics_class, line_magic
from pprint import pprint

#TODO: stack could be cleared at %reset magic

@magics_class
class MagicContextManager(Magics):

    _with_log = []
    _with_stack = []
    
    @line_magic
    def with_enter(self, line):
        """Open context.
        
        Usage:
          %with_enter object
          
        Calls __enter__ on the object given as an argument. Returns value returned by __enter__. Object is put on stack.
        
        See also: %with_exit, %with_show, %with_clear, %with_get
        """
        
        obj = self.shell.ev(line)
        ret = obj.__enter__()
        self._with_log.append(line)
        self._with_stack.append(obj)
        print('Item appended. Current stack:')
        self.print_with_stack()
        return ret
    
    @line_magic
    def with_exit(self, line):
        """Close context.
        
        Usage:
          %with_exit [index=-1, [type=None, [value=None, [tb=None]]]]
          
        Calls __exit__(type, value, tb) on the object from the stack. Object is removed from the stack.
        Index on the stack can be provided. Default is -1 which corresponds the the last item on the stack.
        type, value, tb are arguments that are passed to __exit__.
        
        See also: %with_enter, %with_show, %with_clear, %with_get
        """
        
        if not self._with_log:
            print('Stack empty.')
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
        print('Item popped. Current stack:')
        self.print_with_stack()
        
    @line_magic
    def with_show(self, line):
        """Disply stack of %with_enter/%with_exit commands.
        
        Usage:
          %with_show
        
        See also: %with_enter, %exit, %with_clear, %with_get
        """
        print('Current stack:')
        self.print_with_stack()
    
    @line_magic
    def with_clear(self, line):
        """Clears stack of %with_enter/%with_exit commands.
        
        Usage:
          %with_clear
        
        See also: %with_enter, %with_exit, %with_show, %with_get
        """
        self._with_log.clear()
        self._with_stack.clear()
        print('Stack cleared.')
            
    @line_magic
    def with_get(self, line):
        """Returns object from stack of %with_enter/%with_exit commands.
        
        Usage:
          %with_get [index=-1]
        
        Index on the stack can be provided. Default is -1 which corresponds the the last item on the stack.

        See also: %with_enter, %with_exit, %with_show, %with_clear
        """
        if not self._with_log:
            print('Stack empty.')
            return
            
        if not line:
            line = '-1'

        index_ = line
        index = self.shell.ev(index_)
        return self._with_stack[index]
    
    def print_with_stack(self):
        if self._with_log:
            for i in range(len(self._with_log)):
                print('{}: {}'.format(i, self._with_log[i]))
        else:
            print('(empty)')
            
            
ip = get_ipython()
ip.register_magics(MagicContextManager)

