import os
import json
from app.utils.nlp import match_keywords

# === Загрузка баз знаний ===
BASE_DIR = os.path.dirname(__file__)
data_path = lambda name: os.path.join(BASE_DIR, "..", "data", name)

with open(data_path("knowledge.json"), "r", encoding="utf-8") as f:
    KNOWLEDGE = json.load(f)

with open(data_path("knowledge_articles.json"), "r", encoding="utf-8") as f:
    USER_ARTICLES = json.load(f)

with open(data_path("extended_knowledge.json"), "r", encoding="utf-8") as f:
    EXTENDED_KNOWLEDGE = json.load(f)

# === Основной поиск по ключевым словам ===
def search_knowledge(input_keywords: list) -> dict:
    # 1. Основная база
    for category, info in KNOWLEDGE.items():
        if match_keywords(input_keywords, info.get("keywords", [])):
            response_data = info.get("response")

            # ➕ Обработка случая с отсутствующим "response", но есть default_response
            if not response_data:
                response_data = {
                    "text": info.get("default_response", "Информация найдена, но ответ не определён."),
                    "key": None,
                    "url": None
                }

            return {
                "category": category,
                "action": "Прямое совпадение по категории",
                "answer": response_data
            }

        # 1.1 Подкатегории
        for subcat, subinfo in info.get("subcategories", {}).items():
            if match_keywords(input_keywords, subinfo.get("keywords", [])):
                response = subinfo["response"] if isinstance(subinfo["response"], dict) else {
                    "text": subinfo["response"],
                    "key": None,
                    "url": None
                }

                return {
                    "category": category,
                    "action": f"Найдена подкатегория: {subcat}",
                    "answer": response
                }

    # 2. Пользовательские статьи
    for article in USER_ARTICLES:
        if match_keywords(input_keywords, article.get("keywords", [])):
            return {
                "category": "вопросы пользователей",
                "action": "Ответ из статьи",
                "answer": article["response"]
            }

    # 3. Навигационные записи
    for nav in EXTENDED_KNOWLEDGE:
        if match_keywords(input_keywords, nav.get("keywords", [])):
            return {
                "category": "навигация",
                "action": "Навигационная статья",
                "answer": nav["response"]
            }

    # 4. Fallback
    return {
        "category": "unknown",
        "action": "not found",
        "answer": {
            "text": "Информация не найдена. Попробуйте переформулировать запрос.",
            "key": "Написать в поддержку",
            "url": "https://zakupki.mos.ru/feedback"
        }
    }
