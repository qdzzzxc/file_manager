import tkinter as tk
import numpy as np

import tkinter.font as tkFont
from abc import abstractmethod


class AdapterWindow:
    def __init__(self, root, width, height, data_page_cls, active=False):
        self.active = active
        self.c = tk.Canvas(
            root, width=width, height=height, bg="lightblue", highlightthickness=0
        )

        self.width = width
        self.height = height

        self.get_fonts()
        
    def get_fonts(self):
        self.common_font = tkFont.Font(family="Helvetica", size=12)
        self.selected_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
        self.error_font = tkFont.Font(family="Helvetica", size=10)

    @abstractmethod
    def draw_temp_state():
        pass
    

class ColumnWindow(AdapterWindow):
    def __init__(self, root, width, height, data_page_cls, y_pad=20, first_offset=40, active=False):
        super().__init__(root, width, height, active)

        self.selected = False

        self.data_page = data_page_cls()
        self.text_path_field = None

        self.cursor_position = 0
        self.offset = 0
        self.counters_history = []

        self.first_offset = first_offset
        self.y_pad = y_pad
        self.files_on_page = (height - self.first_offset) // y_pad - 1 # for bar, for dots

    def draw_temp_state(self, highligted_color="black", higlighted_text=None):
        content = self.data_page.get_page_content()
        if isinstance(content, dict):
            return content["error"]
        self.draw_page(
            content, highligted_color=highligted_color, higlighted_text=higlighted_text
        )

    def draw_page(
        self, content, highligted_color="black", higlighted_text=None, rect_color=None
    ):  
        self.c.delete("all")

        font = self.common_font
        self.text_path_field = tk.Text(self.c, height=1, width=self.width, 
                                       bg='lightblue', font=font, bd=0, wrap='none')
        
        self.text_path_field.place(x=0, y=0)
        self.text_path_field.insert(tk.END, self.data_page.path)
        self.c.create_rectangle(
                    0, 20, self.width, self.height, fill=rect_color
                )
        y_offset = self.first_offset

        for i, (file_name, isdir) in enumerate(
            content[self.offset : self.offset + self.files_on_page]
        ):
            text = f"> {file_name}" if isdir else f"| {file_name}"
            if i == self.cursor_position - self.offset:
                self.selected_file = (file_name, isdir)
                rect_color = "#AFEEEE" if self.active else rect_color
                rect_color = "#E0FFFF" if self.selected else rect_color

                self.c.create_rectangle(
                    0, y_offset, self.width, y_offset + 20, fill=rect_color
                )
                self.c.create_text(
                    10,
                    y_offset,
                    anchor="nw",
                    text=text,
                    font=self.selected_font,
                    fill=highligted_color,
                )
                if higlighted_text:
                    self.c.create_text(
                        sum([self.selected_font.measure(x) for x in text]) + self.selected_font.measure('O'),
                        y_offset + 1,
                        anchor="nw",
                        text=higlighted_text,
                        font=self.error_font,
                        fill=highligted_color,
                    )
            else:
                self.c.create_text(10, y_offset, anchor="nw", text=text, font=font)

            y_offset += self.y_pad

        if self.offset > 0:
            self.c.create_text(10, self.first_offset - self.y_pad , anchor="nw", text="...", font=self.selected_font)

        if self.data_page.data_length > self.offset + self.files_on_page:
            self.c.create_text(
                10, y_offset - 10, anchor="nw", text="...", font=self.selected_font
            )

    def reset_counters(self):
        self.counters_history.append(
            (self.cursor_position, self.offset, self.data_page.data_length)
        )
        self.cursor_position = 0
        self.offset = 0

    def get_counters(self):
        if self.counters_history:
            self.cursor_position, self.offset, self.data_page.data_length = (
                self.counters_history.pop()
            )
        else:
            self.cursor_position, self.offset = (
                0,
                0,
            )  # self.data_length всё равно какой

    def calculate_offset(self):
        if self.cursor_position < 0:
            self.cursor_position = self.data_page.data_length - 1
        if self.cursor_position > self.data_page.data_length - 1:
            self.cursor_position = 0

        if self.cursor_position >= self.offset + self.files_on_page:
            self.offset += self.cursor_position + 1 - self.offset - self.files_on_page
        elif self.cursor_position < self.offset:
            self.offset -= self.offset - self.cursor_position

    def draw_temp_state_with_error_check(self):
        self.calculate_offset()

        f = self.draw_temp_state()
        if f:
            print(f)
            self.data_page.cd_higher()
            self.get_counters()
            self.draw_temp_state(highligted_color="red", higlighted_text=f)


class RowWindow(AdapterWindow):
    def __init__(self, root, width, height, bar_height=30, buttons_names=None, buttons_functions=None, buttons_coords=None, active=False):
        super().__init__(root, width, height, active)

        self.cursor_position = 0
        self.active_option = 0

        self.bar_height = 30

        self.buttons_names = buttons_names
        self.buttons_len = len(buttons_names)
        self.buttons_coords = np.linspace(0, width, self.buttons_len + 1) if buttons_coords is None else buttons_coords
        self.buttons_functions = [None] * self.buttons_len if buttons_functions is None else buttons_functions

    def update_active_option(self):
        self.active_option = self.cursor_position

    def draw_temp_state(self, highligted_color="black"):
        content = self.buttons_names
        if isinstance(content, dict):
            return content["error"]
        self.draw_page(
            content, highligted_color=highligted_color
        )

    def draw_page(self, content, highligted_color="black"):
        self.c.delete("all")
        font = self.common_font

        for i, (name, x_pos1, x_pos2) in enumerate(zip(content, self.buttons_coords, self.buttons_coords[1:])):
            print(i, self.active_option)
            rect_color = "#AFEEEE" if i == self.active_option else None
            self.c.create_rectangle(
                    x_pos1, 0, x_pos2, self.bar_height - 1, fill=rect_color
                )
            
            text = name
            if i == self.cursor_position:
                self.c.create_text(
                    (x_pos1 + x_pos2)/2,
                    self.bar_height/2,
                    anchor="center",
                    text=text,
                    font=self.selected_font,
                    fill=highligted_color,
                )
            else:
                self.c.create_text((x_pos1 + x_pos2)/2, self.bar_height/2, anchor="center", text=text, font=font)

    def draw_temp_state_with_error_check(self):
        self.cursor_position = max(min(self.cursor_position, self.buttons_len - 1), 0)
        self.draw_temp_state()
