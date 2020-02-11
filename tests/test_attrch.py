import pytest
from unittest.mock import call
from miscutils.dbg import attrch

@pytest.fixture()
def action(mocker):
    mock = mocker.MagicMock()
    def action(name, value):
        mock(name, value)
    action.mock = mock
    return action

def test_any_attribute_change(action):

        @attrch(action=action)
        class Foo:
            pass

        foo = Foo()
        foo.x = 123
        foo.xy = 123
        foo.xyz = 10

        expected_calls = [
            call('x', 123),
            call('xy', 123),
            call('xyz', 10)]

        assert action.mock.mock_calls == expected_calls

def test_any_change_to_10_and_changes_of_attributes_with_names_of_two_letters(action):

        @attrch(value=10, action=action)
        @attrch('..', action=action)
        class Foo:
            pass

        foo = Foo()
        foo.x = 123
        foo.xy = 123
        foo.xyz = 10

        expected_calls = [
            call('xy', 123),
            call('xyz', 10)]

        assert action.mock.mock_calls == expected_calls

def test_changes_of_attributes_with_names_of_two_letters(action):

        @attrch('..', action=action)
        class Foo:
            pass

        foo = Foo()
        foo.x = 123
        foo.xy = 123
        foo.xyz = 10

        expected_calls = [
            call('xy', 123)]

        assert action.mock.mock_calls == expected_calls

def test_attach_to_metaclass(action):

        class M(type): pass
        class Foo(metaclass=M):
            pass

        attrch('..', action=action)(type(Foo))

        Foo.x = 123
        Foo.xy = 123
        Foo.xyz = 123

        expected_calls = [
            call('xy', 123)]

        assert action.mock.mock_calls == expected_calls

def test_attach_to_metaclass_with_inheritance(action):

        class Foo():
            pass

        class M(type): pass
        attrch('..', action=action)(M)
        class Foo(Foo, metaclass=M): pass

        Foo.x = 123
        Foo.xy = 123
        Foo.xyz = 123

        expected_calls = [
            call('xy', 123)]

        assert action.mock.mock_calls == expected_calls

def test_attach_to_existing_metaclass_automatically(action):

        class M(type): pass

        @attrch('..', action=action, meta=True)
        class Foo(metaclass=M):
            pass

        Foo.x = 123
        Foo.xy = 123
        Foo.xyz = 123

        expected_calls = [
            call('xy', 123)]

        assert action.mock.mock_calls == expected_calls

def test_attach_to_non_existing_metaclass_automatically(action):

        @attrch('..', action=action, meta=True)
        class Foo:
            pass

        Foo.x = 123
        Foo.xy = 123
        Foo.xyz = 123

        expected_calls = [
            call('xy', 123)]

        assert action.mock.mock_calls == expected_calls







