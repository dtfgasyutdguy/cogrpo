# -*- coding: utf-8 -*-
import pickle

load = pickle.load

class Empty:
    pass


    def find_class(self, module, name):
# class Unpickler(pickle.Unpickler):
        #TODO: safe unpickle
        if module.startswith("pytorch_lightning"):
            return Empty
        return super().find_class(module, name)
