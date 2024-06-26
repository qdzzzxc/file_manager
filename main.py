import tkinter as tk

from data_getter import ColumnPage
from widgets import ColumnWindow, RowWindow
from fabric import OSFabric, OptionsFabric

from config import load_json, save_json


class Application(tk.Tk):
    def __init__(self, width, height, bar_height=30):
        super().__init__()

        self.fabric = OSFabric(root=self)
        self.options_fabric = OptionsFabric(root=self)

        self.bg_color, self.active_color, self.selected_color = load_json()

        self.title("File manager")
        self.geometry(f"{width}x{height}")
        self.width = width
        self.height = height
        self.f = tk.Frame(self, width=width, height=height, bg=self.bg_color)
        self.f.pack()
        self.left_window = ColumnWindow(
            self,
            width=self.width // 2,
            height=self.height - bar_height * 2,
            data_page_cls=ColumnPage,
        )
        self.right_window = ColumnWindow(
            self,
            width=self.width // 2,
            height=self.height - bar_height * 2,
            data_page_cls=ColumnPage,
        )

        self.top_bar = RowWindow(
            self,
            width=self.width,
            height=bar_height,
            bar_height=bar_height,
            buttons_names=[
                "Открыть",
                "Создать файл",
                "Создать папку",
                "Переименовать",
                "Копировать",
                "Вырезать",
                "Удалить",
            ],
            fabric=self.fabric,
        )
        self.bottom_bar = RowWindow(
            self,
            width=self.width,
            height=self.height - bar_height,
            bar_height=bar_height,
            buttons_names=["Помощь", "Настройки"],
            need_active=False,
            fabric=self.options_fabric,
        )

        self.left_window.c.place(x=0, y=bar_height)
        self.right_window.c.place(x=width // 2, y=bar_height)
        self.top_bar.c.place(x=0, y=0)
        self.bottom_bar.c.place(x=0, y=height - bar_height)

        self.bind_keys()
        self.window_type = "column"

        self.active_cursor_bar = None
        self.bars = [self.top_bar, self.bottom_bar]

        self.active_cursor = 0
        self.windows = [self.left_window, self.right_window]
        self.temp_window = self.left_window
        self.change_active(left=True)

        self.apply_colors()

    def apply_colors(self, bg_color=None, active_color=None, selected_color=None):
        self.bg_color = bg_color if bg_color is not None else self.bg_color
        self.active_color = active_color if active_color is not None else self.active_color
        self.selected_color = selected_color if selected_color is not None else self.selected_color

        for window in self.windows + self.bars:
            window.c.configure(bg=self.bg_color)
            window.draw_temp_state()

        save_json(self.bg_color, self.active_color, self.selected_color)

    def bind_keys(self):
        self.f.focus_set()
        for letter in [
            "s",
            "S",
            "w",
            "W",
            "Down",
            "Up",
            "Return",
            "Escape",
            "a",
            "A",
            "d",
            "D",
            "Left",
            "Right",
            "1",
            "2",
        ]:
            self.f.bind(f"<KeyPress-{letter}>", self.on_key_press)

    def change_active(self, left=True):
        if left:
            self.active_cursor -= 1
        else:
            self.active_cursor += 1

        self.active_cursor = max(min(self.active_cursor, len(self.windows) - 1), 0)

        self.temp_window.active = False
        self.temp_window.selected = False
        self.temp_window.draw_temp_state_with_error_check()
        self.temp_window = self.windows[self.active_cursor]
        self.temp_window.active = True
        self.temp_window.selected = True

    def on_key_press(self, event):
        if event.keysym in ["Up", "w", "W"]:
            if self.window_type == "column":
                self.temp_window.move_cursor(-1)

            elif self.window_type == "row" and self.active_cursor_bar == 1:
                self.temp_window = self.last_temp
                self.temp_window.selected = True
                self.last_temp = None

                self.active_cursor_bar = None
                self.window_type = "column"
        if event.keysym in ["Down", "s", "S"]:
            if self.window_type == "column":
                self.temp_window.move_cursor(1)

            elif self.window_type == "row" and self.active_cursor_bar == 0:
                self.temp_window = self.last_temp
                self.temp_window.selected = True
                self.last_temp = None

                self.active_cursor_bar = None
                self.window_type = "column"
        if event.keysym in ["Left", "a", "A"]:
            if self.window_type == "column":
                self.change_active(left=True)

            elif self.window_type == "row":
                self.temp_window.move_cursor(-1)
        if event.keysym in ["Right", "d", "D"]:
            if self.window_type == "column":
                self.change_active(left=False)

            elif self.window_type == "row":
                self.temp_window.move_cursor(1)
        if event.keysym in ["1"]:
            self.active_cursor_bar = 0
            self.last_temp = (
                self.temp_window if self.window_type == "column" else self.last_temp
            )
            self.window_type = "row"
            self.temp_window.selected = False
            self.temp_window.draw_temp_state_with_error_check()
            self.temp_window = self.bars[self.active_cursor_bar]
        if event.keysym in ["2"]:
            self.active_cursor_bar = 1
            self.last_temp = (
                self.temp_window if self.window_type == "column" else self.last_temp
            )
            self.window_type = "row"
            self.temp_window.selected = False
            self.temp_window.draw_temp_state_with_error_check()
            self.temp_window = self.bars[self.active_cursor_bar]
        if event.keysym in ["Return"]:
            self.temp_window.enter_press(self.fabric)

        if event.keysym in ["Escape"]:
            if self.window_type == "column":
                check_head = self.temp_window.data_page.cd_higher()
                if check_head:
                    self.temp_window.get_counters()
            elif self.window_type == "row":
                pass

        self.temp_window.draw_temp_state_with_error_check()

    def second_update(self, deleted=False):
        if self.temp_window is self.left_window:
            if deleted:
                self.right_window.move_cursor(-1)
            self.right_window.draw_temp_state()
        else:
            if deleted:
                self.left_window.move_cursor(-1)
            self.left_window.draw_temp_state()


# WIDTH = 600
# HEIGHT = 400
WIDTH = 800
HEIGHT = 600

if __name__ == "__main__":
    app = Application(WIDTH, HEIGHT)
    app.mainloop()
