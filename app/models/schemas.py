from pydantic import BaseModel, Field
from typing import Optional

class UserQuery(BaseModel):
    query: str = Field(..., description="Текст запроса от пользователя")
    session_id: Optional[str] = Field(
        None, description="Уникальный идентификатор сессии пользователя (если требуется сохранить контекст)"
    )

class AnswerBlock(BaseModel):
    text: str = Field(..., description="Текст, возвращённый ассистентом в ответ на запрос")
    key: Optional[str] = Field(
        None, description="Ключевой параметр или идентификатор, связанный с ответом (если применимо)"
    )
    url: Optional[str] = Field(
        None, description="Ссылка на дополнительный ресурс или источник информации (если доступно)"
    )

class AssistantResponse(BaseModel):
    category: str = Field(..., description="Категория запроса, определённая ассистентом")
    intent: str = Field(..., description="Выявленное намерение (интент) пользователя")
    action: str = Field(..., description="Действие, которое должен выполнить ассистент")
    answer: AnswerBlock = Field(..., description="Структурированный ответ ассистента")
    session_id: str = Field(..., description="Идентификатор сессии (повторяется из запроса)")
