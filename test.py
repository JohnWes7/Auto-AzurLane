import os
from src.adb import Adb
from src.path import Path
from src.config import Config


def screenshots():
    command = f'{Path.get_adb_path()} -s 127.0.0.1:7555 exec-out screencap -p > {Path.get_screenshots_dir()}'
    print(command)
    result = os.popen(command).read()
    print(result)


if __name__ == '__main__':
    # e:/MyScripts/Auto-AzurLane/adb/adb.exe
    #e:/MyScripts/Auto-AzurLane/src/image/screenshots
    print(Path.getcwd())
    print(Path.get_adb_path())
    print(Path.get_screenshots_dir())

    a = Adb(Path.get_adb_path(), Path.get_screenshots_dir(),Config.get_hostport())

    a.check()
    a.screenshots()
