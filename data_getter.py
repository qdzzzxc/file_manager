import os

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
        if self.path != self.work_dir:  # выход из мейн директории
            self.path = os.path.dirname(self.path)
            return True
        return False
    
    def touch(self, filename, base=False):
        if os.path.exists(os.path.join(self.path, filename)):
            filename = filename.split('.')[:-1]
            extension = filename.split('.')[-1]
            num = 1
            while os.path.exists(os.path.join(self.path, f"{filename} ({num}).{extension}")):
                num += 1
            filename = f"{filename} ({num}).{extension}"
        open(os.path.join(self.path, filename), 'a').close()
        