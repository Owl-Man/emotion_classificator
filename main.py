from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
import io
import tensorflow as tf

app = FastAPI(title="Классификатор эмоций лица")

# === ЗАГРУЗКА МОДЕЛИ (TFLite) ===
interpreter = tf.lite.Interpreter(model_path="model_dynamic_quant.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Проверяем ожидаемую форму и тип
print("Вход:", input_details[0]['shape'], input_details[0]['dtype'])
print("Выход:", output_details[0]['shape'], output_details[0]['dtype'])

# === Классы эмоций ===
CLASS_NAMES = ["Angry", "Fear", "Happy", "Sad", "Surprise"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def preprocess_image(image: Image.Image):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image = image.resize((120, 120), Image.LANCZOS)
    img_array = np.array(image, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)   # (1, 120, 120, 3)
    return img_array

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        processed = preprocess_image(image)

        # Инференс через TFLite
        interpreter.set_tensor(input_details[0]['index'], processed)
        interpreter.invoke()
        predictions = interpreter.get_tensor(output_details[0]['index'])[0]

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