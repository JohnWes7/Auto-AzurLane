import os
from src.adb import Adb
from src.path import Path
from src.config import Config
import cv2


def screenshots():
    command = f'{Path.get_adb_path()} -s 127.0.0.1:7555 exec-out screencap -p > {Path.get_screenshots_dir()}'
    print(command)
    result = os.popen(command).read()
    print(result)


if __name__ == '__main__':
    # e:/MyScripts/Auto-AzurLane/adb/adb.exe
    # e:/MyScripts/Auto-AzurLane/src/image/screenshots
    print(Path.getcwd())
    print(Path.get_adb_path())
    print(Path.get_screenshots_dir())
    Path.checkdir(Path.get_screenshots_dir())
    print(Path.get_ui_tryagain_path())

    a = Adb(Path.get_adb_path(), Path.get_screenshots_dir(),Config.get_hostport())
    #a.screenshots()
    #a.check()

    screens = cv2.imread(Path.get_screenshots_dir()+'/127.0.0.1-7555.png',cv2.IMREAD_COLOR)
    tryagain = cv2.imread(Path.get_ui_tryagain_path(),cv2.IMREAD_COLOR)
    print(type(screens))
    print(type(tryagain))
    out = cv2.matchTemplate(screens,tryagain,cv2.TM_CCOEFF_NORMED)
    # 获得矩阵最小值，最大值，最小值索引，最大值索引
    print(cv2.minMaxLoc(out))
    cv2.imshow('',out)
    cv2.waitKey()
    