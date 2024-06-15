class Store():
    """Store with discs"""
    def __init__(self, store):
        self.store = store
        self.discs = []

    def __eq__(self, store):
        if store == self.store:
            return True
        return False

def split_discs_in_stores(discs, max_no_discs=None):
    """Split discs into different stores"""
    stores = []

    for disc in discs:
        # Same store, append
        if disc.store in stores:
            index = stores.index(disc.store)
            stores[index].discs.append(disc)
        # New store
        else:
            store = Store(disc.store)
            store.discs.append(disc)
            stores.append(store)

    if max_no_discs is not None:
        for store in stores:
            if len(store.discs) > max_no_discs:
                store.discs = store.discs[:max_no_discs]
    return stores
