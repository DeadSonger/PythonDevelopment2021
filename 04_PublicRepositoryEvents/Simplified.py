import tkinter as tk
import re


class WidgetsTreeNode:
    def __init__(self, widget_master, widget_type, grid_info, **kwargs):

        parsed_grid_info = re.match(
            r'(?P<r>\d+)(?:\.(?P<rw>\d+))?(?:\+(?P<h>\d+))?:'
            r'(?P<c>\d+)(?:\.(?P<cw>\d+))?(?:\+(?P<w>\d+))?(?:/(?P<s>[NWES]+))?',
            grid_info
        ).groupdict()

        row = int(parsed_grid_info['r'])
        col = int(parsed_grid_info['c'])
        row_w = int(parsed_grid_info['rw'] or 1)
        col_w = int(parsed_grid_info['cw'] or 1)
        width = int(parsed_grid_info['w'] or 0) + 1
        height = int(parsed_grid_info['h'] or 0) + 1
        sticky = parsed_grid_info['s'] or 'NEWS'

        self.__master = widget_master
        self.__master.rowconfigure(row, weight=row_w)
        self.__master.columnconfigure(col, weight=col_w)

        self.__widget = widget_type(self.__master, **kwargs)
        self.__widget.grid(row=row, column=col, sticky=sticky, rowspan=height, columnspan=width)
        self.__childs = {}

    def __getattr__(self, item):
        if item in self.__childs:
            return self.__childs[item]
        ret = getattr(self.__widget, item, None)
        if ret:
            return ret

        def wrapper(widget_type, grid_info, **kwargs):
            self.__childs[item] = WidgetsTreeNode(self.__widget, widget_type, grid_info, **kwargs)

        return wrapper


class Application(tk.Frame):
    def __init__(self, master=None, title=None):
        super().__init__(master)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.grid(sticky=tk.NSEW)

        self._widgets_tree = {}
        self.createWidgets()
        if title:
            self.master.title(title)

    def createWidgets(self):
        pass

    def __getattr__(self, item):
        if item in self._widgets_tree:
            return self._widgets_tree[item]

        def wrapper(widget_type, grid_info, **kwargs):
            self._widgets_tree[item] = WidgetsTreeNode(self, widget_type, grid_info, **kwargs)

        return wrapper
