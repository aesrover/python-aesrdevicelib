class Transducer:
    """ A transducer framework class. """
    def __init__(self, atype, itype=None, **other):
        self.id_data: dict = {'atype': atype, 'itype': itype}
        self.id_data.update(other)

    def _add_transducer_info(self, data):
        d = dict(self.id_data)
        d['param'] = data
        return d

    def read(self):
        raise NotImplementedError("Method `read_transducer` not implemented by: {}".format(self))

    def read_full(self):
        return self._add_transducer_info(self.read())


class BasicTransducer(Transducer):
    """ A basic transducer sub-class that takes a read function as input. """
    def __init__(self, func: callable, atype, itype=None, **other):
        super().__init__(atype, itype, **other)
        self.read_transducer = func

    def read(self):
        return self.read_transducer()
