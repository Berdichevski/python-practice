import unittest
import requests
import random
import string
import sys
sys.stdout.reconfigure(encoding='utf-8')


class api_test(unittest.TestCase):
    BASE_URL = "https://plenty-readers-poke.loca.lt/suggest"
    HEADERS = {
        'User-Agent': 'MyUserAgent/1.0',
        'Authorization': 'Bearer some_token'
    }

    def get_words(self, prefix=""):
        """Функция для получения слов по указанному префиксу."""
        response = requests.get(self.BASE_URL, headers=self.HEADERS, params={'w': prefix})
        self.assertEqual(response.status_code, 200, f"Ошибка запроса с параметром w= {prefix} ")
        return response.text.strip().split("\n")

    def generate_prefixes(self, count=15, max_length=4):
        """Генерирует список случайных префиксов длиной до 4 символов."""
        prefixes = set()
        while len(prefixes) < count:
            prefix = ''.join(random.choices(string.ascii_lowercase, k=random.randint(1, max_length)))
            prefixes.add(prefix)

        print(f"testing on prefixes: {prefixes}")
        return list(prefixes)

    def test_get_all_words(self):
        """Проверяем, что API возвращает список всех слов при пустом параметре 'w'."""
        all_words = self.get_words("")
        self.assertIsInstance(all_words, list)
        self.assertGreater(len(all_words), 0, "Список слов должен быть непустым")

        # Сохраняем полный список слов для дальнейших тестов
        self.all_words = all_words

    def test_get_words_by_prefix(self):
        """Проверяем, что API возвращает только слова с указанным префиксом."""
        all_words = self.get_words("")
        test_prefixes = self.generate_prefixes()

        for prefix in test_prefixes:
            filtered_words = self.get_words(prefix)
            expected_words = [word for word in all_words if word.startswith(prefix)]
            if (expected_words == []):
                expected_words = ['']
            self.assertListEqual(sorted(filtered_words), sorted(expected_words), "Ошибка для префикса '{prefix}'")


if __name__ == "__main__":
    unittest.main()
