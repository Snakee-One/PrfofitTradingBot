import asyncio
import logging

from aiogram import types, Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, \
    InlineKeyboardButton, ContentType, CallbackQuery, InputMedia
from aiogram.utils.callback_data import CallbackData

import keyboards as kb

TOKEN = "7745940346:AAE4pP2nkvJ0SVsdv-kaTOb14beJAN3GgQo"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot=bot, storage=MemoryStorage())

MSG = "Это текст рассылки!"


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    #await bot.send_video_note(message.chat.id, video_note=open('circle.mp4', 'rb'))
    await bot.send_message(user_id,
                           "<strong>Я подготовил для тебя подарок и статистику моих сделок,</strong>\n"
                           "<strong>дойди до конца и забирай</strong>🎁\n\n"
                           "✔️<strong>Смотри видео и ознакамливайся</strong>✔️")

    # time.sleep(3)
    await message.answer('Видео: <a href="https://www.youtube.com/watch?v=ceFaOulSr7g">⠀</a>',
                         reply_markup=kb.markup2)


fruits = [
    {
        "slug": "apples",
        "display_name": "Отзыв 1",
        "image_url": "https://disk.yandex.ru/i/p9fp3WnEJyVYkg"
    },
    {
        "slug": "oranges",
        "display_name": "Отзыв 2",
        "image_url": "https://disk.yandex.ru/i/R-ejsVddP3sIlA"
    },
    {
        "slug": "bananas",
        "display_name": "Отзыв 3",
        "image_url": "https://disk.yandex.ru/i/RyohwxdXKwxN_A"
    },
    {
        "slug": "lemons",
        "display_name": "Отзыв 4",
        "image_url": "https://disk.yandex.ru/i/Pa651XfIwEXCPA"
    },
    {
        "slug": "lemons",
        "display_name": "Отзыв 5",
        "image_url": "https://disk.yandex.ru/i/iPXCXJeH_nbh8A"
    },
]

fruits_callback = CallbackData("Fruits", "page")


def get_fruits_keyboard(page: int = 0) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=3)
    has_next_page = len(fruits) > page + 1
    if page != 0:
        keyboard.add(
            InlineKeyboardButton(
                text="Назад◀️",
                callback_data=fruits_callback.new(page=page - 1)
            )
        )
    if has_next_page:
        keyboard.add(
            InlineKeyboardButton(
                text="Вперед▶️",
                callback_data=fruits_callback.new(page=page + 1)
            )
        )
    return keyboard


@dp.callback_query_handler(lambda c: c.data == "reviews")
async def fruits_index(callback: types.CallbackQuery):
    fruit_data = fruits[0]
    caption = f"<b>{fruit_data.get('display_name')}</b>"
    keyboard = get_fruits_keyboard()  # Page: 0

    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=fruit_data.get("image_url"),
        caption=caption,
        parse_mode="HTML",
        reply_markup=keyboard
    )
    await bot.send_message(callback.from_user.id, 'Обязательно посмотри отзывы по ссылке:\n'
                                                  'и наверху⤴️', reply_markup=kb.markup5)


@dp.callback_query_handler(fruits_callback.filter())
async def fruit_page_handler(query: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))

    fruit_data = fruits[page]
    caption = f"<b>{fruit_data.get('display_name')}</b>"
    keyboard = get_fruits_keyboard(page)

    photo = InputMedia(type="photo", media=fruit_data.get("image_url"), caption=caption)

    await query.message.edit_media(photo, keyboard)


@dp.callback_query_handler(lambda c: c.data == 'money')
async def money(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, '<strong>С какого капитала ты готов начать в USDT?\n'
                                                  '(напиши просто цифру, например 1000 или 500)\n\n'
                                                  'Если ты новичок, напиши комфортную для тебя сумму, чтобы\n'
                                                  'удостовериться в моих сделках</strong>')
    state = dp.current_state(user=callback.from_user.id)
    await state.set_state("enter_money")


@dp.message_handler(state='enter_money', content_types=ContentType.TEXT)
async def calc(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state(True)
    cash = int(message.text)
    if cash < 10000:
        price = cash * 2.3
        vol = cash * 4.2
    else:
        price = cash * 1.5
        vol = cash * 2.7
    await bot.send_message(message.chat.id,
                           f'По моей статистике, ты заработаешь чистыми минимум - <strong>{price} USDT</strong>\n\n'
                           f'Так как сейчас рынок волатильный и предсказуемый, твой\n'
                           f'заработок может составить - <strong>{vol} USDT</strong>\n\n'
                           f'<strong>Да, это плюс к твоему депозиту! Но это при условии, что ты\n'
                           f'будешь строго и оперативно выполнять мои инструкции, и\n'
                           f'соблюдать торговую стратегию.📈\n\n'
                           f'Ты дошел до цели! Я приготовил для тебя подарок и\n'
                           f'статистику сделок</strong>⬇️', reply_markup=kb.markup6)


@dp.callback_query_handler(lambda c: c.data == "how")
async def how_(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    # await bot.send_message(callback_query.from_user.id, '<a href="https://m.youtube.com/watch?v=ceFaOulSr7g">⠀</a>', reply_markup=kb.markup2)
    # await bot.send_message(callback_query.from_user.id, 'BlaBlaBla <a href="https://m.youtube.com/watch?v=ceFaOulSr7g">⠀</a>')
    # await bot.send_video(callback_query.from_user.id, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', reply_markup=kb.markup2)


@dp.callback_query_handler(lambda c: c.data == "more")
async def how_(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_photo(callback_query.from_user.id, 'https://disk.yandex.ru/i/0xhZPUBM2n9TSQ',
                         caption='✔️<strong> ЛЕГКО ЗАРАБОТАТЬ</strong>\n'
                                 'Нет необходимости изучать рынок, проведу по всем шагам в течении сделки\n\n'
                                 '✔️ <strong>МГНОВЕННЫЙ СИГНАЛ</strong>\n'
                                 'Ты получаешь информацию о сделке моментально, следовательно максимизируешь свой профит\n\n'
                                 '✔️ <strong>БЕЗ ПОТЕРИ ДЕПОЗИТА</strong> \n'
                                 '<strong>Минимальные риски</strong>, ты полагаешься на четкую торговую стратегию от лучшей команды аналитиков\n\n'
                                 '✔️ <strong>ПОСТОЯННЫЙ ДОХОД</strong>\n'
                                 'Адаптация к меняющимся условиям рынка позволяет нам успешно торговать уже более 10 лет',
                         reply_markup=kb.markup3)


@dp.callback_query_handler(lambda c: c.data == "for_who")
async def how_(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_photo(callback_query.from_user.id, 'https://disk.yandex.ru/i/jDRD5eYXsrMxIQ',
                         caption=
                                 '🙋‍♂️ <strong>НОВИЧОК</strong>\n'
                                 'Тебе будет доступна вся пошаговая инструкция, как это делать,\n'
                                 'лично я буду отвечать на все вопросы и контролировать твои шаги\n'
                                 'Ты получаешь ценные знания от меня - опытного трейдера и я всегда на связи!😉\n\n'
                                 '😎 <strong>ДЕЙСТВУЮЩИЙ ТРЕЙДЕР</strong>\n'
                                 'Вы уже понимаете как работает рынок, знаете, что такое\n'
                                 'фундаментальный, технический и компьютерный анализ.', reply_markup=kb.markup4)


@dp.callback_query_handler(lambda c: c.data == "get")
async def how_(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "<strong>Подожди немного, пока загрузится видео!</strong>")
    await bot.send_video(callback_query.from_user.id, video=open('last.mp4', 'rb'))
    await bot.send_message(callback_query.from_user.id,
                           '<strong>Поздравляю тебя! Ты дошел до конца и получаешь вип\n'
                           'сделку лично от меня</strong>🎁\n\n'
                           'Кстате, я уже тебе написал или напишу чуть позже. Если не\n'
                           'терпиться начать со мной работу - нажимай на кнопку\n'
                           '<strong>"ПОЛУЧИТЬ СДЕЛКУ"</strong> и будем общаться!😉\n'
                           , reply_markup=kb.markup7)


@dp.callback_query_handler(lambda c: c.data == "ready")
async def how_(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_video(callback_query.from_user.id, video=open('last.mp4', 'rb'))
    await bot.send_message(callback_query.from_user.id,
                           '<strong>Поздравляю тебя! Ты дошел до конца и получаешь вип\n'
                           'сделку лично от меня</strong>🎁\n\n'
                           'Кстате, я уже тебе написал или напишу чуть позже. Если не\n'
                           'терпиться начать со мной работу - нажимай на кнопку\n'
                           '<strong>"ПОЛУЧИТЬ СДЕЛКУ"</strong> и будем общаться!😉\n\n'
                           '<srtong>Подожди немного, пока загрузится видео!</strong>', reply_markup=kb.markup7)
    for i in range(10):
        await asyncio.sleep(60 * 60 * 24)
        await bot.send_message(callback_query.from_user.id, MSG)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
