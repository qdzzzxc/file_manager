import os
import shutil

from abc import ABC, abstractmethod

from config import work_dir


class FilePage(ABC):
    @abstractmethod
    def get_page_content(self):
        pass


class ColumnPage(FilePage):
    def __init__(self, path=work_dir):
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
        if self.path != self.work_dir:  # выход из main директории
            self.path = os.path.dirname(self.path)
            return True
        return False

    def touch(self, filename):
        if os.path.exists(os.path.join(self.path, filename)):
            filename_ = ''.join(filename.split(".")[:-1])
            extension = filename.split(".")[-1]
            num = 1
            while os.path.exists(
                os.path.join(self.path, f"{filename_} ({num}).{extension}")
            ):
                num += 1
            filename = f"{filename_} ({num}).{extension}"
        open(os.path.join(self.path, filename), "a").close()

    def mkdir(self, dirname):
        if os.path.exists(os.path.join(self.path, dirname)):
            num = 1
            while os.path.exists(
                os.path.join(self.path, f"{dirname} ({num})")
            ):
                num += 1
            dirname = f"{dirname} ({num})"
        os.makedirs(os.path.join(self.path, dirname))

    def delete(self, file):
        if file[1]:
            shutil.rmtree(os.path.join(self.path, file[0]))
        else:
            os.remove(os.path.join(self.path, file[0]))

    def rename(self, file, name):
        new_file = os.path.join(self.path, name)
        if os.path.exists(os.path.join(self.path, new_file)):
            splitted = name.split(".")
            filename_ = ''.join(splitted[:-1]) if len(splitted) > 1 else splitted[0]
            extension = '.' + name.split(".")[-1] if len(splitted) > 1 else ''
            num = 1
            while os.path.exists(
                os.path.join(self.path, f"{filename_} ({num}){extension}")
            ):
                num += 1
            new_file = os.path.join(self.path, f"{filename_} ({num}){extension}")
        os.rename(os.path.join(self.path, file), new_file)

    def paste(self, src, dst=None):
        dst = self.path if dst is None else dst
        if os.path.isfile(src):
            shutil.copy2(src, dst)
        else:
            shutil.copytree(src, os.path.join(dst, src.split(os.path.sep)[-1]))

    def cut_paste(self, src, dst=None):
        dst = self.path if dst is None else dst
        if os.path.isfile(src):
            shutil.move(src, os.path.join(dst, src.split(os.path.sep)[-1]))
        else:
            shutil.move(src, os.path.join(dst, src.split(os.path.sep)[-1]),
                        copy_function=shutil.copytree)
