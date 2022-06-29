class Store():
    def __init__(self, store):
        self.store = store
        self.discs = []

    def __eq__(self, storeName):
        if (storeName == self.store):
            return True
        else:
            return False

def split_discs_in_stores(discs):
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
    return stores