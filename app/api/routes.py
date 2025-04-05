from fastapi import APIRouter
from app.models.schemas import UserQuery, AssistantResponse
from app.core.processor import handle_query

router = APIRouter()


@router.post(
    "/query",
    response_model=AssistantResponse,
    summary="Отправка запроса ассистенту",
    description=(
        "Обрабатывает пользовательский запрос и возвращает ответ от интеллектуального ассистента.\n\n"
        "Ассистент использует машинное обучение и логические правила для определения категории запроса "
        "и формирования ответа."
    ),
    tags=["Assistant"]
)
def query_assistant(user_query: UserQuery):
    """
    Отправить текстовый запрос ассистенту.

    - **query**: Текст запроса от пользователя
    - **session_id**: Идентификатор сессии (используется для отслеживания контекста диалога)

    Возвращает ответ ассистента, содержащий текст и дополнительную информацию.
    """
    result = handle_query(user_query.query, user_query.session_id)
    return result
