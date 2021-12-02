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

    def tap_until_search(self, path, nextpage, threshold=Adb.threshold, uiname=None, sleepsec=0.25):
        '''一直搜寻直到找到path的图片'''
        timer = Timer()
        if uiname == None:
            temp = os.path.split(path)
            uiname = temp[len(temp) - 1]
        while True:
            print(f'\r正在寻找{uiname}\t{timer.get_duration()}s', end='')
            pos = self.adb.macth(path, threshold=threshold)
            if pos:
                self.adb.tap(pos, sleepsec)
                break
        print(f'\r正在寻找{uiname}\t{timer.get_duration()}\tsuccess')
        self.current_page = nextpage

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

        # 再次页面检查确保页面正确
        if not self.get_page() == 'delegation':
            raise('委托检查失败：无法到达委托界面')

        # 开始收委托
        self.current_page = 'delegation'
        print('start')
        timer = Timer()
        while True:
            print(f'\r检索收取委托中\t{timer.get_duration()}', end='')
            pos = self.adb.macth(Path.get_ui_done_path())
            if pos:
                self.adb.tap(pos)
                self.adb.tap(Position(640, 500, 1, ''))
                self.adb.tap(Position(640, 500, 1, ''))
                self.adb.tap(Position(640, 500, 1, ''))
            else:
                print(f'\r检索收取委托中\t{timer.get_duration()}s\tsuccess')
                break
        print('委托收取完毕')
