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
        "image": "attached_assets/Фото 1_1753272367389.png"
    },
    "director": {
        "name": "Режиссер",
        "category": "center_kino",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "attached_assets/Фото 2_1753272367389.png"
    },
    "scenario": {
        "name": "Сценарий",
        "category": "center_kino",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "attached_assets/Фото 3_1753272367389.jpg"
    },
    "watch_till_end": {
        "name": "Смотри до конца",
        "category": "center_kino",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "attached_assets/Фото 4_1753272367390.jpg"
    },
    "episode_meaning": {
        "name": "Даже в эпизоде есть смысл",
        "category": "center_kino",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "attached_assets/Фото 5_1753272367390.jpg"
    },
    "after_credits": {
        "name": "После титров",
        "category": "center_kino",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "attached_assets/Фото 6_1753272367390.png"
    },
    "film_theory": {
        "name": "Теория кино",
        "category": "center_kino",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "attached_assets/Фото 7_1753272367391.jpg"
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
        "image": "attached_assets/Фото 8_1753272367391.jpg"
    },
    "frame_24": {
        "name": "24 кадра",
        "category": "kinomechanika",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "attached_assets/Фото 9_1753272367391.jpg"
    },
    "stop_frame": {
        "name": "Стоп кадр",
        "category": "kinomechanika",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "attached_assets/Фото 10_1753272367391.jpg"
    },
    "close_up": {
        "name": "Крупный план",
        "category": "kinomechanika",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "attached_assets/Фото 11_1753272367392.jpg"
    },
    "general_plan": {
        "name": "Общий план",
        "category": "kinomechanika",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "attached_assets/Фото 12_1753272367392.jpg"
    },
    "movie_style": {
        "name": "Стиль кино",
        "category": "kinomechanika",
        "price": 2250,
        "size": "OVERSIZE",
        "density": "240 грамм",
        "material": "Хлопок",
        "colors": ["МОЛОЧНЫЙ", "ЧЕРНЫЙ"],
        "image": "attached_assets/Фото 13_1753272367392.jpg"
    },

    # Настольные игры
    "kinoshlyop": {
        "name": "Киношлёп",
        "category": "board_games",
        "price": 2099,
        "description": "Увлекательная настольная игра для любителей кино",
        "colors": ["ОРИГИНАЛЬНЫЙ"],
        "image": "attached_assets/Фото 14_1753272367393.png"
    },
    "kinofix": {
        "name": "КиноФикс",
        "category": "board_games",
        "price": 1999,
        "description": "Настольная игра для киноманов",
        "colors": ["ОРИГИНАЛЬНЫЙ"],
        "image": "attached_assets/Фото 15_1753272367393.png"
    }
}

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)