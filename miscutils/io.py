import re

def prompt(msg, validator=None, default=None, err_msg='Invalid value', input_func=input, error_func=print):
    """This function prompts user until proper input is provided.
       msg - message to be displayed, can contain {default} placeholder which will be replaced by 'default' argument
       validator - can be one of the following:
             * None - user's input is not validated at all, it is always accepted
             * string - user's input is evaluated against regular expression which comes as validator
             * callable - validator is called with user's input as an argument; value returned by validator
                          is evaluated as boolean and determines if the input is valid or not; validator can
                          also raise an exception, which disqualifies user's input as valid
       default - default value; it is returned by prompt function when user's input is empty; this value is
             not validated by validator, but turned into string by str() function
       err_msg - message which is displayed when user submits improper input; can contain {default} and {value}
             placeholders which correspond to default value and last user's value     
       input_func - function that is used to display prompt message and read user's input
       error_func - function that is used to display error message
    """

    msg_formated = msg.format(default=default)

    while True:            
        try:
            value = input_func(msg_formated)
            if default != None and value == '':
                value = str(default)
                break
            elif validator == None:
                break
            elif isinstance(validator, str):
                if re.match(validator, value):
                    break
            else:
                if validator(value):
                    break
            
        except Exception as e:
            error_func(str(e))

        err_msg_formated = err_msg.format(default=default, value=value)
        error_func(err_msg_formated)

    return value

