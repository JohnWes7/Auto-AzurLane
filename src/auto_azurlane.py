import os
from src.adb import Adb
from src.path import Path
from src.position import Position
from src.timer import Timer
import time


class AutoAzurLane:

    pages = {
        'home': Path.get_ui_weigh_anchor_path(),
        'weigh_anchor': Path.get_ui_delegate_path(),
        'delegation': Path.get_ui_delegate_page_path()
    }

    def __init__(self, adb: Adb) -> None:
        self.adb = adb
        self.current_page = None

    def get_page(self):
        '''检查当前的页面'''
        self.adb.screenshots()
        for key in AutoAzurLane.pages:
            if self.adb.macth(AutoAzurLane.pages.get(key), shots=False):
                return key
        return 'unknow'

    def tap_until_search(self, path, nextpage, threshold=Adb.threshold, uiname=None, sleepsec=0.25, timeout=300):
        '''一直搜寻直到找到path的图片 并点击 本意用于跳转页面'''
        if uiname == None:
            temp = os.path.split(path)
            uiname = temp[len(temp) - 1]
        pos = self.adb.search(path, threshold=threshold,
                              sleepsec=sleepsec, timeout=timeout)
        if pos:
            print(f'点击 {uiname}')
            self.adb.tap(pos, sleepsec=sleepsec)
            self.current_page = nextpage
        else:
            raise Exception(f'未能找到 {uiname}')

    def __swipe_callback(*arg):
        if arg[0] % 2 == 0:
            arg[2].swipe(640,150,640,360)
            time.sleep(1)
        else:
            arg[2].swipe(640,360,640,150)
            time.sleep(1)
        pass

    def collect_start_delegation(self):
        # 页面检查确保页面正确
        if not self.get_page() == 'delegation':
            raise('委托收取失败：不在委托界面')
        self.current_page = 'delegation'

        # 开始收委托
        timer = Timer()
        count = 0
        print(f'进行一个委托的收取\t{timer.get_duration()}')
        while True:
            print(f'\r检索收取委托中\t{timer.get_duration()}', end='')
            pos = self.adb.search(Path.get_ui_done_path(),searchtime=3,searchfall_callback=AutoAzurLane.__swipe_callback)
            if pos:
                self.adb.tap(pos)
                self.adb.tap(Position(640, 500, 1, ''))
                self.adb.tap(Position(640, 500, 1, ''))
                self.adb.tap(Position(640, 500, 1, ''), sleepsec=1)
                count += 1
            else:
                print(f'\r没有委托可被收取\t{timer.get_duration()}s\t已收集:{count}\tdone')
                break

        # 开始挂委托
        timer = Timer()
        count = 0
        print('进行一个委托的挂')
        while True:
            print(f'\r检索挂委托中\t{timer.get_duration()}', end='')
            # 检查可派遣队伍
            pos = self.adb.macth(Path.get_ui_delegate_0_path())
            if pos:
                print(f'\r可派遣队伍为零\t{timer.get_duration()}s\t已承接:{count}\tdone')
                break

            pos = pos = self.adb.search(Path.get_ui_delegate_free_path(),searchtime=3,searchfall_callback=AutoAzurLane.__swipe_callback)
            if pos:
                self.adb.tap(pos)
                self.tap_until_search(
                    Path.get_ui_delegate_advice_path(), 'delegation')
                self.tap_until_search(
                    Path.get_ui_delegate_start_path(), 'delegation', sleepsec=1)
                self.adb.tap(Position(640, 550, 1, ''), sleepsec=1)
                count += 1

    def check_delegation(self):
        '''进行一次委托检查  有能收的就收了重新挂'''
        print('开始检查委托')

        # 检查页面
        self.current_page = self.get_page()

        # 页面跳转
        if self.current_page == 'home':
            self.tap_until_search(
                Path.get_ui_weigh_anchor_path(), 'weigh_anchor', uiname='出击按钮')
        if self.current_page == 'weigh_anchor':
            self.tap_until_search(
                Path.get_ui_delegate_path(), 'delegation', uiname='委托任务')

        self.collect_start_delegation()
