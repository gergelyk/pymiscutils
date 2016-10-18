from miscutils.io import prompt

def input_func(data):
    def test_input_gen(data):
        buf = []
        for item in data:
            ret = yield item
            buf.append(ret)
        yield buf[:-1]

    gen = test_input_gen([None] + data)
    gen.send(None)

    def func(inp=None):
        return gen.send(inp)

    return func


def output_func():
    def test_output_gen():
        buf = []
        while True:
            ret = yield buf[:-1]
            buf.append(ret)

    gen = test_output_gen()
    gen.send(None)

    def func(inp=None):
        return gen.send(inp)

    return func


def test_no_validation():
    test_input = input_func(['abc'])
    test_output = output_func()

    name = prompt(msg='Name: ',
                  input_func=test_input,
                  error_func=test_output)

    assert(name == 'abc')
    assert(test_input() == ['Name: '])
    assert(test_output() == [])


def test_integer():
    test_input = input_func(['abc', '123'])
    test_output = output_func()

    name = prompt(msg='Name: ',
                  validator=int,
                  input_func=test_input,
                  error_func=test_output)

    tinp = test_input()
    tout = test_output()
    assert(name == '123')
    assert(tinp == ['Name: ']*2)
    assert(tout == ["invalid literal for int() with base 10: 'abc'", 'Invalid value'])


def test_length_must_be_3():
    test_input = input_func(['abcd', 'g', 'xyz'])
    test_output = output_func()

    name = prompt(msg='Name: ',
                  validator=lambda x: len(x)==3,
                  input_func=test_input,
                  error_func=test_output)

    tinp = test_input()
    tout = test_output()
    assert(name == 'xyz')
    assert(tinp == ['Name: ']*3)
    assert(tout == ['Invalid value']*2)


def test_only_letters_allowed():
    test_input = input_func(['abc3', '_abc', 'xyz'])
    test_output = output_func()

    name = prompt(msg='Name: ',
                  validator='[a-zA-Z]*$',
                  input_func=test_input,
                  error_func=test_output)

    tinp = test_input()
    tout = test_output()
    assert(name == 'xyz')
    assert(tinp == ['Name: ']*3)
    assert(tout == ['Invalid value']*2)


def test_formating_and_default():
    test_input = input_func(['maybe', ''])
    test_output = output_func()

    name = prompt(msg='Name [yn](default={default}): ',
                  validator='[yYnN]',
                  default='n',
                  err_msg='{value} is not acceptable, yes or no?',
                  input_func=test_input,
                  error_func=test_output)

    tinp = test_input()
    tout = test_output()
    assert(name == 'n')
    assert(tinp == ['Name [yn](default=n): ']*2)
    assert(tout == ['maybe is not acceptable, yes or no?'])


