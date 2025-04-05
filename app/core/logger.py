import datetime

# Путь к файлу логирования взаимодействий
LOG_FILE = "log/interaction_log.txt"

def log_interaction(query, intent, category, action):
    """
    Логирует взаимодействие пользователя с ассистентом в текстовый файл.

    :param query: Исходный запрос пользователя
    :param intent: Определённый интент
    :param category: Категория, к которой отнесён запрос
    :param action: Выполненное действие или найденный ответ
    """
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] QUERY: {query} | INTENT: {intent} | CATEGORY: {category} | ACTION: {action}\n")
