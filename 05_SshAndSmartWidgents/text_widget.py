import tkinter as tk

from figure import parse


class FigureEditer(tk.Text):

    def __init__(self, master, figures, update_callback=None, **kw):
        super().__init__(master, **kw)
        self.figures = figures
        self.map = {}
        self.reverse_map = []
        self.update_callback = update_callback
        self.bind('<KeyRelease>', self.check_text)
        self.tag_config('wrong', background='red', foreground='white')

    def update_object(self, idx):
        if idx >= len(self.reverse_map):
            line = int(self.index(tk.END).split('.')[0]) - 1
            line_text = self.get(f'{line}.0', f'{line}.end')
            if line_text:
                self.insert(f'{line}.end', '\n')
                line += 1
            self.map[line-1] = self.figures[idx]
            self.insert(f'{line}.0', self.figures[idx].to_str() + '\n')
            self.reverse_map.append(line)
        else:
            line = self.reverse_map[idx]
            line_text = self.get(f'{line}.0', f'{line}.end')
            if line_text and line_text[-1] != '\n':
                self.insert(f'{line}.end', '\n')
            self.replace(f'{line}.0', f'{line+1}.0', self.figures[idx].to_str())

    def check_text(self, event):
        text = self.get("insert linestart", "insert lineend")
        objects = parse(text)

        if objects and objects[0][1] is None:
            self.tag_add('wrong', "insert linestart", "insert lineend")
        elif objects:
            self.tag_remove('wrong', "insert linestart", "insert lineend")

        self.map.clear()
        for i, fig in parse(self.get('1.0', tk.END)):
            if fig:
                self.map[i] = fig

        self.figures.clear()
        self.reverse_map.clear()
        for line_n, fig in sorted(self.map.items()):
            self.reverse_map.append(line_n + 1)
            if fig:
                self.figures.append(fig)
        self.update_callback()
