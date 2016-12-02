import pytest
from miscutils.config import Config

@pytest.fixture(scope="session")
def cfg():
    cfg = Config()
    cfg.var1 = 123
    cfg.var2 = 456
    return cfg

def test_access_values_index(cfg):
    assert(cfg[0] == 123)
    assert(cfg[1] == 456)

def test_access_values_slice(cfg):
    assert(cfg[0:2] == [123, 456])

def test_access_values_name(cfg):
    assert(cfg['var1'] == 123)
    assert(cfg['var2'] == 456)

def test_access_values_syntax(cfg):
    assert(cfg.var1 == 123)
    assert(cfg.var2 == 456)

def test_access_values_selected(cfg):
    x = list(map(lambda key: cfg[key], ['var1', 'var2']))
    assert(x == [123, 456])

def test_access_values_all(cfg):
    x = cfg[:]
    assert(x == [123, 456])

def test_access_keys_all_list_compr(cfg):
    x = [x for x in cfg]
    assert(x == ['var1', 'var2'])

def test_access_keys_all_list_init(cfg):
    x = list(cfg)
    assert(x == ['var1', 'var2'])

def test_access_keys_all_tuple(cfg):
    x = tuple(cfg)
    assert(x == ('var1', 'var2'))

def test_access_keys_all_set(cfg):
    x = set(cfg)
    assert(x == {'var1', 'var2'})

def test_access_items(cfg):
    x = {x: cfg[x] for x in cfg}
    assert(x == {'var1': 123, 'var2': 456})

def test_len(cfg):
    assert(len(cfg) == 2)

def test_str(cfg):
    assert(str(cfg) == "OrderedDict([('var1', 123), ('var2', 456)])")

def test_repr(cfg):
    assert(repr(cfg) == "OrderedDict([('var1', 123), ('var2', 456)])")



