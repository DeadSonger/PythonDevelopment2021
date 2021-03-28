import tkinter as tk

from draw_widget import DrawWidget
from text_widget import FigureEditer


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.figure = []
        self.create_widgets()

    def create_widgets(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=10)
        self.rowconfigure(1, weight=1)
        self.grid(row=0, column=0, sticky=tk.NSEW)

        self._work_frame = tk.Frame(self)
        self._work_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self._work_frame.columnconfigure(0, weight=1)
        self._work_frame.columnconfigure(1, weight=1)
        self._work_frame.rowconfigure(0, weight=1)

        self._work_frame._text_frame = tk.LabelFrame(self._work_frame, text='Text_label')
        self._work_frame._text_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self._work_frame._text_frame.rowconfigure(0, weight=1)
        self._work_frame._text_frame.columnconfigure(0, weight=1)
        self._work_frame._text_frame._text = FigureEditer(self._work_frame._text_frame, self.figure)
        self._work_frame._text_frame._text.grid(row=0, column=0, sticky=tk.NSEW)

        self._work_frame._drawer = DrawWidget(self._work_frame, self.figure,
                                              self._work_frame._text_frame._text.update_object,
                                              self._work_frame._text_frame._text.update_object)
        self._work_frame._drawer.grid(row=0, column=1, sticky=tk.NSEW)
        self._work_frame._text_frame._text.update_callback = self._work_frame._drawer.redraw

        self._tool_bar = tk.Frame(self)
        self._tool_bar.grid(row=1, column=0, sticky=tk.NSEW)

        self._tool_bar.rowconfigure(0, weight=1)
        for i in range(20):
            self._tool_bar.columnconfigure(i, weight=1)

        self._tool_bar._load = tk.Button(self._tool_bar, text="Load")
        self._tool_bar._load.grid(row=0, column=0, sticky=tk.NSEW)

        self._tool_bar._save = tk.Button(self._tool_bar, text="Save")
        self._tool_bar._save.grid(row=0, column=1, sticky=tk.NSEW)

        self._tool_bar._quit = tk.Button(self._tool_bar, text="Quit", command=self.quit)
        self._tool_bar._quit.grid(row=0, column=19, sticky=tk.NSEW)


if __name__ == '__main__':
    app = Application()
    app.mainloop()
