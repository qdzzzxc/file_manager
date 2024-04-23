import tkinter as tk
import os

import tkinter.font as tkFont
from abc import ABC, abstractmethod


class FilePage(ABC):
    @abstractmethod
    def get_page_content(self):
        pass


class ColumnPage(FilePage):
    def __init__(self, path=os.getcwd()):
        self.data_length = 0
        self.path = path
        self.work_dir = path

    def get_page_content(self):
        try:
            all_files = os.listdir(self.path)
        except (FileNotFoundError, PermissionError) as e:
            print(e)
            return {"error": e}

        result = []
        for file in all_files:
            abs_path = os.path.join(self.path, file)
            result.append((os.path.basename(abs_path), os.path.isdir(abs_path)))

        self.data_length = len(result)
        return result
    
    def cd(self, file_name):
        self.path = os.path.join(self.path, file_name)

    def cd_higher(self):
        # if self.path != self.work_dir:  # выход из мейн директории
        if True:
            self.path = os.path.dirname(self.path) 
            return True
        return False
    
#патерн адаптер
class ColumnWindow:
    def __init__(self, root, width, height, data_page_cls, y_pad=20):
        self.c = tk.Canvas(root, width=width, height=height, bg="lightblue", highlightthickness=0)
        self.data_page = data_page_cls()

        self.cursor_position = 0
        self.offset = 0
        self.counters_history = []
        
        self.y_pad = y_pad
        self.files_on_page = (height - 10)//y_pad - 2

        self.get_fonts()

    def get_fonts(self):
        self.common_font = tkFont.Font(family="Helvetica", size=12)
        self.selected_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
        self.error_font = tkFont.Font(family="Helvetica", size=10)

    def draw_temp_state(self, highligted_color='black', higlighted_text=None):
        content = self.data_page.get_page_content()
        if isinstance(content, dict):
            return content['error']
        self.draw_page(content, highligted_color=highligted_color, higlighted_text=higlighted_text)

    def draw_page(self, content, highligted_color='black', higlighted_text=None):
        y_offset = 10
        self.c.delete("all")
        font = self.common_font

        for i, (file_name, isdir) in enumerate(content[self.offset: self.offset + self.files_on_page]):
            text = f"> {file_name}" if isdir else f"| {file_name}"
            if i == self.cursor_position - self.offset:
                self.selected_file = (file_name, isdir)
                self.c.create_text(10, y_offset, anchor="nw", text=text, font=self.selected_font, fill=highligted_color)
                if higlighted_text:
                    self.c.create_text(self.selected_font.measure('0') * len(text), y_offset + 1, 
                                       anchor="nw", text=higlighted_text, font=self.error_font, fill=highligted_color)
            else:
                self.c.create_text(10, y_offset, anchor="nw", text=text, font=font)

            y_offset += self.y_pad

    def reset_counters(self):
        self.counters_history.append((self.cursor_position, self.offset, self.data_page.data_length))
        self.cursor_position = 0
        self.offset = 0

    def get_counters(self):
        if self.counters_history:
            self.cursor_position, self.offset, self.data_page.data_length = self.counters_history.pop()
        else:
            self.cursor_position, self.offset = 0, 0 # self.temp_window.data_length всё равно какой


class Application(tk.Tk):
    def __init__(self, width, height):
        super().__init__()
        self.title("File manager")
        self.geometry(f"{width}x{height}")
        self.width = width
        self.height = height

        self.f = tk.Frame(self, width=WIDTH, height=HEIGHT)
        self.f.pack()
        self.left_window = ColumnWindow(self.f, width=self.width//2, height=self.height, data_page_cls=ColumnPage)
        self.right_window = ColumnWindow(self.f, width=self.width//2, height=self.height, data_page_cls=ColumnPage)
        
        self.left_window.c.grid(row=0, column=0)
        self.right_window.c.grid(row=0, column=1)

        self.bind_keys()

        self.left_window.draw_temp_state()
        self.right_window.draw_temp_state()

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
            self.temp_window = self.left_window
        if event.keysym in ["Right", "d", "D"]:
            self.temp_window = self.right_window
        if event.keysym in ["Return"]:
            if self.temp_window.selected_file[1]:
                self.temp_window.data_page.cd(self.temp_window.selected_file[0])
                self.temp_window.reset_counters()
        if event.keysym in ["Escape"]:
            check_head = self.temp_window.data_page.cd_higher()
            if check_head:
                self.temp_window.get_counters()

        # self.cursor_position = min(max(0, self.cursor_position), self.temp_window.data_length - 1)

        if self.temp_window.cursor_position < 0:
            self.temp_window.cursor_position = self.temp_window.data_page.data_length - 1
        if self.temp_window.cursor_position > self.temp_window.data_page.data_length - 1:
            self.temp_window.cursor_position = 0

        if self.temp_window.cursor_position >= self.temp_window.offset + self.temp_window.files_on_page:
            self.temp_window.offset += self.temp_window.cursor_position + 1 - self.temp_window.offset - self.temp_window.files_on_page
        elif self.temp_window.cursor_position < self.temp_window.offset:
            self.temp_window.offset -= self.temp_window.offset - self.temp_window.cursor_position

        f = self.temp_window.draw_temp_state()
        if f:
            print(f)
            self.temp_window.data_page.cd_higher()
            self.temp_window.get_counters()
            self.temp_window.draw_temp_state(highligted_color='red', higlighted_text=f)


# WIDTH = 600
# HEIGHT = 400
WIDTH = 800
HEIGHT = 600

if __name__ == "__main__":
    app = Application(WIDTH, HEIGHT)
    app.mainloop()
