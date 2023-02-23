from bs4 import BeautifulSoup
import requests
import schedule_data

schedule_files_data = {}


def download():
    r_file = requests.get(schedule_data.schedule_file_url)
    with open(schedule_data.get_legacy_schedule_path(), 'wb') as schedule_file:
        schedule_file.write(r_file.content)


def is_updated():
    r_page = requests.get(schedule_data.schedules_url).content
    iit_soup = BeautifulSoup(r_page, 'html.parser').find(class_='document-accordion document-accordion-2', id='bx_719294866_75167')
    soup_files_names = iit_soup.find_all('div',class_='document-link__name')
    soup_files_urls = iit_soup.find_all('a')

    files_names = [name.text.strip('\n').strip() for name in soup_files_names]
    files_urls = [url.get('href') for url in soup_files_urls]

    for n, u in zip(files_names, files_urls):
        schedule_files_data[n] = u

    # определение ссылки на файл
    parsed_url = schedule_data.schedules_url[:20] + schedule_files_data.get(schedule_data.legacy_file_name)

    if schedule_data.schedule_file_url != parsed_url:
        schedule_data.schedule_file_url = parsed_url
        return True
    return False
