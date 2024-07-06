import time
import subprocess

import pyautogui


def open_UI(url):
    """
    打开url网站并全屏
    :param url:地址
    :return:0/1
    """
    try:
        command = f"su - orangepi -c 'chromium-browser {url}'"
        subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    except Exception:
        pass
    pyautogui.moveTo(400, 200)
    time.sleep(5)
    pyautogui.click()
    pyautogui.hotkey('F11')
    return 0


def mouse_location():
    """
    获取鼠标位置
    :return:location
    """
    location = pyautogui.position()
    return location