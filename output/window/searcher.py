import math
import os
from File import File


def get_folders_content() -> list:
    files_path_list = []

    for path, _, filenames in os.walk('share'):
        for file in filenames:
            if file.endswith('.txt'):
                files_path_list.append(os.path.join(path, file))

    return files_path_list


def get_files_list(files_path_list: list) -> list:
    files_list = [File(file_path) for file_path in files_path_list]
    return files_list


def calculate_files_words_weight_coef(files_list: list):
    for file in files_list:
        for word in file.words_count.keys():
            file.calculate_words_weight_coef({word: len(get_files_with_word(word, files_list))}, len(files_list))


def get_files_with_word(word: str, files_list: list) -> list:
    files_with_word = []
    for file in files_list:
        if word.lower().strip() in file.words_count.keys():
            files_with_word.append(file)
    return files_with_word


def calculate_files_words_weight(files: list):
    files_weight_coefs = [file.words_weight_coef for file in files]
    for file in files:
        file.calculate_words_weight(files_weight_coefs)


def eq_rating(files: list, search: str):
    calculate_files_words_weight_coef(files)
    calculate_files_words_weight(files)
    search_list = set(search.lower().split())
    for file in files:
        file.words_from_search = [word for word in file.words_weight.keys() if word in search_list]
        numerator = sum([file.words_weight[word] for word in file.words_weight.keys() if word in search_list])
        denominator = math.sqrt(sum([file.words_weight[word] ** 2 for word in file.words_weight.keys()])) * \
                      math.sqrt(sum([1 for word in search_list]))
        file.set_eq_rate(numerator/denominator)


def sort_key(file):
    return file.eq_rate


def main(path: str, search: str):
    files = get_files_list(get_folders_content())
    eq_rating(files, search)
    return sorted(files, key=sort_key, reverse=True)
