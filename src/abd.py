import os

class Abd:

    def __init__(self, adbpath:str, screenshots_dir:str, hostport: str) -> None:
        '''new'''
        self.__adbpath = adbpath
        temp = hostport.replace(':','-')
        self.__screenshots_path = screenshots_dir+temp
        self.__hostport = hostport

    #给这一台设备实例下命令
    def command(self, command:str):
        '''向设备下命令'''
        result = os.popen(f'{self.__adbpath} -s {self.__hostport} {command}')
        return result

    def check(self):
        
        pass
    
    def screenshots(self):
        '''设备屏幕截图'''
        command = f'exec-out screencap -p > {self.__screenshots_path}'
        self.command(command)