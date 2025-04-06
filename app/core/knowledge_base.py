import os
import json
from app.utils.nlp import keyword_similarity_score  # Новая функция вместо match_keywords

# Загрузка баз знаний
BASE_DIR = os.path.dirname(__file__)
data_path = lambda name: os.path.join(BASE_DIR, "..", "data", name)

with open(data_path("knowledge.json"), "r", encoding="utf-8") as f:
    KNOWLEDGE = json.load(f)

with open(data_path("knowledge_articles.json"), "r", encoding="utf-8") as f:
    USER_ARTICLES = json.load(f)

with open(data_path("extended_knowledge.json"), "r", encoding="utf-8") as f:
    EXTENDED_KNOWLEDGE = json.load(f)

# Основной поиск по лучшему совпадению
def search_knowledge(input_keywords: list) -> dict:
    best_match = {"score": 0, "result": None}

    def update_best(score, result):
        if score > best_match["score"]:
            best_match["score"] = score
            best_match["result"] = result

    # 1. Основная база
    for category, info in KNOWLEDGE.items():
        score = keyword_similarity_score(input_keywords, info.get("keywords", []))
        if score > 0.7:
            response_data = info.get("response") or {
                "text": info.get("default_response", "Информация найдена, но ответ не определён."),
                "key": None,
                "url": None
            }
            return {
                "category": category,
                "action": "Прямое совпадение по категории",
                "answer": response_data
            }
        update_best(score, {
            "category": category,
            "action": "Похожая категория",
            "answer": info.get("response") or {
                "text": info.get("default_response", "Информация найдена, но ответ не определён."),
                "key": None,
                "url": None
            }
        })

        # 1.1 Подкатегории
        for subcat, subinfo in info.get("subcategories", {}).items():
            score = keyword_similarity_score(input_keywords, subinfo.get("keywords", []))
            if score > 0.7:
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
            update_best(score, {
                "category": category,
                "action": f"Похожая подкатегория: {subcat}",
                "answer": subinfo["response"] if isinstance(subinfo["response"], dict) else {
                    "text": subinfo["response"],
                    "key": None,
                    "url": None
                }
            })

    # 2. Пользовательские статьи
    for article in USER_ARTICLES:
        score = keyword_similarity_score(input_keywords, article.get("keywords", []))
        if score > 0.7:
            return {
                "category": "вопросы пользователей",
                "action": "Ответ из статьи",
                "answer": article["response"]
            }
        update_best(score, {
            "category": "вопросы пользователей",
            "action": "Похожая пользовательская статья",
            "answer": article["response"]
        })

    # 3. Навигационные записи
    for nav in EXTENDED_KNOWLEDGE:
        score = keyword_similarity_score(input_keywords, nav.get("keywords", []))
        if score > 0.7:
            return {
                "category": "навигация",
                "action": "Навигационная статья",
                "answer": nav["response"]
            }
        update_best(score, {
            "category": "навигация",
            "action": "Похожая навигационная статья",
            "answer": nav["response"]
        })

    # 4. Лучшее приближенное совпадение
    if best_match["result"]:
        best_match["result"]["action"] += f" (схожесть: {best_match['score']:.2f})"
        return best_match["result"]

    # 5. Fallback
    return {
        "category": "unknown",
        "action": "not found",
        "answer": {
            "text": "Информация не найдена. Попробуйте переформулировать запрос.",
            "key": "Написать в поддержку",
            "url": "https://zakupki.mos.ru/feedback"
        }
    }
