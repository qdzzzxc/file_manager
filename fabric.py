import tkinter as tk
from tkinter import colorchooser
import threading

from functools import partial
import os

result_filename = None


class OSFabric:
    def __init__(self, root):
        self.method = 0
        self.methods = [
            self.open,
            self.create_file,
            self.create_dir,
            self.rename,
            self.copy,
            self.cut,
            self.delete,
        ]

        self.copy_path = None
        self.root = root
        self.second_update = self.root.second_update

    def __call__(self, temp_window):
        method = self.methods[self.method]
        method(temp_window)

    def open(self, temp_window):
        if temp_window.selected_file[1]:
            temp_window.data_page.cd(temp_window.selected_file[0])
            temp_window.reset_counters()
            temp_window.selected_file = (None, False)

    def create_file(self, temp_window):
        args = (
            "Создание файла",
            "Введите название создаваемого файла",
            "file.txt",
            temp_window,
            self,
            "file",
            self.root.bg_color,
        )
        threading.Thread(target=create_prompt, args=args).start()

    def create_dir(self, temp_window):
        args = (
            "Создание директории",
            "Введите название создаваемой директории",
            "directory",
            temp_window,
            self,
            "dir",
            self.root.bg_color,
        )
        threading.Thread(target=create_prompt, args=args).start()

    def rename(self, temp_window):
        args = (
            "Переименовать",
            "Введите новое название",
            "new name",
            temp_window,
            self,
            "rename",
            self.root.bg_color,
        )
        threading.Thread(target=create_prompt, args=args).start()

    def copy(self, temp_window):
        if self.copy_path is None:
            self.copy_path = os.path.join(
                temp_window.data_page.path, temp_window.selected_file[0]
            )
        else:

            def thread():
                temp_window.data_page.paste(self.copy_path)

                self.copy_path = None
                temp_window.draw_temp_state()

            threading.Thread(target=thread, args=()).start()

    def cut(self, temp_window):
        if self.copy_path is None:
            self.copy_path = os.path.join(
                temp_window.data_page.path, temp_window.selected_file[0]
            )
        else:

            def thread():
                temp_window.data_page.cut_paste(self.copy_path)

                self.copy_path = None
                self.second_update(deleted=True)
                temp_window.draw_temp_state()

            threading.Thread(target=thread, args=()).start()

    def delete(self, temp_window):
        if temp_window.selected_file[0]:
            temp_window.data_page.delete(temp_window.selected_file)
            temp_window.move_cursor(-1)
            temp_window.selected_file = (None, False)

            self.second_update()

    def choose_mode(self, n, window=None):
        self.method = n
        self.copy_path = None


class OptionsFabric:
    def __init__(self, root):
        self.method = 0
        self.methods = [
            self.help,
            self.settings,
        ]

        self.root = root

    def help(self, temp_window):
        args = (
            "Помощь",
            "Нажмите 1 для доступа к верхнему меню\nНажмите 2 для доступа к нижнему меню",
            temp_window,
            self.root.bg_color,
        )
        threading.Thread(target=create_text_window, args=args).start()

    def settings(self, temp_window):
        args = (
            "Настройки",
            "Выберите нужные вам цвета",
            temp_window,
            self.root,
        )
        threading.Thread(target=create_select_color_window, args=args).start()

    def choose_mode(self, n, window):
        self.method = n
        method = self.methods[self.method]
        method(window)


def create_prompt(label_text, field_text, default_text, window, self, type="file", bg_color=None):
    top = tk.Toplevel(bg=bg_color)
    top.geometry(f"{300}x{125}")
    top.title(label_text)

    tk.Label(top, text=field_text, width=50).pack(side=tk.TOP, padx=5, pady=5)

    entry = tk.Entry(top, width=50)
    entry.pack(side=tk.TOP, padx=10, pady=10)
    entry.insert(tk.END, default_text)

    def on_submit(event=None):
        name = entry.get()
        top.destroy()

        if type == "file":
            window.data_page.touch(name)
        elif type == "dir":
            window.data_page.mkdir(name)
        elif type == "rename":
            window.data_page.rename(window.selected_file[0], name)

        self.second_update()

        window.draw_temp_state()

    top.bind("<Return>", on_submit)

    submit_button = tk.Button(top, text="Подтвердить", command=on_submit)
    submit_button.pack(side=tk.TOP, padx=10, pady=10)

    window.c.wait_window(top)


def create_text_window(label_text, field_text, window, bg_color=None):
    top = tk.Toplevel(bg=bg_color)
    top.geometry(f"{300}x{125}")
    top.title(label_text)

    tk.Label(top, text=field_text, width=50).pack(side=tk.TOP, padx=5, pady=5)

    def on_submit(event=None):
        top.destroy()

    top.bind("<Return>", on_submit)

    submit_button = tk.Button(top, text="Закрыть", command=on_submit)
    submit_button.pack(side=tk.BOTTOM, padx=10, pady=10)

    window.c.wait_window(top)


def create_select_color_window(label_text, field_text, window, root):
    top = tk.Toplevel(bg=root.bg_color)
    top.geometry(f"{300}x{250}")
    top.title(label_text)

    tk.Label(top, text=field_text, width=50).pack(side=tk.TOP, padx=5, pady=5)

    colors = {"bg_color": root.bg_color,
              "active_color": root.active_color,
              "selected_color": root.selected_color}

    def choose_color(text, kind):
        color_code = colorchooser.askcolor(title=text)
        if color_code[1] is not None:
            colors[kind] = color_code[1]

    text = "Фоновый цвет"
    tk.Button(top, text=text, command=partial(choose_color, text=text, kind='bg_color')).pack(
        side=tk.TOP, padx=5, pady=5
    )

    text = "Цвет активного элемента"
    tk.Button(top, text=text, command=partial(choose_color, text=text, kind='active_color')).pack(
        side=tk.TOP, padx=5, pady=5
    )

    text = "Цвет выбранного элемента"
    tk.Button(top, text=text, command=partial(choose_color, text=text, kind='selected_color')).pack(
        side=tk.TOP, padx=5, pady=5
    )

    def on_submit(event=None):
        root.apply_colors(**colors)
        top.destroy()

    top.bind("<Return>", on_submit)

    submit_button = tk.Button(top, text="Подтвердить", command=on_submit)
    submit_button.pack(side=tk.BOTTOM, padx=10, pady=10)

    window.c.wait_window(top)
