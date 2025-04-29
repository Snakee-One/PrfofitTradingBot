from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton, ContentType

how_button = KeyboardButton('/Как?🧐')
keyboard_start = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_start.add(how_button)

got_button = InlineKeyboardButton('Я все понял и готов!🔥', callback_data="ready")
more_button = InlineKeyboardButton('Подробнее о преимуществах🔍', callback_data="more")
watch = InlineKeyboardButton('Смотреть видео! ▶️', url="https://m.youtube.com/watch?v=ceFaOulSr7g")
markup2 = InlineKeyboardMarkup(row_width=1)
markup2.add(watch, more_button, got_button)

for_who = InlineKeyboardButton('Для кого подходит?🧐', callback_data="for_who")
markup3 = InlineKeyboardMarkup()
markup3.add(got_button, for_who)

reviews = InlineKeyboardButton('Посмотреть отзывы💬', callback_data="reviews")
markup4 = InlineKeyboardMarkup(row_width=2)
markup4.add(got_button, reviews)

calc = InlineKeyboardButton('Рассчитать заработок💰', callback_data="money")
markup5 = InlineKeyboardMarkup(resize_keyboard=True)
markup5.add(got_button, calc)

get = InlineKeyboardButton('ПОЛУЧИТЬ ПОДАРОК И СТАТИСТИКУ🎁', callback_data="get")
markup6 = InlineKeyboardMarkup()
markup6.add(get)

offer = InlineKeyboardButton('ПОЛУЧИТЬ СДЕЛКУ🔥', url="https://t.me/motiongun")
markup7 = InlineKeyboardMarkup()
markup7.add(offer)
