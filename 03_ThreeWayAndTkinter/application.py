import tkinter as tk
from tkinter import messagebox
from model import TagModel


class Application(tk.Frame):
    def __init__(self, master=None, game_model: TagModel = None):
        super().__init__(master)
        self.master.title(f"Tag game {game_model.width}x{game_model.height}")
        self._game_model = game_model or TagModel(4, 4)
        self.grid(sticky=tk.NSEW)
        self.__create_widgets()

    def __setup_grid(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        for y in range(1, 1+self._game_model.height):
            self.rowconfigure(y, weight=10)
        for x in range(self._game_model.width):
            self.columnconfigure(x, weight=1)

    def __make_shuffle(self):
        self._game_model.shuffle()
        for idx, button in self._chip_buttons.items():
            x, y = self._game_model.get_chip_coords(idx)
            button.grid(row=y+1, column=x)

    def __generate_new_game_part(self):
        for button in self._chip_buttons.values():
            button.destroy()
        self._chip_buttons.clear()
        for y in range(self._game_model.height):
            for x in range(self._game_model.width):
                current_chip = self._game_model.get_chip_idx_at(x, y)
                if current_chip is None:
                    continue
                button_name = str(current_chip + 1)
                b = tk.Button(self,
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

            if self._game_model.check_win():
                messagebox.showinfo("WIN", 'You are win this game!')
                self.__make_shuffle()
        return wrapper

    def change_game(self, new_game: TagModel):
        self._game_model = new_game
        self.master.title(f"Tag game {new_game.width}x{new_game.height}")
        self.__generate_new_game_part()

    def __create_widgets(self):
        self.__setup_grid()

        self._new_button = tk.Button(self, text='Shuffle', command=self.__make_shuffle)
        self._new_button.grid(row=0, column=0, sticky=tk.NSEW)

        self._exit_button = tk.Button(self, text='Exit', command=self.quit)
        self._exit_button.grid(row=0, column=self._game_model.width-1, sticky=tk.NSEW)

        self._chip_buttons = {}
        self.__generate_new_game_part()
