import os


class Path:

    __cwd = None
    __a = 5

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
    def test(cls):
        return id(cls.__a)

    @classmethod
    def geta(cls):
        return cls.__a
    
    @classmethod
    def seta(cls, a):
        cls.__a = a

