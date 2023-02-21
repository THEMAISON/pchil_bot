class User:
    def __init__(self, user_id: int = None):
        self.__user_id = user_id
        self.__message_id = None
        self.__group = None
        self.__week = None
        self.__day = None

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id: int):
        self.__user_id = user_id

    @property
    def message_id(self):
        return self.__message_id

    @message_id.setter
    def message_id(self, message_id: int):
        self.__message_id = message_id

    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, group: int):
        self.__group = group

    @property
    def week(self):
        return self.__week

    @week.setter
    def week(self, week: int):
        self.__week = week

    @property
    def day(self):
        return self.__day

    @day.setter
    def day(self, day: int):
        self.__day = day
