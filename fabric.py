class OSFabric:
    def __init__(self):
        self.method = 0
        self.methods = [self.open, self.create, self.copy, self.cut, self.delete]

    def __call__(self, temp_window):
        print(f'Вызывается метод {self.methods[self.method]}')

    def open(self, temp_window):
        if temp_window.selected_file[1]:
            temp_window.data_page.cd(temp_window.selected_file[0])
            temp_window.reset_counters()
            temp_window.selected_file = (None, False)

    def create(self, temp_window):
        pass

    def copy(self, temp_window):
        pass

    def cut(self, temp_window):
        pass

    def delete(self, temp_window):
        pass

    def choose_mode(self, n):
        self.method = n
