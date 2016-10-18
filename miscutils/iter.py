
class isfirst:
    """Iterates through items of collection returning subsequent elements and flag which tells if given element is first."""
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
    """Iterates through items of collection returning subsequent elements and flag which tells if given element is last."""
    def __init__(self, collection):
        self.collection = collection

    def __len__(self): 
        return len(self.collection)

    def __iter__(self):
        indices_rev = range(len(self.collection))[::-1]
        for collection, index_rev in zip(self.collection, indices_rev):
            yield (collection, index_rev==0)

class isfirstlast:
    """Iterates through items of collection returning subsequent elements and flag which tells if given element is first/last."""
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

