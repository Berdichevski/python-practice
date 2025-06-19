import string
import unittest
import find_words

# Вспомогательные функции для тестов
def get_match_length(a: str, b: str) -> int:
    max_match = 0
    for i in range(1, min(len(a), len(b)) + 1):
        if a[:i] == b[-i:]:
            max_match = i
    return max_match

def overall_max_match(words: list[str]) -> int:
    max_match = 0
    for i in range(len(words)):
        for j in range(len(words)):
            if i != j:
                match = get_match_length(words[i], words[j])
                if match > max_match:
                    max_match = match
    return max_match

# Тесты

class TestGenerateWords(unittest.TestCase):
    def test_word_count(self):
        words = find_words.generate_words(10, 5)
        self.assertEqual(len(words), 10)

    def test_word_length(self):
        avg_len = 5
        words = find_words.generate_words(100, avg_len)
        for word in words:
            self.assertGreaterEqual(len(word), avg_len - 2)
            self.assertLessEqual(len(word), avg_len + 2)

    def test_characters(self):
        words = find_words.generate_words(20, 6)
        for word in words:
            for char in word:
                self.assertIn(char, string.ascii_lowercase)


class TestMatchingPairBfFunctions(unittest.TestCase):

    def setUp(self):
        # Стандартный тестовый набор слов
        self.words = ["abcd", "xyzab", "abcde", "ab", "hello", "lo"]
        self.pair = find_words.find_matching_pair_bruteforce(self.words)
        if self.pair is not None:
            self.a, self.b = self.pair

    def test_words_in_list_and_distinct(self):
        # Проверяем, что выбранная пара слов принадлежит исходному списку и слова различны
        self.assertIn(self.a, self.words)
        self.assertIn(self.b, self.words)
        self.assertNotEqual(self.a, self.b)

    def test_match_length_equals_expected_max(self):
        # Проверяем, что длина совпадения между выбранными словами равна общему максимальному
        match_length = get_match_length(self.a, self.b)
        expected_max = overall_max_match(self.words)
        self.assertEqual(match_length, expected_max)

    def test_non_english_words(self):
        # Тест с неанглийскими словами (например, на русском)
        words = ["привет", "мир", "тест", "ветер", "мерить"]
        pair = find_words.find_matching_pair_bruteforce(words)
        if len(words) < 2:
            self.assertIsNone(pair)
        else:
            self.assertIsNotNone(pair)
            a, b = pair
            self.assertIn(a, words)
            self.assertIn(b, words)
            self.assertNotEqual(a, b)
            self.assertEqual(get_match_length(a, b), overall_max_match(words))

    def test_capital_letters(self):
        # Тест со словами, содержащими заглавные буквы
        words = ["Hello", "World", "HELLO", "world"]
        pair = find_words.find_matching_pair_bruteforce(words)
        if len(words) < 2:
            self.assertIsNone(pair)
        else:
            self.assertIsNotNone(pair)
            a, b = pair
            self.assertIn(a, words)
            self.assertIn(b, words)
            self.assertNotEqual(a, b)
            self.assertEqual(get_match_length(a, b), overall_max_match(words))

    def test_single_word(self):
        # Тест со списком, содержащим только одно слово
        words = ["singleton"]
        pair = find_words.find_matching_pair_bruteforce(words)
        self.assertIsNone(pair)

    def test_empty_list(self):
        # Тест с пустым списком
        words = []
        pair = find_words.find_matching_pair_bruteforce(words)
        self.assertIsNone(pair)


class TestMatchingPairDictFunctions(unittest.TestCase):

    def setUp(self):
        # Стандартный тестовый набор слов
        self.words = ["abcd", "xyzab", "abcde", "ab", "hello", "lo"]
        self.pair = find_words.find_matching_pair_dict(self.words)
        if self.pair is not None:
            self.a, self.b = self.pair

    def test_words_in_list_and_distinct(self):
        # Проверяем, что выбранная пара слов принадлежит исходному списку и слова различны
        self.assertIn(self.a, self.words)
        self.assertIn(self.b, self.words)
        self.assertNotEqual(self.a, self.b)

    def test_match_length_equals_expected_max(self):
        # Проверяем, что длина совпадения между выбранными словами равна общему максимальному
        match_length = get_match_length(self.a, self.b)
        expected_max = overall_max_match(self.words)
        self.assertEqual(match_length, expected_max)

    def test_non_english_words(self):
        # Тест с неанглийскими словами (например, на русском)
        words = ["привет", "мир", "тест", "ветер", "мерить"]
        pair = find_words.find_matching_pair_dict(words)
        if len(words) < 2:
            self.assertIsNone(pair)
        else:
            self.assertIsNotNone(pair)
            a, b = pair
            self.assertIn(a, words)
            self.assertIn(b, words)
            self.assertNotEqual(a, b)
            self.assertEqual(get_match_length(a, b), overall_max_match(words))

    def test_capital_letters(self):
        # Тест со словами, содержащими заглавные буквы
        words = ["Hello", "World", "HELLO", "world"]
        pair = find_words.find_matching_pair_dict(words)
        if len(words) < 2:
            self.assertIsNone(pair)
        else:
            self.assertIsNotNone(pair)
            a, b = pair
            self.assertIn(a, words)
            self.assertIn(b, words)
            self.assertNotEqual(a, b)
            self.assertEqual(get_match_length(a, b), overall_max_match(words))

    def test_single_word(self):
        # Тест со списком, содержащим только одно слово
        words = ["singleton"]
        pair = find_words.find_matching_pair_dict(words)
        self.assertIsNone(pair)

    def test_empty_list(self):
        # Тест с пустым списком
        words = []
        pair = find_words.find_matching_pair_dict(words)
        self.assertIsNone(pair)

if __name__ == '__main__':
    unittest.main()
