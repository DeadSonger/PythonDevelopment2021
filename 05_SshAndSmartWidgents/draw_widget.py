import tkinter as tk
import tkinter.colorchooser as cc

from figure import RectFigure, OvalFigure, BaseDrawSettings


class ColorChooser(tk.Frame):
    def __init__(self, master, color, callback):
        super().__init__(master)
        self.color = color
        self.callback = callback
        self.master.title(f"Color setup")
        self.master.minsize(200, 150)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky=tk.NSEW)
        self.create_widgets()

    def change_color(self, val):
        self._view_frame.configure(
            bg=
            f'#{hex(int(self._color_frame._red.get()))[2:].zfill(2)}'
            f'{hex(int(self._color_frame._green.get()))[2:].zfill(2)}'
            f'{hex(int(self._color_frame._blue.get()))[2:].zfill(2)}')

    def apply(self):
        self.callback(self._view_frame['bg'])
        self.master.destroy()

    def create_widgets(self):
        self.rowconfigure(0, weight=10)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self._view_frame = tk.Frame(self, bg=self.color)
        self._view_frame.grid(row=0, column=1, sticky=tk.NSEW)

        self._color_frame = tk.Frame(self)
        self._color_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self._color_frame.columnconfigure(0, weight=1)
        for i in range(3):
            self._color_frame.rowconfigure(i, weight=1)

        red = int(self.color[1:3], base=16)
        green = int(self.color[3:5], base=16)
        blue = int(self.color[5:], base=16)

        self._color_frame._red = tk.Scale(self._color_frame, from_=0, to_=255,
                                          label='red', orient=tk.HORIZONTAL, command=self.change_color)
        self._color_frame._red.grid(row=0, column=0, sticky=tk.NSEW)
        self._color_frame._red.set(red)

        self._color_frame._green = tk.Scale(self._color_frame, from_=0, to_=255,
                                            label='green', orient=tk.HORIZONTAL, command=self.change_color)
        self._color_frame._green.grid(row=1, column=0, sticky=tk.NSEW)
        self._color_frame._green.set(green)

        self._color_frame._blue = tk.Scale(self._color_frame, from_=0, to_=255,
                                           label='blue', orient=tk.HORIZONTAL, command=self.change_color)
        self._color_frame._blue.grid(row=2, column=0, sticky=tk.NSEW)
        self._color_frame._blue.set(blue)

        self._ok = tk.Button(self, text='apply', command=self.apply)
        self._ok.grid(row=1, column=1, sticky=tk.NSEW)


class DrawWidget(tk.Frame):

    def __init__(self, master, figures, update_callback=None, append_callback=None):
        super().__init__(master)
        self.figures = figures
        self.map = []
        self.draw_map = {
            'Oval': OvalFigure,
            'Rect': RectFigure
        }
        self.update_callback = update_callback
        self.append_callback = append_callback
        self.create_widgets()

    def redraw(self):
        self._canvas.delete("all")
        self.map.clear()
        for fig in self.figures:
            self.map.append(fig.draw(self._canvas))

    def press_handler(self, event):
        self.move_obj = None
        for i, fig in enumerate(self.figures):
            if fig.contains(event.x, event.y):
                self.move_obj = i

        if self.move_obj is None:
            self.x0 = event.x
            self.y0 = event.y

            ds = BaseDrawSettings(
                int(self._tool_bar._bw.get()),
                self._tool_bar._bg['bg'],
                self._tool_bar._fg['bg']
            )

            self.figures.append(
                self.draw_map[self._tool_bar._shape.get()](
                    event.x, event.y, event.x, event.y, ds))
            self.redraw()
            self.append_callback(len(self.map)-1)
        else:
            self.prev_x = event.x
            self.prev_y = event.y

    def motion_handler(self, event):
        if self.move_obj is not None:
            dx = event.x - self.prev_x
            dy = event.y - self.prev_y
            self._canvas.move(self.map[self.move_obj], dx, dy)
            self.figures[self.move_obj].move(dx, dy)
            self.prev_x = event.x
            self.prev_y = event.y
            self.update_callback(self.move_obj)
        else:
            self.figures[-1].x1 = event.x
            self.figures[-1].y1 = event.y
            self._canvas.coords(self.map[-1], self.x0, self.y0, event.x, event.y)
            self.update_callback(len(self.map)-1)

    def chenge_bg(self):
        l = tk.Toplevel(self)

        def callback(color):
            self._tool_bar._bg['bg'] = color

        ColorChooser(l, self._tool_bar._bg['bg'], callback)

    def chenge_fg(self):
        l = tk.Toplevel(self)

        def callback(color):
            self._tool_bar._fg['bg'] = color

        ColorChooser(l, self._tool_bar._fg['bg'], callback)

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=20)

        self._tool_bar = tk.Frame(self)
        self._tool_bar.grid(row=0, column=0, sticky=tk.NSEW)

        self._tool_bar.rowconfigure(0, weight=1)
        for i in range(4):
            self._tool_bar.columnconfigure(i, weight=1)

        self._tool_bar._shape = tk.Spinbox(self._tool_bar,
                                           justify=tk.CENTER, values=[*self.draw_map.keys()],
                                           exportselection=True, state='readonly')
        self._tool_bar._shape.grid(row=0, column=0, sticky=tk.NSEW)

        self._tool_bar._bw = tk.Spinbox(self._tool_bar, text='BW = ', increment=1, from_=1, to_=999)
        self._tool_bar._bw.grid(row=0, column=1, sticky=tk.NSEW)

        self._tool_bar._bg = tk.Button(self._tool_bar, bg='#000000', command=self.chenge_bg)
        self._tool_bar._bg.grid(row=0, column=2, sticky=tk.NSEW)

        self._tool_bar._fg = tk.Button(self._tool_bar, bg='#ffffff', command=self.chenge_fg)
        self._tool_bar._fg.grid(row=0, column=3, sticky=tk.NSEW)

        self._canvas = tk.Canvas(self, background='#FFFFFF')
        self._canvas.bind('<ButtonPress >', self.press_handler)
        self._canvas.bind('<B1-Motion>', self.motion_handler)
        self._canvas.grid(row=1, column=0, sticky=tk.NSEW)

        cc.Dialog(self)
