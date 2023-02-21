from bs4 import BeautifulSoup
import requests
import schedule_data


def download_schedule_file():
    # делаем запрос на файл
    schedule_file_request = requests.get(schedule_data.schedule_file_url)

    # сохраняем скаченный файл
    with open(schedule_data.get_legacy_schedule_path(), 'wb') as schedule_file:
        schedule_file.write(schedule_file_request.content)


def is_schedule_file_updated():
    # запрос на html страницу расписаний
    schedules_request = requests.get(schedule_data.schedules_url).content

    # получение нужных ссылок и имен файлов
    soup = BeautifulSoup(schedules_request, 'html.parser')
    soup_names = soup.find(class_='document-accordion document-accordion-2', id='bx_719294866_75167').find_all('div', class_='document-link__name')
    soup_urls = soup.find(class_='document-accordion document-accordion-2', id='bx_719294866_75167').find_all('a')

    schedules_names = [name.text.strip('\n').strip() for name in soup_names]
    schedules_urls = [url.get('href') for url in soup_urls]

    for n, u in zip(schedules_names, schedules_urls):
        schedule_data.schedule_files_data[n] = u

    # определение ссылки на нужный файл и проверка на изменение
    sch_url = schedule_data.schedules_url[:20] + schedule_data.schedule_files_data.get(schedule_data.legacy_file_name)

    if schedule_data.schedule_file_url != sch_url:
        schedule_data.schedule_file_url = sch_url
        return True
    return False
