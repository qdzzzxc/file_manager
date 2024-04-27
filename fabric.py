import tkinter as tk
import threading

result_filename = None

class OSFabric:
    def __init__(self):
        self.method = 0
        self.methods = [self.open, self.create_file, self.create_dir, self.copy, self.cut, self.delete]

    def __call__(self, temp_window):
        method = self.methods[self.method]
        method(temp_window)

    def open(self, temp_window):
        if temp_window.selected_file[1]:
            temp_window.data_page.cd(temp_window.selected_file[0])
            temp_window.reset_counters()
            temp_window.selected_file = (None, False)

    def create_file(self, temp_window):
        create_file_prompt('Создание файла', 
                'Введите название создаваемого файла', 
                'file.txt', temp_window)
        
        #args = ('Создание файла', 
        #        'Введите название создаваемого файла', 
        #        'file.txt', temp_window)
        #threading.Thread(target=create_file_prompt, args=args).start()

    def create_dir(self, temp_window):
        create_file_prompt('Создание директории', 'Введите название создаваемой директории',
                           default_text='directory')
        temp_window.wait_window()

    def copy(self, temp_window):
        pass

    def cut(self, temp_window):
        pass

    def delete(self, temp_window):
        pass

    def choose_mode(self, n):
        self.method = n

def create_file_prompt(label_text, field_text, default_text, window):
    top = tk.Toplevel(bg='lightblue')
    top.geometry(f"{300}x{125}")
    top.title(label_text)

    tk.Label(top, text=field_text, width=50).pack(side=tk.TOP, padx=5, pady=5)

    entry = tk.Entry(top, width=50)
    entry.pack(side=tk.TOP, padx=10, pady=10)
    entry.insert(tk.END, default_text)

    def on_submit():
        filename = entry.get()
        top.destroy()

        global result_filename
        result_filename =  filename
        print(result_filename)

    submit_button = tk.Button(top, text="Подтвердить", command=on_submit)
    submit_button.pack(side=tk.TOP, padx=10, pady=10)

    window.c.wait_window(top)
