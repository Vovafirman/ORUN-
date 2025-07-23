import os
import logging

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "8076821995:AAGUehKkk_EagiZWJgPd3MQs7iT5LzR-wFU")
DATABASE_URL = "cinema_merch.db"
GAME_URL = "https://center-kino.github.io/game_kinoshlep/"
SUPPORT_USERNAME = "@PRdemon"

# Admin user IDs (add your admin user IDs here)
ADMIN_IDS = [123456789]  # Replace with actual admin user IDs

# Product categories
CATEGORIES = {
    "center_kino": "Футболки \"Центр Кино\"",
    "kinomechanika": "Футболки \"Киномеханки\"",
    "board_games": "Настольные игры"
}

# Product data
PRODUCTS = {
    # Центр Кино футболки
    "original": {
        "name": "Оригинал",
        "category": "center_kino",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "images/Фото 1.png",
        "description": "**Фирменная футболка Центр Кино.** 💥"
    },
    "director": {
        "name": "Режиссер",
        "category": "center_kino",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "images/Фото 2.png",
        "description": "**Лаконичный дизайн для ценителей кино.** 🎬"
    },
    "scenario": {
        "name": "Сценарий",
        "category": "center_kino",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "images/Фото 3.jpg",
        "description": "**Сценарий на груди – выбор истинного киномана.** 📝"
    },
    "watch_till_end": {
        "name": "Смотри до конца",
        "category": "center_kino",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "images/Фото 4.jpg",
        "description": "**Не отвлекайся – смотри до конца!** 🍿"
    },
    "episode_meaning": {
        "name": "Даже в эпизоде есть смысл",
        "category": "center_kino",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "images/Фото 5.jpg",
        "description": "**Каждый эпизод важен.** 🎞️"
    },
    "after_credits": {
        "name": "После титров",
        "category": "center_kino",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "images/Фото 6.png",
        "description": "**Главное случается после титров.** 🎥"
    },
    "film_theory": {
        "name": "Теория кино",
        "category": "center_kino",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "images/Фото 7.jpg",
        "description": "**Теория кино на практике.** 📚"
    },

    # Киномеханки футболки
    "movie_poster": {
        "name": "Кинопостер",
        "category": "kinomechanika",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "images/Фото 8.jpg",
        "description": "**Стильный кинопостер на груди.** 🖼️"
    },
    "frame_24": {
        "name": "24 кадра",
        "category": "kinomechanika",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "images/Фото 9.jpg",
        "description": "**24 кадра – магия кино.** 🎞️"
    },
    "stop_frame": {
        "name": "Стоп кадр",
        "category": "kinomechanika",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "images/Фото 10.jpg",
        "description": "**Замри на стоп‑кадре.** ⏸️"
    },
    "close_up": {
        "name": "Крупный план",
        "category": "kinomechanika",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "images/Фото 11.jpg",
        "description": "**Крупный план – только хиты.** 🔍"
    },
    "general_plan": {
        "name": "Общий план",
        "category": "kinomechanika",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "images/Фото 12.jpg",
        "description": "**Весь кадр целиком – общий план.** 🌆"
    },
    "movie_style": {
        "name": "Стиль кино",
        "category": "kinomechanika",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "images/Фото 13.jpg",
        "description": "**Настоящий стиль кино.** ⭐"
    },

    # Настольные игры
    "kinoshlyop": {
        "name": "Киношлёп",
        "category": "board_games",
        "price": 2099,
        "colors": ["ОРИГИНАЛЬНЫЙ"],
        "image": "images/Фото 14.png",
        "description": "**Настольная игра \"Киношлёп\" – веселье гарантировано.** 🎲"
    },
    "kinofix": {
        "name": "КиноФикс",
        "category": "board_games",
        "price": 1999,
        "description": "Настольная игра для киноманов",
        "colors": ["ОРИГИНАЛЬНЫЙ"],
        "image": "images/Фото 15.png",
        "description": "**КиноФикс – проверь свои знания фильмов.** 🎲"
    }
}

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
