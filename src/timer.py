import datetime

class Timer:
    def __init__(self) -> None:
        self.initime = datetime.datetime.now()

    def get_duration(self):
        '''获得从创建类到现在的时间'''
        return (datetime.datetime.now() - self.initime).seconds