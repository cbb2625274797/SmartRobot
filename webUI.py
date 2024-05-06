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


if __name__ == '__main__':

    running = 99


    def run(running):
        while running:
            running -= 1
            time.sleep(0.1)
            print(running)


    def thread_function_1():
        run(running)


    def thread_function_2():
        while 1:
            time.sleep(1)
            print(mouse_location())


    thread1 = threading.Thread(target=thread_function_1)
    thread2 = threading.Thread(target=thread_function_2)

    thread1.start()
    thread2.start()
    thread1.join()
    thread1 = threading.Thread(target=thread_function_1)
    thread1.start()
