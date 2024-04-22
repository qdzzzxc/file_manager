import os
import shutil


def list_directory(path):
    """Выводит список файлов и папок в директории"""
    try:
        files = os.listdir(path)
        print(f"Содержимое {path}:")
        for file in files:
            print(file)
    except FileNotFoundError:
        print("Директория не найдена")


def make_directory(path):
    """Создает новую папку"""
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Папка {path} создана")
    except OSError as e:
        print(f"Ошибка: {e}")


def make_file(path):
    """Создает новый файл"""
    try:
        with open(path, "w") as file:
            file.write("")  # Создаем пустой файл
        print(f"Файл {path} создан")
    except OSError as e:
        print(f"Ошибка: {e}")


def remove_file(path):
    """Удаляет файл или папку"""
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
            print(f"Папка {path} удалена")
        elif os.path.isfile(path):
            os.remove(path)
            print(f"Файл {path} удален")
        else:
            print("Файл или папка не найдены")
    except OSError as e:
        print(f"Ошибка: {e}")


def main():
    current_directory = os.getcwd()
    while True:
        print("\nТекущая директория:", current_directory)
        print("Команды: ls, cd <path>, mkdir <path>, touch <path>, rm <path>, exit")
        command = input("Введите команду: ").strip().split()
        if not command:
            continue
        if command[0] == "ls":
            list_directory(current_directory)
        elif command[0] == "cd":
            if len(command) > 1:
                new_dir = os.path.join(current_directory, command[1])
                if os.path.isdir(new_dir):
                    current_directory = new_dir
                else:
                    print("Директория не найдена")
            else:
                print("Укажите директорию")
        elif command[0] == "mkdir":
            if len(command) > 1:
                make_directory(os.path.join(current_directory, command[1]))
            else:
                print("Укажите имя папки")
        elif command[0] == "touch":
            if len(command) > 1:
                make_file(os.path.join(current_directory, command[1]))
            else:
                print("Укажите имя файла")
        elif command[0] == "rm":
            if len(command) > 1:
                remove_file(os.path.join(current_directory, command[1]))
            else:
                print("Укажите путь для удаления")
        elif command[0] == "exit":
            print("Выход из программы")
            break
        else:
            print("Неизвестная команда")


if __name__ == "__main__":
    main()
