from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import schedule_data
import sevsu_info

sevsu_markup = InlineKeyboardMarkup(row_width=3)
lk = InlineKeyboardButton(text='👤 Личный кабинет', url=sevsu_info.urls.get('lk'))
mudl = InlineKeyboardButton(text='💻 Мудл', url=sevsu_info.urls.get('mudl'))
rocket = InlineKeyboardButton(text='📢 Рокет чат', url=sevsu_info.urls.get('rocket'))
electiv = InlineKeyboardButton(text='🏓 Элективы', url=sevsu_info.urls.get('electiv'))
sch = InlineKeyboardButton(text='📒 Расписания пар', url=sevsu_info.urls.get('sch'))
sevsu = InlineKeyboardButton(text='🌊 Сайт СевГУ', url=sevsu_info.urls.get('sevsu'))
sevsu_markup.add(sevsu, lk, sch).add(mudl, rocket, electiv)

groups_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4, one_time_keyboard=True)
is1 = KeyboardButton('📒 ИСб-21-1-о')
is2 = KeyboardButton('📒 ИСб-21-2-о')
is3 = KeyboardButton('📒 ИСб-21-3-о')
pi1 = KeyboardButton('📒 ПИб-21-1-о')
legacy_schedule = KeyboardButton('📓 ИИТ-21')
cancel_groups = KeyboardButton('🗑️ Отмена')
groups_markup.add(is1, is2, is3, pi1).add(legacy_schedule, cancel_groups)

days_week_markup = InlineKeyboardMarkup(row_width=3)
monday = InlineKeyboardButton('🤯 Пн', callback_data='days_week_d1')
tuesday = InlineKeyboardButton('🫠 Вт', callback_data='days_week_d2')
wednesday = InlineKeyboardButton('🫥 Ср', callback_data='days_week_d3')
thursday = InlineKeyboardButton('🥴 Чт', callback_data='days_week_d4')
friday = InlineKeyboardButton('😵‍💫 Пт', callback_data='days_week_d5')
saturday = InlineKeyboardButton('😶‍🌫️ Сб', callback_data='days_week_d6')
days_week_markup.add(monday, tuesday, wednesday, thursday, friday, saturday)

week_inline_keyboard = InlineKeyboardMarkup(row_width=4)
week_text = InlineKeyboardButton(text='🗒 Текстовая версия', callback_data='week_options_text')


def get_sevsu_ik() -> InlineKeyboardMarkup:
    return sevsu_markup


def get_group_rk() -> ReplyKeyboardMarkup:
    return groups_markup


def define_weeks_ik():
    for week_num in schedule_data.available_weeks:
        new_week_button = InlineKeyboardButton(text=f'{week_num} Нед',
                                               callback_data=f'week_options_num{week_num}')
        week_inline_keyboard.insert(new_week_button)
    week_inline_keyboard.add(week_text)


def get_weeks_ik() -> InlineKeyboardMarkup:
    return week_inline_keyboard


def get_days_week_ik() -> InlineKeyboardMarkup:
    return days_week_markup
