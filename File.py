import math
import re


class File:
    def __init__(self, path):
        self.path = path
        self.words_count = {}
        self.calculate_words_count()
        self.words_weight_coef = {}
        self.words_weight = {}
        self.eq_rate = 0
        self.words_from_search = []

    def calculate_words_count(self) -> None:
        with open(self.path, 'r') as file:
            for row in file:
                row = re.sub(r'[^\w\s]', '', row).lower()
                for word in row.split():
                    if word in self.words_count.keys():
                        self.words_count[word] += 1
                    else:
                        self.words_count[word] = 1

    def calculate_words_weight_coef(self, files_word_count: dict, files_count: int) -> None:
        for word in files_word_count.keys():
            if files_word_count[word] == 1 and files_count == 1:
                self.words_weight_coef[word] = 1
            else:
                self.words_weight_coef[word] = self.words_count[word] * math.log(files_count/files_word_count[word])

    def calculate_words_weight(self, files_weight_coef_list: list) -> None:
        coef_sum = {}
        for word in self.words_weight_coef.keys():
            for file in files_weight_coef_list:
                if word in file.keys():
                    if word in coef_sum.keys():
                        coef_sum[word] += file[word] ** 2
                    else:
                        coef_sum[word] = file[word] ** 2

        for word in self.words_weight_coef.keys():
            self.words_weight[word] = self.words_weight_coef[word] / math.sqrt(coef_sum[word]) \
                if not coef_sum[word] == 0 else 0

    def set_eq_rate(self, value: float) -> None:
        self.eq_rate = value
