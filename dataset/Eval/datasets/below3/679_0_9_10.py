# -*- coding: utf-8 -*-
import pickle

load = pickle.load

class Empty:
    pass


    def find_class(self, module, name):
        #TODO: safe unpickle
# class Unpickler(pickle.Unpickler):
        if module.startswith("pytorch_lightning"):
            return Empty
        return super().find_class(module, name)
