# FoodGPT Bot

Telegram-бот для распознавания продуктов по фото или тексту и генерации пошаговых рецептов с помощью GPT.

---

## 📦 Описание

Бот позволяет:
- Отправить список продуктов текстом или прислать фотографию ингредиентов
- Получить пошаговый рецепт с помощью GPT (g4f)

---

## ⚡ Быстрый старт (локально)

1. **Склонируй репозиторий**
   ```bash
   git clone https://github.com/Kxqusos/ProjectDP.git
   cd ProjectDP
2. **Создай .env файл в корне проекта:
   ```env
   TELEGRAM_TOKEN=your_telegram_bot_token
   WEBHOOK_URL=your_webhook
3. **Установи requirements.txt**
   ```bash
   pip install -r requirements.txt
4. **Собери образ Docker**
   ```bash
   docker build -t CONTAINER_NAME .
5. **Запусти контейнер**
   ```bash
   docker run --env-file .env -p 8000:8000 CONTAINER_NAME
  
