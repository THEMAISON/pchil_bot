import asyncio
from webdav3.client import Client
from config import WEBDAV_DATA
from schedule_data import get_legacy_schedule_path

client = Client(WEBDAV_DATA)

schedule_legacy_folder = 'PchilBotData/Schedules/Legacy'
schedules_improved_folder = 'PchilBotData/Schedules/Improved'

legacy_kwargs = {
    'remote_path': 'PchilBotData/Schedules/Legacy',
    'local_path': 'D://PyCharm Projects//pchil_bot//schedule_data//ИИТ-21.xlsx',
    'callback': 'legacy'
}

# Load resource
kwargsL = {
    'remote_path': "dir1/file1",
    'local_path': "~/Downloads/file1",
    'callback': 'callback'
}
# client.download_async(**kwargs)

# Unload resource
kwargsU = {
    'remote_path': "dir1/file1",
    'local_path': "~/Downloads/file1",
    'callback': 'legacy'
}


# client.upload_async(**kwargs)

# NOT WORKING
async def upload_legacy_schedule():
    client.upload_async(**legacy_kwargs)
