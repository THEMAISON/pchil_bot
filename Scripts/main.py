import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text

import keyboards
from config import BOT_API_TOKEN
from keyboards import get_weeks_ik, get_group_rk, get_sevsu_ik, get_days_week_ik
from user import User
from schedule_parser import is_schedule_file_updated, download_schedule_file
import schedule_improver
import schedule_data
from datetime import datetime

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=BOT_API_TOKEN)
dp = Dispatcher(bot=bot, storage=storage)


class ScheduleStatesGroup(StatesGroup):
    group = State()


start_text = '''
👋 *пчил* приветствует тебя

Я в `бета` версии, но уже могу:
🦾 Кидать расписание на прогиб
🔗 Кидать ссылки в сибирь
🥱 Делать вид, что мне интересно с тобой общаться

/help - Узнать все возможности бота'''

help_text = '''
/sch - Расписание на текущую неделю
/sev - Сайты студента (личный кабинет, расписание, мудл и др.)'''

schedule_messages = {
    'check': '🔄 Проверяю расписание...',
    'update_pr': '⏏️ Обновляю расписание...',
    'download_pr': '📥 Скачиваю расписание...',
    'improve_pr': '🪄 Улучшаю расписание...',
    'load_pr': '📥 Загружаю...',
    'cancel': '⚠️ Процесс был отменен',
    'error': '⚠️ Расписание не доступно',
}

user = User()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=start_text, parse_mode='Markdown')


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=help_text, parse_mode='Markdown')
    await message.delete()


@dp.message_handler(commands=['sev'])
async def sev_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text='🔍 Доступные ссылки для уч. СевГУ',
                           reply_markup=get_sevsu_ik())


@dp.message_handler(commands=['sch'])
async def schedule_command(message: types.Message):
    await message.delete()
    # await upload_legacy_schedule()

    # проверяем файл расписания на сайте на обновление
    schedule_sent_message = await bot.send_message(chat_id=message.chat.id, text=schedule_messages.get('check'))
    is_updated = is_schedule_file_updated()
    await schedule_sent_message.delete()

    is_exist = schedule_data.is_legacy_file_exist()

    if is_updated or not is_exist:
        ssm_text = schedule_messages.get('download_pr') if not is_exist else schedule_messages.get('update_pr')
        schedule_sent_message = await bot.send_message(chat_id=message.chat.id, text=ssm_text)

        # удаление существующих файлов, скачивание нового
        schedule_data.remove_schedule_files()
        download_schedule_file()

        # сохраняем данные для парсинга
        schedule_data.save_parse_data()

        await schedule_sent_message.delete()

    # определяем доступные недели из расписания
    if is_updated or not len(schedule_data.available_weeks):
        schedule_improver.define_available_weeks()
        keyboards.define_weeks_ik()

    await bot.send_message(chat_id=message.chat.id, text='Выберите группу или институт', reply_markup=get_group_rk())
    await ScheduleStatesGroup.group.set()


@dp.message_handler(Text(equals='🗑️ Отмена'), state='*')
async def cancel_schedule_improve(message: types.Message, state: FSMContext):
    if state is None:
        return

    await message.delete()
    await bot.send_message(chat_id=message.chat.id, text=schedule_messages.get('cancel'), reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(Text(equals='📓 ИИТ-21'), state=ScheduleStatesGroup.group)
async def schedule_process(message: types.Message, state: FSMContext):
    loading_schedule_message = await bot.send_message(chat_id=message.chat.id, text=schedule_messages.get('load_pr'), reply_markup=ReplyKeyboardRemove())
    schedule_sent_message = await bot.send_document(chat_id=message.chat.id, document=open(
        schedule_data.get_legacy_schedule_path(), 'rb'))
    await loading_schedule_message.delete()

    await state.finish()


@dp.message_handler(Text(equals=['📒 ИСб-21-1-о', '📒 ИСб-21-2-о', '📒 ИСб-21-3-о', '📒 ПИб-21-1-о']), state=ScheduleStatesGroup.group)
async def schedule_improve_process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = int(message.text[-3]) if 'ИС' in message.text else 4

    print('name:', message.from_user.first_name, 'id:', message.from_user.id, 'time: ', datetime.now())

    # устанавливаем номер группы
    schedule_data.group = data['group']
    # user.group = schedule_data.group

    # устанавливаем текущую неделю
    schedule_data.set_current_week()
    # user.week = schedule_data.week

    # проверяем текущую неделю на актуальность
    if schedule_data.week not in schedule_data.available_weeks:
        await bot.send_message(chat_id=message.chat.id, text=schedule_messages.get('error'),
                               reply_markup=ReplyKeyboardRemove())
        return

    # улучшаем расписание, если его не существует
    if not schedule_data.is_improve_file_exist():
        message_schedule_improving = await bot.send_message(chat_id=message.chat.id, text=schedule_messages.get('improve_pr'), reply_markup=ReplyKeyboardRemove())
        schedule_improver.improve_schedule_week()
        await message_schedule_improving.delete()

    loading_schedule_message = await bot.send_message(chat_id=message.chat.id, text=schedule_messages.get('load_pr'), reply_markup=ReplyKeyboardRemove())
    schedule_sent_message = await bot.send_document(chat_id=message.chat.id, document=open(
        schedule_data.get_improve_schedule_path(), 'rb'), reply_markup=get_weeks_ik())
    await loading_schedule_message.delete()

    await state.finish()


@dp.callback_query_handler(lambda cb: 'week_options' in cb.data)
async def callback_schedule_option(callback: types.CallbackQuery):
    # выбрано текстовое расписание
    if 'text' in callback.data:
        await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup())

        # определяем текстовое расписание для текущего расписания
        schedule_improver.define_days_week_messages()

        # устанавливаем понедельник как первое расписание
        schedule_data.day = 1
        day_week_message = schedule_data.days_week_messages.get(schedule_data.day)

        if day_week_message:
            day_week_sent_message = await bot.send_message(chat_id=callback.message.chat.id, text=day_week_message, parse_mode='Markdown', reply_markup=get_days_week_ik())

        await callback.answer()
    # выбрана другая неделя
    else:
        # schedule_data.update_week(callback.data)
        week_num = int(callback.data[callback.data.find('num')+3:])

        if week_num != schedule_data.week:
            await callback.message.delete()

            schedule_data.define_week(week_num)

            if not schedule_data.is_improve_file_exist():
                schedule_sent_message = await bot.send_message(chat_id=callback.message.chat.id, text=schedule_messages.get('improve_pr'))
                schedule_improver.improve_schedule_week()
                await schedule_sent_message.delete()

            loading_schedule_message = await bot.send_message(chat_id=callback.message.chat.id, text=schedule_messages.get('load_pr'), reply_markup=ReplyKeyboardRemove())
            schedule_sent_message = await bot.send_document(chat_id=callback.message.chat.id, document=open(
                schedule_data.get_improve_schedule_path(), 'rb'), reply_markup=get_weeks_ik())
            await loading_schedule_message.delete()
            await callback.answer()
        else:
            await callback.answer('Расписание на эту неделю уже отправлено')


@dp.callback_query_handler(lambda cb: 'days_week' in cb.data)
async def callback_text_schedule_days_week(callback: types.CallbackQuery):
    # await callback.message.delete()

    # определяем текст для сообщения относительно дня недели
    schedule_data.day = int(callback.data[-1])
    day_week_message = schedule_data.days_week_messages.get(schedule_data.day)
    await callback.message.edit_text(day_week_message, parse_mode='Markdown', reply_markup=get_days_week_ik())

    await callback.answer()


if __name__ == '__main__':
    if schedule_data.is_parse_data_exist():
        schedule_data.import_parse_data()

    executor.start_polling(dp, skip_updates=True)
