import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

from database import init_db, add_booking
from keyboards import main_kb, services_kb, dates_kb, times_kb

load_dotenv()
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

class Booking(StatesGroup):
    service = State()
    date = State()
    time = State()
    name = State()
    phone = State()

async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не найден")

    await init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    @dp.message(CommandStart())
    async def start(message: Message):
        await message.answer(
            "Привет! Я бот для записи.\nВыбери действие:",
            reply_markup=main_kb()
        )

    @dp.message(F.text == "📅 Записаться")
    async def start_booking(message: Message, state: FSMContext):
        await state.set_state(Booking.service)
        await message.answer("Выбери услугу:", reply_markup=services_kb())

    @dp.callback_query(F.data.startswith("service_"))
    async def choose_service(callback: CallbackQuery, state: FSMContext):
        service_map = {
            "service_haircut": "Стрижка",
            "service_manicure": "Маникюр",
            "service_consult": "Консультация"
        }
        service = service_map.get(callback.data, "Услуга")
        await state.update_data(service=service)
        await state.set_state(Booking.date)
        await callback.message.edit_text(f"Услуга: <b>{service}</b>\n\nВыбери дату:", reply_markup=dates_kb(), parse_mode="HTML")
        await callback.answer()

    @dp.callback_query(F.data.startswith("date_"))
    async def choose_date(callback: CallbackQuery, state: FSMContext):
        today = datetime.now().date()
        date_map = {
            "date_tomorrow": (today + timedelta(days=1)).strftime("%d.%m.%Y"),
            "date_day_after": (today + timedelta(days=2)).strftime("%d.%m.%Y"),
            "date_3days": (today + timedelta(days=3)).strftime("%d.%m.%Y"),
        }
        date = date_map.get(callback.data, "Дата")
        await state.update_data(date=date)
        await state.set_state(Booking.time)
        await callback.message.edit_text(f"Дата: <b>{date}</b>\n\nВыбери время:", reply_markup=times_kb(), parse_mode="HTML")
        await callback.answer()

    @dp.callback_query(F.data.startswith("time_"))
    async def choose_time(callback: CallbackQuery, state: FSMContext):
        time = callback.data.replace("time_", "")
        await state.update_data(time=time)
        await state.set_state(Booking.name)
        await callback.message.edit_text(f"Время: <b>{time}</b>\n\nКак вас зовут?", parse_mode="HTML")
        await callback.answer()

    @dp.message(Booking.name)
    async def get_name(message: Message, state: FSMContext):
        await state.update_data(name=message.text)
        await state.set_state(Booking.phone)
        await message.answer("Укажите номер телефона:")

    @dp.message(Booking.phone)
    async def get_phone(message: Message, state: FSMContext):
        data = await state.get_data()
        phone = message.text

        await add_booking(
            user_id=message.from_user.id,
            username=message.from_user.username or "",
            name=data["name"],
            phone=phone,
            date=data["date"],
            time=data["time"],
            service=data["service"]
        )

        # Уведомление админу
        if ADMIN_ID:
            try:
                await bot.send_message(
                    ADMIN_ID,
                    f"🆕 <b>Новая запись!</b>\n\n"
                    f"Услуга: {data['service']}\n"
                    f"Дата: {data['date']} {data['time']}\n"
                    f"Имя: {data['name']}\n"
                    f"Телефон: {phone}\n"
                    f"Username: @{message.from_user.username or 'нет'}",
                    parse_mode="HTML"
                )
            except Exception:
                pass

        await message.answer(
            f"✅ Запись успешно создана!\n\n"
            f"Услуга: <b>{data['service']}</b>\n"
            f"Дата: <b>{data['date']}</b>\n"
            f"Время: <b>{data['time']}</b>\n"
            f"Имя: {data['name']}\n\n"
            f"Мы свяжемся с вами для подтверждения.",
            parse_mode="HTML",
            reply_markup=main_kb()
        )
        await state.clear()

    @dp.message(F.text == "ℹ️ Услуги")
    async def services_info(message: Message):
        await message.answer(
            "<b>Наши услуги:</b>\n\n"
            "• Стрижка — от 1500 ₽\n"
            "• Маникюр — от 2000 ₽\n"
            "• Консультация — бесплатно\n\n"
            "Нажми «Записаться», чтобы выбрать.",
            parse_mode="HTML"
        )

    @dp.message(F.text == "📞 Контакты")
    async def contacts(message: Message):
        await message.answer("Телефон: +7 (999) 123-45-67\nАдрес: г. Москва, ул. Примерная, 1")

    @dp.callback_query(F.data == "cancel")
    async def cancel(callback: CallbackQuery, state: FSMContext):
        await state.clear()
        await callback.message.edit_text("Запись отменена.")
        await callback.answer()

    print("Бот записи запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
