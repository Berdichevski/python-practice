import sys
import os


def display_page(data, offset, bytes_per_line=16, lines=16):
    """Выводит страницу файла, начиная с указанного смещения."""
    print("Offset | HEX                                            | ASCII")
    print("----------------------------------"
          "----------------------------------------")
    for line in range(lines):
        start = offset + line * bytes_per_line
        if start >= len(data):
            break
        segment = data[start:start + bytes_per_line]
        hex_bytes = " ".join(f"{b:02X}" for b in segment)
        ascii_repr = "".join(chr(b) if 32 <= b < 127 else "." for b in segment)
        print(f"{start:06X}   {hex_bytes:<48} {ascii_repr}")


def edit_byte(data):
    """Редактирует байт по заданному смещению."""
    try:
        offset_str = input("Введите смещение для редактирования "
                           "(например, 000006): ").strip()
        offset = int(offset_str, 16)
        if offset < 0 or offset >= len(data):
            print("Неверное смещение.")
            return
        original = data[offset]
        print(f"Исходное значение по смещению {offset_str.upper()}: "
              f"{original:02X}")
        new_hex = input("Введите новое значение (HEX, например 20): "
                        "").strip()
        if len(new_hex) != 2:
            print("Неверный формат. Должно быть 2 шестнадцатеричных "
                  "символа.")
            return
        new_value = int(new_hex, 16)
        data[offset] = new_value
        print(f"Значение по смещению {offset_str.upper()} изменено на "
              f"{new_hex.upper()}.")
    except Exception as e:
        print("Ошибка редактирования:", e)


def search_data(data):
    """Осуществляет поиск по данным в формате HEX или ASCII."""
    mode = input("Поиск по (HEX/ASCII): ").strip().lower()
    if mode == "hex":
        pattern_str = input("Введите HEX-последовательность (например, "
                            "48 65 6C 6C 6F): ").strip()
        # Удаляем пробелы
        pattern_str = pattern_str.replace(" ", "")
        if pattern_str != "":
            try:
                pattern = bytes.fromhex(pattern_str)
            except ValueError:
                print("Неверный формат HEX.")
                return
        else:
            print("Неверный формат HEX.")
            return
    elif mode == "ascii":
        pattern_str = input("Введите ASCII-последовательность: ")
        pattern = pattern_str.encode('ascii', errors='replace')
    else:
        print("Неверный режим поиска. Выберите HEX или ASCII.")
        return

    offset = data.find(pattern)
    if offset == -1:
        print("Паттерн не найден.")
    else:
        print(f"Паттерн найден по смещению: {offset:06X}")


def save_file(filename, data):
    """Сохраняет изменения в исходный файл."""
    try:
        with open(filename, "wb") as f:
            f.write(data)
        print("Файл успешно сохранен.")
    except Exception as e:
        print("Ошибка сохранения файла:", e)


def print_help():
    """Вывод справки по командам редактора."""
    print("""
Доступные команды:
    view [offset]   - Показать содержимое файла с указанного
    смещения (offset в шестнадцатеричном формате, по умолчанию
    текущий).
    next            - Перейти к следующей странице.
    prev            - Перейти к предыдущей странице.
    goto [offset]   - Перейти к указанному смещению (в
     шестнадцатеричном формате).
    edit            - Редактировать значение по смещению.
    search          - Поиск данных (HEX или ASCII).
    save            - Сохранить изменения в файл.
    help            - Показать это сообщение.
    quit            - Выход из редактора.
""")


def main():
    if len(sys.argv) < 2:
        print("Использование: python hexeditor.py <путь_к_файлу>")
        sys.exit(1)
    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print("Файл не найден.")
        sys.exit(1)
    try:
        with open(filename, "rb") as f:
            file_data = bytearray(f.read())
    except Exception as e:
        print("Ошибка чтения файла:", e)
        sys.exit(1)

    current_offset = 0
    page_size = 16 * 16  # 16 строк по 16 байт

    print(f"Открыт файл: {filename} ({len(file_data)} байт)")
    print_help()

    while True:
        command = input("\nВведите команду: ").strip().lower()
        if command.startswith("view"):
            parts = command.split()
            if len(parts) > 1:
                try:
                    current_offset = int(parts[1], 16)
                except ValueError:
                    print("Неверный формат смещения.")
                    continue
            display_page(file_data, current_offset)
        elif command == "next":
            if current_offset + page_size < len(file_data):
                current_offset += page_size
            else:
                print("Достигнут конец файла.")
            display_page(file_data, current_offset)
        elif command == "prev":
            if current_offset - page_size >= 0:
                current_offset -= page_size
            else:
                current_offset = 0
            display_page(file_data, current_offset)
        elif command.startswith("goto"):
            parts = command.split()
            if len(parts) < 2:
                print("Укажите смещение.")
                continue
            try:
                current_offset = int(parts[1], 16)
                display_page(file_data, current_offset)
            except ValueError:
                print("Неверный формат смещения.")
        elif command == "edit":
            edit_byte(file_data)
        elif command == "search":
            search_data(file_data)
        elif command == "save":
            save_file(filename, file_data)
        elif command == "help":
            print_help()
        elif command == "quit":
            answer = input("Сохранить изменения перед выходом? "
                           "(y/n): ").strip().lower()
            if answer == 'y':
                save_file(filename, file_data)
            print("Выход из редактора.")
            break
        else:
            print("Неизвестная команда. Введите 'help' для "
                  "списка команд.")


if __name__ == "__main__":
    main()
