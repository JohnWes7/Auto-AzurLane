import os
import cv2
from src.position import Position
import time

class Adb:

    threshold = 0.8

    def __init__(self, adbpath: str, screenshots_dir: str, hostport: str) -> None:
        '''new'''
        self.__adbpath = adbpath
        self.__screenshots_path = screenshots_dir + \
            '/' + hostport.replace(':', '-') + '.png'
        self.__hostport = hostport

    def get_screenshots_path(self):
        return self.__screenshots_path

    # 给这一台设备实例下命令
    def hostport_command(self, command: str):
        '''adb -s 设备端口 command'''
        result = os.popen(f'{self.__adbpath} -s {self.__hostport} {command}')
        result.reconfigure(encoding='utf-8')
        return result.read().strip()

    # adb命令
    def adb_command(self, command: str):
        '''adb command'''
        result = os.popen(f'{self.__adbpath} {command}')
        result.reconfigure(encoding='utf-8')
        return result.read().strip()

    def check(self):
        '''检查'''
        print('==== check ====')

        # adb位置检查
        self.check_adb()
        # 设备连接检查
        self.check_connect()
        # 杂项检查
        self.check_miscellaneous()

        print('==== check done ====')

    def check_connect(self):
        '''检查设备连接'''
        print('检查连接:\t', end='')

        # 尝试连接
        out = self.adb_command(f'connect {self.__hostport}')
        print(out)
        devices = self.adb_command(f'devices')
        devices = devices.splitlines()

        # 检测是否在设备列表中
        temp = None
        for line in devices:
            print(line, end='')
            if self.__hostport in line:
                temp = line
            print()

        # 没有连接
        if not temp:
            print('adb没有连接上,请重试')
            print('或者尝试cmd手动连接')
            print(f'cmd输入 "{self.__adbpath} connect {self.__hostport}"')
            input('exit')
            exit(1)

        # 设备离线
        if 'offline' in temp:
            print('检测到设备离线！！！')
            print('由于不同模拟器ADB实现细节不同，请尝试以下办法（没有先后顺序）：')
            print('· 重启模拟器')
            print('· 如果模拟器已经自带了ADB，则可以尝试将脚本中adb文件夹的文件拷贝至模拟器自带ADB目录。注意备份原文件')
            print(
                '· 在adb目录下打开cmd，执行 adb kill-server 后再执行 adb start-server，然后执行 adb devices 查看是否解决')
            print('· 重启电脑')
            print('· 换个模拟器')
            input('exit')
            exit(1)

    def check_adb(self):
        '''检查adb位置'''
        print('检查adb路径:\t', self.__adbpath, end='\t')
        if os.path.exists(self.__adbpath):
            print('success')
        else:
            input(f'adb路径出错 当前路径设置为: {self.__adbpath}')
            exit(1)

    def check_miscellaneous(self):
        '''检查杂项'''
        print('检查杂项: ')

        # 检查屏幕分辨率
        out = self.hostport_command('shell wm size')
        print('分辨率:\t', out)
        if not '1280x720' in out:
            print('请将分辨率设置为 1280x720')
            exit(1)
        # 像素密度
        out = self.hostport_command('shell wm density')
        print('像素密度:\t'+out)
        # 系统类型
        out = self.hostport_command('shell getprop ro.product.device')
        print('系统类型:\t'+out)
        # 系统版本
        out = self.hostport_command('shell getprop ro.build.version.release')
        print('系统版本:\t'+out)

    def screenshots(self):
        '''设备屏幕截图'''
        command = f'exec-out screencap -p > {self.__screenshots_path}'
        self.hostport_command(command)

    def macth(self, img_path: str, threshold=threshold, shots=True):
        '''和传入图片进行对比'''
        if shots:
            self.screenshots()
        screenshot = cv2.imread(self.__screenshots_path)
        template = cv2.imread(img_path)
        # 进行比较
        out = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        # 获得比较结果矩阵最小值，最大值，最小值索引，最大值索引 也就是真正的结果
        minvalue, maxvalue, minpos, maxpos = cv2.minMaxLoc(out)

        # 如果maxvalue超过阈值 返回找到的position结果
        if maxvalue > threshold:
            posx = maxpos[0] + int(template.shape[1]/2)
            posy = maxpos[1] + int(template.shape[0]/2)
            return Position(posx, posy, maxvalue, img_path)
    
    def macths(self, *img_path:str, threshold=threshold, shots=True):
        pass

    def tap(self, pos: Position, sleepsec=0.25):
        '''点击postion的位置'''
        x, y = pos.get_pos()
        cm = f'shell input tap {x} {y}'
        self.hostport_command(cm)
        time.sleep(sleepsec)

    def swipe(self, start_x, start_y, end_x, end_y, duration=1500):
        '''滑动'''
        self.hostport_command('shell input swipe %d %d %d %d %d' % (start_x, start_y, end_x, end_y, duration))