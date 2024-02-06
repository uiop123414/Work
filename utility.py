import random

def is_valid_word(word):
    # Проверяем, что слово состоит из букв и длина больше 3 символов
    return word.isalpha() and len(word) > 3

def choose_random_word(text):
    # Список слов для выбора
    word_list = text.split(" ")

    # Отфильтровываем слова, соответствующие условиям
    valid_words = [word for word in word_list if is_valid_word(word)]

    # Выбираем случайное слово из отфильтрованного списка
    random_word = random.choice(valid_words)

    return random_word


