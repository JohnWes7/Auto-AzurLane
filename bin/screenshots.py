import os
if __name__ == '__main__':
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.adb import Adb
from src.path import Path
from src.config import Config

def run():
    a = Adb(adbpath=Path.get_adb_path(),screenshots_dir=Path.get_screenshots_dir(),hostport=Config.get_hostport())
    a.screenshots()
    print(f'截图已保存 {a.get_screenshots_path()}')

if __name__ == '__main__':
    run()
