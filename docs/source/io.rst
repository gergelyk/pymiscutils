io
==

This module provides tools for interacting with input/output of python script.

Functions
---------

**prompt** `(msg, validator=None, default=None, err_msg='Invalid value', input_func=input, error_func=print)`

This function prompts user until proper input is provided.

    `msg` - message to be displayed, can contain ``{default}`` placeholder which will be replaced by `default` argument.

    `validator` - can be one of the following:
         * ``None`` - user's input is not validated at all, it is always accepted.
         * string - user's input is evaluated against regular expression which comes as validator.
         * callable - validator is called with user's input as an argument. Value returned by validator is evaluated as boolean and determines if the input is valid or not. Validator can also raise an exception, which disqualifies user's input as valid.

    `default` - default value. It is returned by prompt function when user's input is empty. This value is not validated by validator, but turned into string by ``str()`` function.

    `err_msg` - message which is displayed when user submits improper input. Can contain ``{default}`` and ``{value}`` placeholders which correspond to default value and last user's value.

    `input_func` - function that is used to display prompt message and read user's input.

    `error_func` - function that is used to display error message.

    Returned value - user's input.


