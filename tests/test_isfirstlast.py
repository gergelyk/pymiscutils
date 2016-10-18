from miscutils.iter import isfirst, islast, isfirstlast

def test_isfirst():
    result = ''
    reference = '10000'

    for x, first in isfirst(range(5)):
        result += '1' if first else '0'

    assert(result == reference)
    
def test_islast():
    result = ''
    reference = '00001'

    for x, last in islast(range(5)):
        result += '1' if last else '0'

    assert(result == reference)

def test_isfirstlast():
    result_first = ''
    result_last  = ''
    reference_first = '10000'
    reference_last  = '00001'

    for x, first, last in isfirstlast(range(5)):
        result_first += '1' if first else '0'
        result_last  += '1' if last  else '0'

    assert(result_first == reference_first)
    assert(result_last  == reference_last)

