import joblib
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ai_assistant/intent_model.joblib")

# Загружаем модель один раз при инициализации
model = joblib.load(MODEL_PATH)

def classify_intent(text: str) -> str:
    return model.predict([text])[0]
