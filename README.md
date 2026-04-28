# 😊 Классификатор эмоций на лице

Полнофункциональное приложение для классификации эмоций на основе изображений лиц с использованием глубокого обучения, REST API и веб-интерфейса.

## 📋 Описание проекта

Этот проект демонстрирует полный жизненный цикл разработки и развёртывания модели машинного обучения:

- **Архитектура:** Frontend (Streamlit) + Backend (FastAPI) + ML Model (TensorFlow)
- **Датасет:** [Human Face Emotions](https://www.kaggle.com/datasets/samithsachidanandan/human-face-emotions)
- **Классы:** 7 эмоций (Злость, Отвращение, Страх, Радость, Нейтральный, Грусть, Удивление)
- **Размер входа:** 48×48 пиксели, оттенки серого

## 🎯 Возможности

### Frontend (Streamlit)
- ✅ Загрузка изображений лиц (JPG, PNG)
- ✅ Рисование прямо в приложении
- ✅ Вещественное время предпросмотра
- ✅ Визуализация вероятностей эмоций
- ✅ Информативный интерфейс

### Backend (FastAPI)
- ✅ REST API для предсказания
- ✅ Автоматическая документация (Swagger UI)
- ✅ Обработка изображений
- ✅ CORS поддержка
- ✅ Здоровье сервера и статус

### ML Model
- ✅ Классификация эмоций
- ✅ Вероятности для всех классов
- ✅ Оптимизированная предварительная обработка

## 📁 Структура проекта

```
emotion_classificator/
├── main.py                          # FastAPI Backend
├── app.py                           # Streamlit Frontend
├── requirements.txt                 # Зависимости
├── best_classification_model.h5     # Обученная модель (добавить позже)
├── README.md                        # Этот файл
├── .gitignore                       # Git ignore
├── Procfile                         # Для деплоя на Render
└── render.yaml                      # Конфигурация Render
```

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.8 или выше
- pip (Python Package Manager)

### Локальный запуск

#### 1. Клонируйте или скачайте проект

```bash
cd emotion_classificator
```

#### 2. Создайте виртуальное окружение (опционально)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

#### 4. Добавьте модель

Поместите файл `best_classification_model.h5` в корневую папку проекта.

#### 5. Запустите BackEnd (FastAPI)

**Терминал 1:**
```bash
uvicorn main:app --reload
```

Сервер будет доступен по адресу:
- API: http://localhost:8000
- Документация: http://localhost:8000/docs

#### 6. Запустите FrontEnd (Streamlit)

**Терминал 2:**
```bash
streamlit run app.py
```

Приложение откроется в браузере на http://localhost:8501

## 📚 API Документация

### Главные endpoints

#### 1. GET `/` - Информация о API
```bash
curl http://localhost:8000/
```

#### 2. GET `/health` - Проверка статуса
```bash
curl http://localhost:8000/health
```

#### 3. GET `/emotions` - Получить список эмоций
```bash
curl http://localhost:8000/emotions
```

#### 4. POST `/predict/` - Предсказание из файла
```bash
curl -X POST "http://localhost:8000/predict/" \
  -H "accept: application/json" \
  -F "file=@image.jpg"
```

**Ответ:**
```json
{
  "predicted_class": 3,
  "emotion": "Happy (Радость)",
  "confidence": 0.9234,
  "probabilities": [0.001, 0.002, 0.003, 0.923, 0.045, 0.020, 0.006],
  "emotion_probabilities": {
    "Angry (Злость)": 0.0010,
    "Disgust (Отвращение)": 0.0020,
    "Fear (Страх)": 0.0030,
    "Happy (Радость)": 0.9230,
    "Neutral (Нейтральный)": 0.0450,
    "Sad (Грусть)": 0.0200,
    "Surprise (Удивление)": 0.0060
  }
}
```

#### 5. POST `/predict_from_array/` - Предсказание из массива
```bash
curl -X POST "http://localhost:8000/predict_from_array/" \
  -H "Content-Type: application/json" \
  -d '{"array": [0.5, 0.3, ..., 0.8]}'
```

## 🌐 Развёртывание на Render.com

### Шаг 1: Подготовка репозитория GitHub

Создайте репозиторий с файлами:
```
emotion_classificator/
├── main.py
├── app.py
├── requirements.txt
├── best_classification_model.h5
├── Procfile
├── render.yaml
└── README.md
```

### Шаг 2: Создание Procfile

Файл `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Шаг 3: Создание render.yaml

Файл `render.yaml`:
```yaml
services:
  - type: web
    name: emotion-classifier
    env: python
    plan: free
    pythonVersion: 3.12.1
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.12.1
```

### Шаг 4: Развёртывание на Render

1. Перейдите на [render.com](https://render.com)
2. Создайте новый Web Service
3. Подключите GitHub репозиторий
4. Установите параметры:
   - **Name:** emotion-classifier
   - **Environment:** Python 3.12.1
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Нажмите Deploy

### Использование развёрнутого API

После развёртывания на Render:

```bash
# API будет доступен по адресу:
curl https://your-service-name.onrender.com/predict/

# В Streamlit измените URL на:
# https://your-service-name.onrender.com
```

## 🔧 Настройка

### Конфигурация Frontend

В `app.py` можно изменить:
- URL сервера (по умолчанию: http://localhost:8000)
- Максимальный размер изображения для отображения
- Цвета и тему интерфейса

### Конфигурация Backend

В `main.py` можно изменить:
- Размер входного изображения (по умолчанию: 48×48)
- Список поддерживаемых классов эмоций
- Логирование и обработку ошибок

## 📊 Примеры использования

### Python

```python
import requests
from PIL import Image

# Открыть изображение
image = Image.open("face.jpg")

# Отправить на API
with open("face.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://localhost:8000/predict/",
        files=files
    )

# Получить результат
result = response.json()
print(f"Предсказанная эмоция: {result['emotion']}")
print(f"Уверенность: {result['confidence']:.2%}")
```

### JavaScript/Fetch

```javascript
const formData = new FormData();
formData.append('file', imageFile);

const response = await fetch('http://localhost:8000/predict/', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(`Эмоция: ${result.emotion}`);
console.log(`Уверенность: ${(result.confidence * 100).toFixed(2)}%`);
```

## 🤖 Обучение собственной модели

Если вы хотите обучить свою модель:

```python
import tensorflow as tf
from tensorflow import keras

# Создание и обучение модели
model = keras.Sequential([
    keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(7, activation='softmax')  # 7 классов эмоций
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Обучение на данных
# model.fit(train_images, train_labels, epochs=50, validation_data=(val_images, val_labels))

# Сохранение модели
model.save('best_classification_model.h5')
```

## 🐛 Решение проблем

### Проблема: "Модель не найдена"
**Решение:** Убедитесь, что файл `best_classification_model.h5` находится в той же папке что и `main.py`

### Проблема: "Не удалось подключиться к серверу"
**Решение:** 
1. Проверьте, что FastAPI сервер запущен: `uvicorn main:app --reload`
2. Убедитесь, что используете правильный URL (http://localhost:8000)
3. Проверьте, что порт 8000 не занят

### Проблема: "CORS ошибка"
**Решение:** Проверьте, что CORS middleware правильно настроен в `main.py`

### Проблема: "ImportError: cannot import name..."
**Решение:** Переустановите все зависимости:
```bash
pip install --upgrade -r requirements.txt
```

## 📚 Дополнительные ресурсы

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [TensorFlow Guides](https://www.tensorflow.org/guide)
- [Kaggle Dataset](https://www.kaggle.com/datasets/samithsachidanandan/human-face-emotions)
- [CNN для классификации изображений](https://www.tensorflow.org/tutorials/images/classification)

## 📝 Лицензия

Этот проект распространяется под MIT лицензией. Смотрите файл LICENSE для деталей.

## 👥 Автор

Создано как учебный проект для демонстрации полного цикла разработки ML-приложений.

---

**Версия:** 1.0.0  
**Последнее обновление:** 2024  
**Статус:** ✅ Готово к использованию
