import math
import os
import sys
import numpy as np
from File import File
import socket


def get_folders_content(path: str) -> list:
    files_path_list = []

    for path, _, filenames in os.walk(path):
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


def start_socket():
    sock = socket.socket()
    sock.bind(('', 9090))
    sock.listen(5)
    conn, addr = sock.accept()
    print(f'connected: {addr}')
    while True:
        # print('*')
        size_recv = conn.recv(8)
        # print(size_recv)
        if not size_recv:
            continue
        search_size = int.from_bytes(size_recv, 'big')
        search_string = conn.recv(search_size).decode(encoding='utf-8')
        files = get_files_list(get_folders_content())
        eq_rating(files, search_string)
        result = [[file.path, file.eq_rate] for file in sorted(files, key=sort_key, reverse=True)]
        result = np.array(result)
        result_size = sys.getsizeof(result)
        result_size_bytes = result_size.to_bytes(2, byteorder='big')
        conn.send(result_size_bytes)
        conn.send(result.tobytes())


def main():
    # start_socket()
    files = get_files_list(get_folders_content('/home/monstrillllo/EYAZIS/share'))
    eq_rating(files, 'sex')
    files.sort(key=sort_key, reverse=True)
    for file in files:
        print(f'{file.path} - {file.eq_rate}')


if __name__ == '__main__':
    main()
