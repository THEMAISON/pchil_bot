from os import path, remove, listdir
from datetime import datetime

data_path = 'D:/PyCharm Projects/pchil_bot/Schedules/Data/'
legacy_path = 'D:/PyCharm Projects/pchil_bot/Schedules/Legacy/'
improved_path = 'D:/PyCharm Projects/pchil_bot/Schedules/Improved/'

parse_data_file_name = 'parse_data.txt'
legacy_file_name = 'ИИТ-21-о'

schedules_url = 'https://www.sevsu.ru/univers/shedule/'
schedule_file_url = 'https://www.sevsu.ru/univers/shedule/download.php?file=AJ9DbHFYwaf5SMoJygDJTw%3D%3D'

group_names = {
    1: 'ИСб-21-1-о',
    2: 'ИСб-21-2-о',
    3: 'ИСб-21-3-о',
    4: 'ПИб-21-1-о',
}

days_week_names = {
    1: 'Понедельник',
    2: 'Вторник',
    3: 'Среда',
    4: 'Четверг',
    5: 'Пятница',
    6: 'Суббота',
}

days_week_messages = {
    1: '',
    2: '',
    3: '',
    4: '',
    5: '',
    6: ''
}

available_weeks = []
group = 2
week = 6
day = 1

schedule_files_data = {}
schedule_message_id = 0
schedule_chat_id = 0


# parse
def save_parse_data():
    with open(data_path + parse_data_file_name, 'w') as file:
        file.write(schedules_url + '\n')
        file.write(schedule_file_url + '\n')


def import_parse_data():
    global schedules_url, schedule_file_url, legacy_file_name

    with open(data_path + parse_data_file_name, 'r') as file:
        data = file.readlines()

    schedules_url = data[0].strip('\n')
    schedule_file_url = data[1].strip('\n')


def is_parse_data_exist():
    return path.isfile(data_path + parse_data_file_name)


# remove files
def remove_schedule_files():
    # удаление улучшенных расписаний
    for file in listdir(improved_path):
        remove(path.join(improved_path, file))

    # удаление общего расписаня
    for file in listdir(legacy_path):
        remove(path.join(legacy_path, file))


def get_legacy_schedule_path():
    return legacy_path + legacy_file_name + '.xlsx'


def get_improve_schedule_path():
    return improved_path + group_names[group] + f' ({week} Неделя).xlsx'


def is_legacy_file_exist():
    return path.isfile(get_legacy_schedule_path())


def is_improve_file_exist():
    return path.isfile(get_improve_schedule_path())


def set_current_week():
    global week
    week = datetime.today().isocalendar().week


def define_week(week_num: int) -> None:
    global week
    week = week_num


def update_week(data_text):
    global week
    if week < available_weeks[0]:
        week = available_weeks[0]
    elif 'prev' in data_text:
        if week > available_weeks[0]:
            week -= 1
    elif 'next' in data_text:
        if week > available_weeks[-1]:
            week = available_weeks[-1]
        elif week < available_weeks[-1]:
            week += 1


def align_week_type():
    if len(available_weeks) > 1:
        # номер недели в начале списка
        if available_weeks.index(week) == 0:
            return 0
        # номер недели в конце списка
        elif available_weeks.index(week) == len(available_weeks) - 1:
            return 2
        # номер недели в середине списка
        return 1
    return -1
