import os
import re
import math


def get_folders_content(path: str) -> list:
    files_path_list = []

    for path, _, filenames in os.walk(path):
        for file in filenames:
            if file.endswith('.txt'):
                if not path.endswith('/'):
                    path += '/'
                files_path_list.append(path + file)

    return files_path_list


def calculations_for_file(path: str) -> dict:
    metrics = {}
    with open(path, 'r') as file:
        for row in file:
            row = re.sub(r'[^\w\s]', '', row).lower()
            for word in row.split():
                if word in metrics.keys():
                    metrics[word] += 1
                else:
                    metrics[word] = 1
    return metrics


def get_metrics(path: str) -> dict:
    metrics_dict = {}
    for file in get_folders_content(path):
        metrics_dict[file] = calculations_for_file(file)

    return metrics_dict


def get_files_with_word(word: str, metrics_dict: dict) -> list:
    files_with_word = []
    for file in metrics_dict.keys():
        if word.lower().strip() in metrics_dict[file].keys():
            files_with_word.append({file: metrics_dict[file]})
    return files_with_word


def get_files_depends_on_request(find_list: list) -> list:
    final_list = []
    for word in find_list:
        for i in get_files_with_word(word, get_metrics('./test')):
            if i not in final_list:
                final_list += get_files_with_word(word, get_metrics('./test'))

    return final_list


def word_weight(word: str, path: str) -> dict:
    files_metrics = get_files_with_word(word, get_metrics(path))
    docs_count = len(files_metrics)
    files_count = len(get_folders_content(path))
    weight = 0
    files_word_weight = {}
    for file_metrics in files_metrics:
        for file in file_metrics.keys():
            all_words_weight = 0
            for w in file_metrics[file].keys():
                all_words_weight += (file_metrics[file][w] *
                                     math.log(files_count/len(get_files_with_word(w, get_metrics(path))))) ** 2
            weight = (file_metrics[file][word] * math.log(files_count/docs_count)) /



def main():
    find_list = input('words to find: ').split(' ')
    print(get_files_depends_on_request(find_list))


if __name__ == '__main__':
    main()
