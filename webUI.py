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
    pyautogui.moveTo(200, 300)
    time.sleep(3)
    pyautogui.click()
    return 0
