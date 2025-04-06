
from app.core.classifier import classify_intent
from app.core.knowledge_base import search_knowledge
from app.core.logger import log_interaction
from app.core.session_manager import (
    create_session, get_session_history, add_to_session,
    get_followup_key, set_followup_key, clear_followup_key
)
from app.utils.nlp import clean_text, extract_keywords, match_keywords
import json
import os

# Загрузка базы знаний
with open(os.path.join(os.path.dirname(__file__), "..", "data", "knowledge.json"), "r", encoding="utf-8") as f:
    KNOWLEDGE = json.load(f)


def handle_query(text, session_id=None):
    """
    Базовая функция обработки пользовательского запроса:
    - Предобработка
    - Классификация намерения
    - Поиск ответа в базе знаний
    - Управление follow-up
    """

    cleaned = clean_text(text)
    keywords = extract_keywords(cleaned)

    if not session_id:
        session_id = create_session()

    follow_key = get_followup_key(session_id)
    if follow_key and follow_key in KNOWLEDGE:
        subcats = KNOWLEDGE[follow_key].get("subcategories", {})

        for subcat_name, subcat_data in subcats.items():
            if match_keywords(keywords, subcat_data.get("keywords", [])):
                clear_followup_key(session_id)
                response = {
                    "category": follow_key,
                    "intent": "follow-up",
                    "action": f"Follow-up: {subcat_name}",
                    "answer": subcat_data["response"],
                    "session_id": session_id
                }
                add_to_session(session_id, text, response)
                return response

    intent = classify_intent(cleaned)
    action_data = search_knowledge(keywords)

    category_data = KNOWLEDGE.get(action_data["category"])
    if category_data and category_data.get("follow_up_expected"):
        set_followup_key(session_id, category_data.get("follow_up_key"))
    else:
        clear_followup_key(session_id)

    response = {
        "category": action_data.get("category"),
        "intent": intent,
        "action": action_data.get("action"),
        "answer": action_data.get("answer"),
        "session_id": session_id
    }

    log_interaction(text, intent, action_data.get("category"), action_data.get("action"))
    add_to_session(session_id, text, response)

    return response
