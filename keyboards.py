from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def main_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Записаться")],
            [KeyboardButton(text="ℹ️ Услуги"), KeyboardButton(text="📞 Контакты")]
        ],
        resize_keyboard=True
    )

def services_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Стрижка", callback_data="service_haircut")],
        [InlineKeyboardButton(text="Маникюр", callback_data="service_manicure")],
        [InlineKeyboardButton(text="Консультация", callback_data="service_consult")],
        [InlineKeyboardButton(text="« Отмена", callback_data="cancel")]
    ])

def dates_kb() -> InlineKeyboardMarkup:
    # Простые даты для демо
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Завтра", callback_data="date_tomorrow")],
        [InlineKeyboardButton(text="Послезавтра", callback_data="date_day_after")],
        [InlineKeyboardButton(text="Через 3 дня", callback_data="date_3days")],
        [InlineKeyboardButton(text="« Назад", callback_data="back_services")]
    ])

def times_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="10:00", callback_data="time_10:00"),
            InlineKeyboardButton(text="12:00", callback_data="time_12:00"),
        ],
        [
            InlineKeyboardButton(text="14:00", callback_data="time_14:00"),
            InlineKeyboardButton(text="16:00", callback_data="time_16:00"),
        ],
        [
            InlineKeyboardButton(text="18:00", callback_data="time_18:00"),
            InlineKeyboardButton(text="20:00", callback_data="time_20:00"),
        ],
        [InlineKeyboardButton(text="« Назад", callback_data="back_dates")]
    ])
