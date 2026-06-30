# encoding: utf-8
import tkinter as tk
import tkinter.ttk as ttk

from pygubu.widgets.tkscrollbarhelper import ScrollbarHelperBase


class TTKScrollbarHelperFactory(type):
    def __new__(cls, clsname, superclasses, attrs):
        return type.__new__(cls, str(clsname), superclasses, attrs)



