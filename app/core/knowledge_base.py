
import os
import json
import difflib

# Путь к данным
BASE_DIR = os.path.dirname(__file__)
data_path = lambda name: os.path.join(BASE_DIR, "..", "data", name)

# Загрузка основной базы знаний
with open(data_path("knowledge.json"), "r", encoding="utf-8") as f:
    KNOWLEDGE = json.load(f)

# Fuzzy-сравнение по ключевым словам с использованием difflib
def keyword_similarity_score(input_keywords: list, target_keywords: list) -> float:
    matches = 0
    for kw in input_keywords:
        if difflib.get_close_matches(kw.lower(), [k.lower() for k in target_keywords], n=1, cutoff=0.7):
            matches += 1
    return matches / max(len(input_keywords), 1)

# Основной поиск по базе знаний
def search_knowledge(input_keywords: list) -> dict:
    best_match = {"score": 0, "result": None}

    def update_best(score, result):
        if score > best_match["score"]:
            best_match["score"] = score
            best_match["result"] = result

    for category, info in KNOWLEDGE.items():
        # Сначала ищем по подкатегориям
        for subcat, subinfo in info.get("subcategories", {}).items():
            score = keyword_similarity_score(input_keywords, subinfo.get("keywords", []))
            if score > 0.5:
                return {
                    "category": category,
                    "action": f"Найдена подкатегория: {subcat}",
                    "answer": subinfo["response"]
                }
            update_best(score, {
                "category": category,
                "action": f"Похожая подкатегория: {subcat}",
                "answer": subinfo["response"]
            })

        # Затем — по категории
        score = keyword_similarity_score(input_keywords, info.get("keywords", []))
        if score > 0.5:
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

    if best_match["result"]:
        best_match["result"]["action"] += f" (схожесть: {best_match['score']:.2f})"
        return best_match["result"]

    return {
        "category": "unknown",
        "action": "not found",
        "answer": {
            "text": "Информация не найдена. Попробуйте переформулировать запрос.",
            "key": "Написать в поддержку",
            "url": "https://zakupki.mos.ru/feedback"
        }
    }
