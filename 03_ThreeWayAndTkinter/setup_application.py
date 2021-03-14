import tkinter as tk


class SetupApplication(tk.Frame):
    def __init__(self, master, callback):
        super().__init__(master)
        self.master.title(f"New Game Setup")
        self.master.minsize(200, 150)
        self.grid(sticky=tk.NSEW)
        self._callback = callback
        self.__create_widgets()

    def __on_new_press(self):
        self._callback(int(self._width_val.get()), int(self._height_val.get()))
        self.master.destroy()

    def __create_widgets(self):
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        for i in range(3):
            self.rowconfigure(i, weight=1)

        for i in range(2):
            self.columnconfigure(i, weight=1)

        self._width_label = tk.Label(self, width=5, height=2, text="Width = ")
        self._width_label.grid(row=0, column=0, sticky=tk.NSEW)
        self._width_val = tk.Spinbox(self, width=5, from_=2, to=25, increment=1)
        self._width_val.grid(row=0, column=1, sticky=tk.NSEW)

        self._height_label = tk.Label(self, width=5, height=2, text="Height = ")
        self._height_label.grid(row=1, column=0, sticky=tk.NSEW)
        self._height_val = tk.Spinbox(self, width=5, from_=2, to=25, increment=1)
        self._height_val.grid(row=1, column=1, sticky=tk.NSEW)

        self._cancel_button = tk.Button(self, width=5, height=2, text='Cancel', command=self.master.destroy)
        self._cancel_button.grid(row=2, column=0, sticky=tk.NSEW)

        self._new_button = tk.Button(self, width=5, height=2, text='New', command=self.__on_new_press)
        self._new_button.grid(row=2, column=1, sticky=tk.NSEW)
