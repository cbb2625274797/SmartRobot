import threading
import webbrowser
import pyautogui
import time


def open_UI(url):
    """
    打开url网站并全屏
    :param url:地址
    :return:0/1
    """
    webbrowser.open_new(url)
    time.sleep(2)
    pyautogui.press('F11')
    pyautogui.moveTo(400, 300)
    return 0


def mouse_location():
    """
    获取鼠标位置
    :return:location
    """
    location = pyautogui.position()
    return location