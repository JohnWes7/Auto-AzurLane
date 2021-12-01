import os

# 路径类 提供项目所需文件夹路径以及文件相关的方法 路径全为绝对路径
class Path:

    __cwd = None

    @classmethod
    def getcwd(cls):
        if cls.__cwd:
            return cls.__cwd
        srcdir = os.path.dirname(os.path.abspath(__file__))
        cls.__cwd = cwd = os.path.dirname(srcdir).replace('\\', '/')
        return cwd

    @classmethod
    def get_adb_path(cls):
        return cls.getcwd() + '/adb/adb.exe'

    @classmethod
    def get_screenshots_dir(cls):
        return cls.getcwd() + '/src/image/screenshots'
    
    @classmethod
    def get_configini_path(cls):
        return cls.getcwd() + '/config.ini'
    
    @classmethod
    def get_ui_dir(cls):
        return cls.getcwd() + '/src/image/ui'
    
    @classmethod
    def get_ui_tryagain_path(cls):
        return cls.get_ui_dir() + '/tryagain.png'
    
    @classmethod
    def get_ui_pause_path(cls):
        return cls.get_ui_dir() + '/pause.png'
    
    @classmethod
    def get_ui_fulldock_path(cls):
        return cls.get_ui_dir() + '/fulldock.png'

    @classmethod
    def get_ui_clean_up_path(cls):
        return cls.get_ui_dir() + '/clean_up.png'

    @classmethod
    def get_ui_retired_path(cls):
        return cls.get_ui_dir() + '/retired.png'
    
    @classmethod
    def get_ui_confirm_path(cls):
        return cls.get_ui_dir() + '/confirm.png'
        
    @classmethod
    def get_ui_tap_to_continue_path(cls):
        return cls.get_ui_dir() + '/tap_to_continue.png'
    
    @staticmethod
    def checkdir(dirpath):
        if os.path.exists(dirpath) and os.path.isdir(dirpath):
            return
        os.makedirs(dirpath)

