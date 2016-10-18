from miscutils.iter import isfirst, islast, isfirstlast

for x, first in isfirst(range(5)):
    print(x, first)
    
for x, last in islast(range(5)):
    print(x, last)

for (x, first), last in islast(isfirst(range(5))):
    print(x, first, last)

for x, first, last in isfirstlast(range(5)):
    print(x, first, last)
