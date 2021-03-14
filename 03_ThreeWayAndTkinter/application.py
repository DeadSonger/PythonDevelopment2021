import tkinter as tk
from tkinter import messagebox
from setup_application import SetupApplication
from model import TagModel


class Application(tk.Frame):
    def __init__(self, master=None, game_model: TagModel = None):
        super().__init__(master)
        self.master.title(f"Tag game {game_model.width}x{game_model.height}")
        self._game_model = game_model or TagModel(4, 4)
        self._step_counter = 0
        self._step_counter_text_var = tk.StringVar()
        self.grid(sticky=tk.NSEW)
        self.__create_widgets()

    def __set_step_counter(self, val: int):
        self._step_counter = val
        self._step_counter_text_var.set(f'Steps: {val:03d}')

    def __setup_grid(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)

    def __generate_new_game_part(self):
        for button in self._chip_buttons.values():
            button.destroy()
        self._chip_buttons.clear()

        if self._game_field:
            self._game_field.destroy()

        self._game_field = tk.Frame(self)
        self._game_field.grid(sticky=tk.NSEW, row=1, column=0)

        for y in range(self._game_model.height):
            self._game_field.rowconfigure(y, weight=1)

        for x in range(self._game_model.width):
            self._game_field.columnconfigure(x, weight=1)

        for y in range(self._game_model.height):
            for x in range(self._game_model.width):
                current_chip = self._game_model.get_chip_idx_at(x, y)
                if current_chip is None:
                    continue
                button_name = str(current_chip + 1)
                b = tk.Button(self._game_field,
                              width=10, height=3,
                              text=button_name, command=self.__on_chip_button_press_generator(current_chip))
                b.grid(row=1+y, column=x, padx=1, pady=1, ipadx=1, ipady=1, sticky=tk.NSEW)
                self._chip_buttons[current_chip] = b

    def __on_chip_button_press_generator(self, idx: int):
        def wrapper():
            if not self._game_model.is_chip_movable(idx):
                return
            free_space = self._game_model.free_space_coords
            self._game_model.move_chip(idx)
            self._chip_buttons[idx].grid(row=free_space[1]+1, column=free_space[0])

            self.__set_step_counter(self._step_counter+1)

            if self._game_model.check_win():
                messagebox.showinfo("WIN", f'You are win this game use {self._step_counter} steps!')
                self.__make_shuffle()
        return wrapper

    def __on_new_game_press(self):
        l = tk.Toplevel(self)

        def callback(width, height):
            new_game = TagModel(width, height)
            new_game.shuffle()
            self.change_game(new_game)

        l.title("New game setup")
        SetupApplication(l, callback)

    def __create_widgets(self):
        self.__setup_grid()

        self._menu_frame = tk.Frame(self)
        self._menu_frame.grid(sticky=tk.NSEW, row=0, column=0, columnspan=self._game_model.width)

        for i in range(4):
            self._menu_frame.columnconfigure(i, weight=1)

        self._shuffle_button = tk.Button(self._menu_frame, width=5, text='Shuffle', command=self.__make_shuffle)
        self._shuffle_button.grid(row=0, padx=10, ipadx=10, column=0, sticky=tk.NSEW)

        self._new_game_button = tk.Button(self._menu_frame, width=5, text='New', command=self.__on_new_game_press)
        self._new_game_button.grid(row=0, padx=10, ipadx=10, column=1, sticky=tk.NSEW)

        self.__set_step_counter(0)
        self._step_counter_text = tk.Label(self._menu_frame, width=5, textvariable=self._step_counter_text_var)
        self._step_counter_text.grid(row=0, padx=10, ipadx=10, column=2, sticky=tk.NSEW)

        self._exit_button = tk.Button(self._menu_frame, width=5, text='Exit', command=self.quit)
        self._exit_button.grid(row=0, padx=10, ipadx=10, column=3, sticky=tk.NSEW)

        self._chip_buttons = {}
        self._game_field = None
        self.__generate_new_game_part()

    def __make_shuffle(self):
        self._game_model.shuffle()
        self.__set_step_counter(0)
        for idx, button in self._chip_buttons.items():
            x, y = self._game_model.get_chip_coords(idx)
            button.grid(row=y + 1, column=x)

    def change_game(self, new_game: TagModel):
        self._game_model = new_game
        self.master.title(f"Tag game {new_game.width}x{new_game.height}")
        self.__set_step_counter(0)
        self.__generate_new_game_part()
