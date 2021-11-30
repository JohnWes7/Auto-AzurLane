import configparser
from src.path import Path

class Config:

    __ini = None
    
    @classmethod
    def __getconfig(cls):
        if cls.__ini:
            print('aaa')
            return cls.__ini
        
        cls.__ini = configparser.ConfigParser()
        cls.__ini.read(Path.get_configini_path(),encoding='utf-8')
        return cls.__ini
    
    @classmethod
    def get_hostport(cls):
        return cls.__getconfig().get('general','hostport')
    