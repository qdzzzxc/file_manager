import tkinter as tk

from data_getter import ColumnPage
from widgets import ColumnWindow, RowWindow


class Application(tk.Tk):
    def __init__(self, width, height, bar_height=30):
        super().__init__()
        self.title("File manager")
        self.geometry(f"{width}x{height}")
        self.width = width
        self.height = height
        self.f = tk.Frame(self, width=width, height=height, bg='lightblue')
        self.f.pack()
        self.left_window = ColumnWindow(
            self.f,
            width=self.width // 2,
            height=self.height - bar_height * 2,
            data_page_cls=ColumnPage,
            active=True,
        )
        self.right_window = ColumnWindow(
            self.f,
            width=self.width // 2,
            height=self.height - bar_height * 2,
            data_page_cls=ColumnPage,
        )

        self.top_bar = RowWindow(
            self.f,
            width=self.width,
            height=bar_height,
            bar_height=bar_height,
            buttons_names=['кнопка 1', 'кнопка 2', 'кнопка 3'],
        )
        self.bottom_bar = RowWindow(
            self.f,
            width=self.width,
            height=self.height - bar_height,
            bar_height=bar_height,
            buttons_names=['кнопка 3', 'кнопка 4'],
        )

        self.left_window.c.place(x=0, y=bar_height)
        self.right_window.c.place(x=width // 2, y=bar_height)
        self.top_bar.c.place(x=0, y=0)
        self.bottom_bar.c.place(x=0, y=height - bar_height)

        self.bind_keys()

        self.left_window.draw_temp_state()
        self.right_window.draw_temp_state()
        self.top_bar.draw_temp_state()
        self.bottom_bar.draw_temp_state()

        self.temp_window = self.left_window

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
        ]:
            self.f.bind(f"<KeyPress-{letter}>", self.on_key_press)

    def on_key_press(self, event):
        if event.keysym in ["Up", "w", "W"]:
            self.temp_window.cursor_position -= 1
        if event.keysym in ["Down", "s", "S"]:
            self.temp_window.cursor_position += 1
        if event.keysym in ["Left", "a", "A"]:
            self.temp_window.active = False
            self.temp_window.draw_temp_state_with_error_check()
            self.temp_window = self.left_window
            self.temp_window.active = True
        if event.keysym in ["Right", "d", "D"]:
            self.temp_window.active = False
            self.temp_window.draw_temp_state_with_error_check()
            self.temp_window = self.right_window
            self.temp_window.active = True
        if event.keysym in ["Return"]:
            if self.temp_window.selected_file[1]:
                self.temp_window.data_page.cd(self.temp_window.selected_file[0])
                self.temp_window.reset_counters()
                self.temp_window.selected_file = (None, False)
        if event.keysym in ["Escape"]:
            check_head = self.temp_window.data_page.cd_higher()
            if check_head:
                self.temp_window.get_counters()

        # self.cursor_position = min(max(0, self.cursor_position), self.temp_window.data_length - 1)

        self.temp_window.calculate_offset()

        self.temp_window.draw_temp_state_with_error_check()


# WIDTH = 600
# HEIGHT = 400
WIDTH = 800
HEIGHT = 600

if __name__ == "__main__":
    app = Application(WIDTH, HEIGHT)
    app.mainloop()
