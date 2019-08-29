import uproot as ur
import numpy as np


class Ntuplizer:
    def __init__(self):
        self.selectors = []
        self.quantities = []

    def register_selector(self, s):
        self.selectors.append(s)

    def register_quantity_module(self, q):
        self.quantities.append(q)

    def convert(self, input_file):
        print('loading file: ' + input_file)
        f = ur.open(input_file)
        e = f['Events']

        n_events = e.__len__()
        n_quantities = 0

        # allocate required values
        values = {}

        for s in self.selectors:
            for key in s.get_keys():
                if key in values:
                    continue
                values[key] = e.array(key)

        for q in self.quantities:
            n_quantities += q.get_size()

            for key in q.get_keys():
                if key in values:
                    continue
                values[key] = e.array(key)

        print('running selector modules')
        # compute selection mask
        mask = np.ones(n_events, dtype=bool)
        for selector in self.selectors:
            mask = np.logical_and(mask, selector.select(values))

        # apply selection mask
        for key, value in values.items():
            values[key] = values[key][mask]

        print('running quantity modules')
        n_events = np.sum(mask)
        result = np.empty(shape=(n_events, n_quantities))
        names = []
        # compute all quantities and add to result
        j = 0
        for q in self.quantities:
            val = q.compute(values, n_events)
            s = q.get_size()
            result[:, j:j + s] = val
            j += s
            names.extend(q.get_names())

        return result, names
