import motor.motor_asyncio
from user import User
from config import MONGODB_DATA

cluster = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_DATA.get('pchil_bot_cluster'))

users_collection = cluster.PchilBotDb.Users
schedules_files_collection = cluster.SchedulesFiles
schedules_parse_collection = cluster.SchedulesParse


async def add_user_message(user: User) -> None:
    users_collection.insert_one({
        '_id': str(user.user_id),
        'message': str(user.message_id),
        'group': str(user.group),
        'week': str(user.week),
        'day': str(user.day),
    })


async def update_user_message(old_message_id: int, new_message_id: int, new_group: int, new_week: int, new_day: int) -> None:
    users_collection.update_one({'message':  str(old_message_id)}, {'$set': {
        'message': str(new_message_id),
        'group': str(new_group),
        'week': str(new_week),
        'day': str(new_day)
    }})

