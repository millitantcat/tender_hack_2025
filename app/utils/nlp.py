from fuzzywuzzy import fuzz
from rapidfuzz import fuzz
import re

def clean_text(text):
    """
    Приводит текст к нижнему регистру и удаляет пробелы по краям.

    :param text: Входной текст
    :return: Очищенный текст
    """
    return text.lower().strip()

def extract_keywords(text):
    """
    Делит строку на отдельные слова по пробелам.

    :param text: Входной текст
    :return: Список слов (предположительно ключевых)
    """
    return text.split()


def match_keywords(input_words, keyword_list, threshold=80):
    """
    Сопоставляет слова из входного списка с ключевыми словами по принципу нечёткого сравнения.

    :param input_words: Список слов из пользовательского ввода
    :param keyword_list: Список эталонных ключевых слов
    :param threshold: Порог совпадения для fuzzy matching (от 0 до 100)
    :return: Список уникальных совпавших ключевых слов
    """
    matches = []
    for word in input_words:
        for keyword in keyword_list:
            # Используем частичное сравнение строк, например: "госзаказ" ≈ "государственный заказ"
            if fuzz.partial_ratio(word, keyword) >= threshold:
                matches.append(keyword)
    return list(set(matches))  # Убираем дубликаты


def keyword_similarity_score(input_keywords: list, target_keywords: list) -> float:
    if not input_keywords or not target_keywords:
        return 0.0
    input_set = set(k.lower() for k in input_keywords)
    target_set = set(k.lower() for k in target_keywords)
    intersection = input_set & target_set
    union = input_set | target_set
    return len(intersection) / len(union) if union else 0.0



def tokenize_text(text: str) -> list:
    """
    Преобразует текст в список токенов: убирает спецсимволы, приводит к нижнему регистру.
    """
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)  # удаляем знаки препинания
    tokens = text.split()
    return tokens
