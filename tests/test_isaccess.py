from miscutils.insp import isaccess

def test_special():
    name = '__foobar__'
    assert isaccess(name).special == True
    assert isaccess(name).private == False
    assert isaccess(name).protected == False
    assert isaccess(name).public == False
    assert str(isaccess(name)) == 'special'

def test_private():
    name = '__foobar'
    assert isaccess(name).special == False
    assert isaccess(name).private == True
    assert isaccess(name).protected == False
    assert isaccess(name).public == False
    assert str(isaccess(name)) == 'private'

def test_protected():
    name = '_foobar'
    assert isaccess(name).special == False
    assert isaccess(name).private == False
    assert isaccess(name).protected == True
    assert isaccess(name).public == False
    assert str(isaccess(name)) == 'protected'

def test_public():
    name = 'foobar'
    assert isaccess(name).special == False
    assert isaccess(name).private == False
    assert isaccess(name).protected == False
    assert isaccess(name).public == True
    assert str(isaccess(name)) == 'public'

