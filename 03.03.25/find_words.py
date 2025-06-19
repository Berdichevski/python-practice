import random
import string
import time


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f'Execution time: {time.time() - start}')
        return result

    return wrapper

def generate_words(word_count: int, avg_len_words: int) -> list[str]:
    word_list: list[str] = []
    for _ in range (word_count):
        length1: int = random.randint(avg_len_words - 2, avg_len_words + 2)
        word: str = "".join(random.choices(string.ascii_lowercase, k = length1))
        word_list.append(word)
    return word_list

@timeit
def find_matching_pair_bruteforce(words: list[str]) -> tuple[str, str]:
    max_len = 0
    pair = tuple
    for word_pref in words:
        for word_suf in words:
            if word_pref != word_suf:
                for i in range(len(word_pref)):
                    if word_pref[:i] == word_suf[-i:]:
                        if i > max_len:
                            max_len = i
                            pair = (word_pref, word_suf)
    return pair

@timeit
def find_matching_pair_dict(words: list[str]) -> tuple[str, str]:
    dict = {}
    max_len = 0
    pair = tuple
    for word in words:
        for i in range (len(word)):
            dict[word[:i]] = word
    for word in words:
        for i in range (len(word)):
            if word[-i:] in dict and i > max_len:
                max_len = i
                pair = (dict[word[-i:]], word)
    return pair


if __name__ == "__main__":
    num = 500
    length = 10
    words = generate_words(num, length)
    print (find_matching_pair_bruteforce(words))
    print (find_matching_pair_dict(words))
