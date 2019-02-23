import miscutils.user.box as box
import json
import ruamel.yaml
from textwrap import dedent

def test_compare():
    data = {'x': 123, 'y': {'z': 234}}
    uut = box.Box(data)

    assert uut == {'x': 123, 'y': {'z': 234}}
    assert not uut != {'x': 123, 'y': {'z': 234}}
    assert not uut == {'x': 321, 'y': {'z': 234}}
    assert uut != {'x': 321, 'y': {'z': 234}}
    assert not uut is {'x': 123, 'y': {'z': 234}}
    assert not uut is data
    assert uut._target is data


def test_delegate():
    data = {'x': 123, 'y': {'z': 234}}
    uut = box.Box(data)

    assert str(uut) == "{'x': 123, 'y': {'z': 234}}"
    assert repr(uut) == "Box({'x': 123, 'y': {'z': 234}})"
    assert len(uut) == 2


def test_subscribe():
    data = {'x': 123, 'y': {'z': 234}}
    uut = box.Box(data)

    assert uut['x'] == 123
    uut['y']['z'] = 432
    assert uut.y.z == 432
    del uut['y']
    assert len(uut) == 1


def test_simple_get():
    data = {'x': 123, 'y': {'z': 234}}
    uut = box.Box(data)

    assert uut.x == 123
    assert uut.y.z == 234
    assert uut['y'].z == 234
    assert uut.y['z'] == 234
    assert uut['y']['z'] == 234
    assert uut.__class__ == box.Box


def test_simple_set():
    data = {'x': 123, 'y': {'z': 234}}
    uut = box.Box(data)

    uut.x = 321
    assert data == {'x': 321, 'y': {'z': 234}}

    uut.y.z = 432
    assert data == {'x': 321, 'y': {'z': 432}}


def test_simple_del():
    data = {'x': 123, 'y': {'z': 234}}
    uut = box.Box(data)

    del uut['y']
    assert data == {'x': 123}


def test_list_get_set_del():
    data = {'x': 123, 'y': [{'z': 234, 'w': [9, 8, {'a': 7, 'b': 6}]}, 345]}
    uut = box.Box(data)

    assert uut.y[0].w[2].b == 6

    uut.y[0].w[2].b = 7
    assert data['y'][0]['w'][2]['b'] == 7

    del uut.y[0].w[2].a
    assert data['y'][0]['w'][2] == {'b': 7}


def test_json():
    data = json.loads('[1,2,3,{"x":5, "y":7}]')
    uut = box.Box(data)

    assert uut[3].y == 7

    uut[3].x = 4
    del uut[1]

    assert json.dumps(data) == '[1, 3, {"x": 4, "y": 7}]'


def test_yaml():

    inp = dedent("""\
    # example
    name:
      # details
      family: Smith   # very common
      given: Alice    # one of the siblings
      children:
        - name: Sue
          age: 12
        - name: John
          age: 10
    """)

    out = dedent("""\
    # example
    name:
      # details
      family: Smith   # very common
      given: Bob      # one of the siblings
      children:
        - name: John
          age: 7
        - 123
    """)


    yaml = ruamel.yaml.YAML()
    buf = ruamel.yaml.compat.StringIO()
    data = yaml.load(inp)
    uut = box.Box(data)
    uut.name.given = 'Bob'

    uut.name.children[1].age = 7
    uut.name.children.append(123)
    del uut.name.children[0]

    yaml.dump(data, buf)
    assert yaml.load(buf.getvalue()) == yaml.load(out)



test_compare()
test_delegate()
test_subscribe()
test_simple_get()
test_simple_set()
test_simple_del()
test_list_get_set_del()
test_json()
test_yaml()
