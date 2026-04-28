# app.py
import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="Классификатор эмоций", layout="centered", page_icon="🎭")

st.markdown("""
    <h1 style='text-align: center; color: #FF4B4B;'>
        🎭 Классификатор эмоций лица
    </h1>
""", unsafe_allow_html=True)

# ←←← ИЗМЕНИ НА СВОЙ URL ПОСЛЕ ДЕПЛОЯ НА RENDER ←←←
API_URL = "https://твой-проект.onrender.com/predict"

EMOJI = {
    "Angry": "😠",
    "Fear": "😨",
    "Happy": "😊",
    "Sad": "😢",
    "Surprise": "😲"
}

uploaded_file = st.file_uploader("Загрузите фотографию лица", 
                                 type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Показываем загруженное изображение
    st.image(image, caption="Загруженное изображение", use_container_width=True)
    
    if st.button("🔍 Определить эмоцию", type="primary", use_container_width=True):
        with st.spinner("Модель анализирует эмоцию..."):
            try:
                # Подготавливаем файл для отправки
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                files = {"file": ("face.png", buf.getvalue(), "image/png")}
                
                response = requests.post(API_URL, files=files, timeout=20)
                
                if response.status_code == 200:
                    result = response.json()
                    emotion = result["predicted_class"]
                    
                    st.success(f"**Предсказанная эмоция:** {EMOJI.get(emotion, '')} **{emotion}**")
                    
                    st.subheader("Вероятности по эмоциям:")
                    probs = result["probabilities"]
                    
                    for emo, prob in sorted(probs.items(), key=lambda x: x[1], reverse=True):
                        st.progress(prob, text=f"{EMOJI.get(emo, '')} {emo}: {prob*100:.1f}%")
                else:
                    st.error(f"Ошибка API: {response.status_code} — {response.text}")
                    
            except Exception as e:
                st.error(f"Ошибка соединения: {e}")

st.caption("Размер входного изображения модели: 120×120")