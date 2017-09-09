from miscutils.str import lsub, rsub

def test_lsub_no_match():
    assert lsub("abcdef", "xyz") == "abcdef"

def test_lsub_old_str_new_empty():
    assert lsub("abcdef", "abc") == "def"

def test_lsub_old_str_new_str():
    assert lsub("abcdef", "abc", "123") == "123def"

def test_lsub_old_empty_new_empty():
    assert lsub("abcdef", "") == "abcdef"

def test_lsub_old_empty_new_str():
    assert lsub("abcdef", "", "123") == "123abcdef"

def test_rsub_no_match():
    assert rsub("abcdef", "xyz") == "abcdef"

def test_rsub_old_str_new_empty():
    assert rsub("abcdef", "def") == "abc"

def test_rsub_old_str_new_str():
    assert rsub("abcdef", "def", "123") == "abc123"

def test_rsub_old_empty_new_empty():
    assert rsub("abcdef", "") == "abcdef"

def test_rsub_old_empty_new_str():
    assert rsub("abcdef", "", "123") == "abcdef123"
