import os


class Adb:

    def __init__(self, adbpath: str, screenshots_dir: str, hostport: str) -> None:
        '''new'''
        self.__adbpath = adbpath
        self.__screenshots_path = screenshots_dir + \
            '/' + hostport.replace(':', '-') + '.png'
        self.__hostport = hostport

    # 给这一台设备实例下命令
    def command(self, command: str):
        '''向设备下命令'''
        result = os.popen(f'{self.__adbpath} -s {self.__hostport} {command}')
        return result

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
        print('检查连接:\t', end=' ')

        # 尝试连接
        re = os.popen(f'{self.__adbpath} connect {self.__hostport}').read()
        print(re, end='')
        devices = os.popen(f'{self.__adbpath} devices').read()
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
        print('检查adb路径:\t', self.__adbpath, end=' ')
        if os.path.exists(self.__adbpath):
            print('success')
        else:
            input(f'adb路径出错 当前路径设置为: {self.__adbpath}')
            exit(1)

    def check_miscellaneous(self):
        '''检查杂项'''
        print('检查杂项: ')

        # 检查屏幕分辨率
        out = self.command('shell wm size').read()
        print('分辨率:\t', out[:-1], end='')
        if not '1280x720' in out:
            print('请将分辨率设置为 1280x720')
            exit(1)
        # 像素密度
        out = self.command('shell wm density').read()
        print('像素密度:\t'+out[:-1], end='')
        # 系统类型
        out = self.command('shell getprop ro.product.device').read()
        print('系统类型:\t'+out[:-1], end='')
        # 系统版本
        out = self.command('shell getprop ro.build.version.release').read()
        print('系统版本:\t'+out[:-1], end='')

    def screenshots(self):
        '''设备屏幕截图'''
        
        command = f'exec-out screencap -p > {self.__screenshots_path}'
        self.command(command)
