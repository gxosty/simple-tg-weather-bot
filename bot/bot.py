import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.types import Message

from pyowm import OWM


owm = OWM(os.environ["OWM_TOKEN"])
logging.debug("OWM_TOKEN=%s", os.environ["OWM_TOKEN"])
city_registry = owm.city_id_registry()
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(
        "Hello, I am weather checker bot. Give me the city name, and I will get you the weather info."
    )


@dp.message()
async def check_weather_handler(message: Message) -> None:
    city = message.text.strip().capitalize()
    city_id = None

    for cid, cname, _, _, _, _ in city_registry.ids_for(city):
        if city == cname:
            city_id = cid

    if city_id is None:
        logging.warning(f"Couldn't find id of '{city}'")
        await message.answer("❌ Couldn't find the city. Please, try enter correct city name")
        return

    wmgr = owm.weather_manager()
    weather = wmgr.weather_at_id(city_id).weather

    temp = weather.temperature(unit="celsius")

    text = (
        f"🌍 <b>{city}</b>\n\n"
        f"📌 <i>{weather.detailed_status.capitalize()}</i>\n\n"
        f"🌡 <b>Current temperature:</b> {temp['temp']}°C\n"
        f"🔻 <b>Min temperature:</b> {temp['temp_min']}°C\n"
        f"🔺 <b>Max temperature:</b> {temp['temp_max']}°C\n"
        f"🤔 <b>Feels like:</b> {temp['feels_like']}°C\n\n"
        f"💧 <b>Humidity:</b> {weather.humidity}%\n"
        f"💨 <b>Wind speed:</b> {weather.wind().get('speed', 0)} m/s\n"
    )

    await message.answer(text, parse_mode="HTML")


async def bot_main():
    bot = Bot(
        token=os.environ["BOT_TOKEN"],
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await dp.start_polling(bot)
