import json
import os
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Определим базу для обучения
TRAIN_DATA = []

# Загружаем файл, содержащий основную структуру категорий и подкатегорий
with open("../data/knowledge.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    for intent, info in data.items():
        # Добавляем ключевые слова, относящиеся к основной категории
        TRAIN_DATA += [(kw, intent) for kw in info.get("keywords", [])]
        if "subcategories" in info:
            for subname, subdata in info["subcategories"].items():
                # Также добавляем ключевые слова из подкатегорий
                TRAIN_DATA += [(kw, intent) for kw in subdata.get("keywords", [])]

# Загружаем дополнительный источник знаний — пользовательские статьи
with open("../data/knowledge_articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)
    # Все ключевые слова из статей относятся к намерению "документация"
    TRAIN_DATA += [(kw, "документация") for article in articles for kw in article.get("keywords", [])]

# Загружаем навигационные элементы, например: переходы по сайту, разделы
with open("../data/extended_knowledge.json", "r", encoding="utf-8") as f:
    nav = json.load(f)
    TRAIN_DATA += [(kw, "навигация") for item in nav for kw in item.get("keywords", [])]

# Добавляем вручную список слов/фраз, которые заведомо не относятся к теме
irrelevant = [
    "кот", "погода", "анекдот", "что такое любовь", "прикол", "рецепт борща",
    "бесплатно скачать фильм", "игра престолов", "мемы", "кошки смешные"
]
TRAIN_DATA += [(text, "нерелевантный запрос") for text in irrelevant]

# Разделяем обучающую выборку на тексты (X) и метки классов (y)
X, y = zip(*TRAIN_DATA)

# Создаём pipeline из двух этапов:
# 1. TfidfVectorizer — преобразует текст в числовой вектор (учитываются униграммы и биграммы)
# 2. LogisticRegression — модель классификации
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("clf", LogisticRegression(max_iter=1000))
])

# Обучаем модель на собранных данных
pipeline.fit(X, y)

# Сохраняем обученную модель в файл для последующего использования
model_path = os.path.join("ai_assistant", "intent_model.joblib")
joblib.dump(pipeline, model_path)

print(f"Модель обучена и сохранена в {model_path}")
