import sys
from pathlib import Path

def get_repo_path(bundled=False):
    if bundled and getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)
        # запуск из PyInstaller bundle
        # создаётся в C:/Temp/_MEI... и туда закидываются все файлы, которые есть в режиме не onefile
    return Path.cwd()