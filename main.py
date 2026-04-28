# main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
import io
import tensorflow as tf

app = FastAPI(title="Классификатор эмоций лица")

# === ЗАГРУЗКА МОДЕЛИ ===
try:
    model = tf.keras.models.load_model("best_emotion_model.h5")   # или .h5
    print("✅ Модель успешно загружена!")
except Exception as e:
    print(f"❌ Ошибка загрузки модели: {e}")
    raise

# === Классы эмоций ===
CLASS_NAMES = ["Angry", "Fear", "Happy", "Sad", "Surprise"]

# === CORS для работы со Streamlit ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Предобработка изображения ===
def preprocess_image(image: Image.Image):
    # Приводим к RGB
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Изменяем размер под твою модель (120x120)
    image = image.resize((120, 120), Image.LANCZOS)
    
    # Преобразуем в numpy + нормализация
    img_array = np.array(image, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)   # (1, 120, 120, 3)
    return img_array


# === Основной эндпоинт ===
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        processed = preprocess_image(image)
        predictions = model.predict(processed, verbose=0)[0]
        
        predicted_idx = np.argmax(predictions)
        predicted_class = CLASS_NAMES[predicted_idx]
        
        probabilities = {
            CLASS_NAMES[i]: float(predictions[i]) 
            for i in range(len(CLASS_NAMES))
        }
        
        return {
            "predicted_class": predicted_class,
            "probabilities": probabilities
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки изображения: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Emotion Classifier API is running"}