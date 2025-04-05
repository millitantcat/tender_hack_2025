import redis
import uuid
import json
import os

# Получаем настройки для подключения к Redis из переменных окружения
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Создаём клиента Redis с автоматическим декодированием строк
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

# Префиксы для ключей в Redis, чтобы разделять сессии и follow-up действия
SESSION_PREFIX = "chat_session:"
FOLLOWUP_PREFIX = "followup:"

def create_session() -> str:
    """
    Создаёт новую сессию с уникальным ID и сохраняет пустую историю чата в Redis.
    Возвращает идентификатор сессии.
    """
    session_id = str(uuid.uuid4())  # Генерируем уникальный UUID
    redis_client.set(f"{SESSION_PREFIX}{session_id}", json.dumps([]))  # Сохраняем пустой список как историю
    return session_id

def get_session_history(session_id: str) -> list:
    """
    Получает историю сообщений по заданной сессии.
    Возвращает список словарей (история сообщений).
    """
    data = redis_client.get(f"{SESSION_PREFIX}{session_id}")
    if data:
        return json.loads(data)  # Преобразуем строку JSON обратно в список
    return []  # Если данных нет — возвращаем пустой список

def add_to_session(session_id: str, user_msg: str, bot_response: dict):
    """
    Добавляет сообщение пользователя и ответ бота в историю текущей сессии.
    Сохраняет обновлённую историю обратно в Redis.
    """
    history = get_session_history(session_id)  # Загружаем текущую историю
    history.append({
        "user": user_msg,
        "bot": bot_response
    })  # Добавляем новую пару сообщений
    redis_client.set(f"{SESSION_PREFIX}{session_id}", json.dumps(history))  # Сохраняем обратно

def set_followup_key(session_id: str, key: str):
    """
    Сохраняет ключ следующего действия (follow-up) для конкретной сессии.
    """
    redis_client.set(f"{FOLLOWUP_PREFIX}{session_id}", key)

def get_followup_key(session_id: str) -> str:
    """
    Получает текущий follow-up ключ по сессии.
    """
    return redis_client.get(f"{FOLLOWUP_PREFIX}{session_id}")

def clear_followup_key(session_id: str):
    """
    Удаляет follow-up ключ для указанной сессии.
    """
    redis_client.delete(f"{FOLLOWUP_PREFIX}{session_id}")
