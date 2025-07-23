#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reply клавиатуры для бота
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_contact_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для отправки контакта"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_remove_keyboard() -> ReplyKeyboardMarkup:
    """Удаление клавиатуры"""
    return ReplyKeyboardMarkup(
        keyboard=[],
        resize_keyboard=True
    )
