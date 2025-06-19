import unittest
from unittest import mock
import os
from hex_editor import display_page, edit_byte, search_data, save_file, \
    print_help


class TestHexEditor(unittest.TestCase):
    def setUp(self):
        self.file_data = bytearray([
            0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x20,
            0x57, 0x6F, 0x72, 0x6C, 0x64, 0x21
        ])
        self.filename = 'testfile.bin'
        with open(self.filename, 'wb') as f:
            f.write(self.file_data)

    def tearDown(self):
        try:
            os.remove(self.filename)
        except Exception as e:
            print(f"Ошибка удаления файла: {e}")

    def test_display_page(self):
        with mock.patch('builtins.print') as mocked_print:
            display_page(self.file_data, 0)
            mocked_print.assert_any_call("Offset | HEX                        "
                                         "                    | ASCII")
            mocked_print.assert_any_call("------------------------------------"
                                         "-------------------"
                                         "-------------------")

    def test_display_page_invalid_offset(self):
        """Тестируем случай, когда смещение больше, чем размер файла."""
        with mock.patch('builtins.print') as mocked_print:
            display_page(self.file_data, len(self.file_data) + 1)
            mocked_print.assert_any_call("Offset | HEX                        "
                                         "                    | ASCII")

    def test_edit_byte_valid(self):
        with mock.patch('builtins.input', side_effect=["000004", "41"]):
            edit_byte(self.file_data)
        self.assertEqual(self.file_data[4], 0x41)

    def test_edit_byte_invalid_offset(self):
        with mock.patch('builtins.input', side_effect=["001000", "20"]):
            with mock.patch('builtins.print') as mocked_print:
                edit_byte(self.file_data)
                mocked_print.assert_any_call("Неверное смещение.")

    def test_edit_byte_invalid_hex(self):
        with mock.patch('builtins.input', side_effect=["000004", "ZZ"]):
            with mock.patch('builtins.print') as mocked_print:
                try:
                    edit_byte(self.file_data)
                except ValueError:
                    pass
                mocked_print.assert_any_call("Ошибка редактирования:",
                                             mock.ANY)

    def test_edit_byte_empty_input(self):
        with mock.patch('builtins.input', side_effect=["000004", ""]):
            with mock.patch('builtins.print') as mocked_print:
                edit_byte(self.file_data)
                mocked_print.assert_any_call("Неверный формат. Должно быть "
                                             "2 шестнадцатеричных символа.")

    def test_search_ascii_found(self):
        with mock.patch('builtins.input', side_effect=["ascii", "World"]):
            with mock.patch('builtins.print') as mocked_print:
                search_data(self.file_data)
                mocked_print.assert_any_call("Паттерн найден по смещению: "
                                             "000006")

    def test_search_ascii_not_found(self):
        with mock.patch('builtins.input', side_effect=["ascii", "NotFound"]):
            with mock.patch('builtins.print') as mocked_print:
                search_data(self.file_data)
                mocked_print.assert_any_call("Паттерн не найден.")

    def test_search_hex_valid_found(self):
        with mock.patch('builtins.input', side_effect=["hex", "57 6F 72"]):
            with mock.patch('builtins.print') as mocked_print:
                search_data(self.file_data)
                mocked_print.assert_any_call("Паттерн найден по смещению: "
                                             "000006")

    def test_search_hex_invalid_format(self):
        with mock.patch('builtins.input', side_effect=["hex", "invalid hex"]):
            with mock.patch('builtins.print') as mocked_print:
                search_data(self.file_data)
                mocked_print.assert_any_call("Неверный формат HEX.")

    def test_search_hex_empty_input(self):
        with mock.patch('builtins.input', side_effect=["hex", ""]):
            with mock.patch('builtins.print') as mocked_print:
                search_data(self.file_data)
                mocked_print.assert_any_call("Неверный формат HEX.")

    def test_save_file(self):
        modified_data = bytearray([0xAA] * len(self.file_data))
        save_file(self.filename, modified_data)

        with open(self.filename, 'rb') as f:
            result = f.read()
        self.assertEqual(result, modified_data)

    def test_save_file_error(self):
        with mock.patch('builtins.print') as mocked_print:
            save_file('/non_existent_dir/testfile.bin', self.file_data)
            mocked_print.assert_any_call("Ошибка сохранения файла:", mock.ANY)

    def test_next_command(self):
        with mock.patch('builtins.input', side_effect=["next"]):
            with mock.patch('builtins.print') as mocked_print:
                current_offset = 0
                page_size = 16 * 16
                current_offset += page_size
                display_page(self.file_data, current_offset)
                mocked_print.assert_any_call("Offset | HEX                    "
                                             "                        | ASCII")

    def test_prev_command(self):
        with mock.patch('builtins.input', side_effect=["prev"]):
            with mock.patch('builtins.print') as mocked_print:
                current_offset = 16 * 16
                page_size = 16 * 16
                current_offset -= page_size
                display_page(self.file_data, current_offset)
                mocked_print.assert_any_call("Offset | HEX                    "
                                             "                        | ASCII")

    def test_goto_command(self):
        with mock.patch('builtins.input', side_effect=["goto 000010"]):
            with mock.patch('builtins.print') as mocked_print:
                current_offset = 0
                new_offset = 16
                display_page(self.file_data, new_offset)
                mocked_print.assert_any_call("Offset | HEX                    "
                                             "                        | ASCII")

    def test_help_command(self):
        with mock.patch('builtins.input', side_effect=["help"]):
            with mock.patch('builtins.print') as mocked_print:
                print_help()
                mocked_print.assert_any_call("""
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


if __name__ == "__main__":
    unittest.main()
