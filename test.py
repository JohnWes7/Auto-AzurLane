import os
from src.adb import Adb
from src.path import Path
from src.config import Config
from src.auto_azurlane import AutoAzurLane
import cv2
import time

def test():
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
    minvalue,maxvalue,minpos,maxpos = cv2.minMaxLoc(out)
    print(minvalue,maxvalue,minpos,maxpos)
    #最符合的位置maxpos 是左上角
    #中心位置为
    print(tryagain.shape)
    x = maxpos[0] + int(tryagain.shape[1] / 2)
    y = maxpos[1] + int(tryagain.shape[0] / 2)
    pos = (x,y)
    print(pos)

    #cv2.circle(screens,pos,3,(0,0,255),5)
    cv2.rectangle(screens, maxpos, (maxpos[0] + tryagain.shape[1],maxpos[1] + tryagain.shape[0]), (0,0,255), 1)
    cv2.imshow('', screens)
    cv2.waitKey()

    # pyplot.subplot(2,1,1)
    # pyplot.imshow(cv2.cvtColor(screens, cv2.COLOR_BGR2RGB))
    # pyplot.title('pic 1')
    # pyplot.xticks([])
    # pyplot.yticks([])

    # pyplot.subplot(2,1,2)
    # pyplot.imshow(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
    # pyplot.title('pic 2')
    # pyplot.xticks([])
    # pyplot.yticks([])

    # pyplot.savefig('plt.png')
    # pyplot.show()

def test2():
    a = Adb(Path.get_adb_path(),Path.get_screenshots_dir(),Config.get_hostport())
    pos = a.macth(Path.get_ui_tap_to_continue_path())
    if pos:
        print(pos.__dict__)
        ss = cv2.imread(a.get_screenshots_path())
        y,x,_ = cv2.imread(pos.name).shape
        cv2.rectangle(ss,(pos.x+int(x/2),pos.y+int(y/2)),(pos.x-int(x/2),pos.y-int(y/2)),(0,0,200),2)
        cv2.imshow('',ss)
        cv2.waitKey()
        a.tap(pos)
        time.sleep(1)

        pos = a.macth(Path.get_ui_confirm_path())
        if pos:
            print(pos.__dict__)
            ss = cv2.imread(a.get_screenshots_path())
            y,x,_ = cv2.imread(pos.name).shape
            cv2.rectangle(ss,(pos.x+int(x/2),pos.y+int(y/2)),(pos.x-int(x/2),pos.y-int(y/2)),(0,0,200),2)
            cv2.imshow('',ss)
            cv2.waitKey()
            a.tap(pos)

            pos = a.macth(Path.get_ui_confirm_path())
            if pos:
                print(pos.__dict__)
                ss = cv2.imread(a.get_screenshots_path())
                y,x,_ = cv2.imread(pos.name).shape
                cv2.rectangle(ss,(pos.x+int(x/2),pos.y+int(y/2)),(pos.x-int(x/2),pos.y-int(y/2)),(0,0,200),2)
                cv2.imshow('',ss)
                cv2.waitKey()
                a.tap(pos)
            
    else:
        print(pos)

def test3():
    a = Adb(Path.get_adb_path(),Path.get_screenshots_dir(),Config.get_hostport())
    #a.check()
    pos = a.macth(Path.get_ui_delegate_done_path())
    if pos:
        print(pos.__dict__)
        ss = cv2.imread(a.get_screenshots_path())
        y,x,_ = cv2.imread(pos.name).shape
        cv2.rectangle(ss,(pos.x+int(x/2),pos.y+int(y/2)),(pos.x-int(x/2),pos.y-int(y/2)),(0,0,200),2)
        cv2.imshow('',ss)
        cv2.waitKey()
        a.tap(pos)

def test4():
    a = Adb(Path.get_adb_path(),Path.get_screenshots_dir(),Config.get_hostport())
    #a.swipe(640,360,640,150)
    a.swipe(640,150,640,360)

def test5():
    a = Adb(Path.get_adb_path(),Path.get_screenshots_dir(),Config.get_hostport())
    a.check()
    azurlane = AutoAzurLane(a)
    print(azurlane.get_page())
    azurlane.check_delegation()

if __name__ == '__main__':
   test5()