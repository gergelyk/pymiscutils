
class index:
    """Iterates through items of collection returning subsequent elements and together with their indices.

    Example:

        >>> for x, idx in index(range(7,2,-1)):
        ...     print(x, idx)
        7 0
        6 1
        5 2
        4 3
        3 4
    """
    def __init__(self, collection):
        self.collection = collection

    def __len__(self): 
        return len(self.collection)

    def __iter__(self):
        for collection, idx in zip(self.collection, range(len(self.collection))):
            yield (collection, idx)

class isfirst:
    """Iterates through items of collection returning subsequent elements and flag which tells if given element is first.

    Examples:

        >>> for x, first in isfirst(range(5)):
        ...     print(x, first)
        0 True
        1 False
        2 False
        3 False
        4 False

        >>> for (x, first), last in islast(isfirst(range(5))):
        ...     print(x, first, last)
        0 True False
        1 False False
        2 False False
        3 False False
        4 False True

    """
    def __init__(self, collection):
        self.collection = collection

    def __len__(self): 
        return len(self.collection)

    def __iter__(self):
        first = True
        for collection in self.collection:
            yield (collection, first)
            first = False
            
class islast:
    """Iterates through items of collection returning subsequent elements and flag which tells if given element is last.

    Examples:

        >>> for x, last in islast(range(5)):
        ...     print(x, last)
        0 False
        1 False
        2 False
        3 False
        4 True

        >>> for (x, first), last in islast(isfirst(range(5))):
        ...     print(x, first, last)
        0 True False
        1 False False
        2 False False
        3 False False
        4 False True

    """
    def __init__(self, collection):
        self.collection = collection

    def __len__(self): 
        return len(self.collection)

    def __iter__(self):
        indices_rev = range(len(self.collection))[::-1]
        for collection, index_rev in zip(self.collection, indices_rev):
            yield (collection, index_rev==0)

class isfirstlast:
    """Iterates through items of collection returning subsequent elements and flag which tells if given element is first/last.

    Example:

        >>> for x, first, last in isfirstlast(range(5)):
        ...     print(x, first, last)
        0 True False
        1 False False
        2 False False
        3 False False
        4 False True
    """
    def __init__(self, collection):
        self.collection = collection

    def __len__(self): 
        return len(self.collection)

    def __iter__(self):
        first = True
        indices_rev = range(len(self.collection))[::-1]
        for collection, index_rev in zip(self.collection, indices_rev):
            yield (collection, first, index_rev==0)
            first = False

