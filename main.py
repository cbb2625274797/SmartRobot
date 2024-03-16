import QF_ASK as QF
import MQTT
import audio_process as AU
import threading
import time
import os
import glob

filepath = "./audio/recorded_audio.wav"


def thread_function_1():
    while True:
        init()
        time.sleep(1)
        input("按回车继续...")  # 这里程序会暂停，等待用户按下回车
        AU.record(5, 16000, filepath)
        question = AU.STT(filepath)[0]
        # question = input("请输入你的提问:\n")
        QF.chat("Yi-34B-Chat", question)


def thread_function_2():
    # MQTT.stop_server()
    time.sleep(1)
    # MQTT.start_server()
    # time.sleep(3)
    MQTT.client_init()


thread2 = threading.Thread(target=thread_function_2)
thread1 = threading.Thread(target=thread_function_1)


def init():
    # 使用glob模块匹配路径下的所有文件
    files = glob.glob("./audio")
    # 遍历文件列表并删除每个文件
    for file in files:
        if os.path.isfile(file):  # 确保只删除文件，不删除目录
            os.remove(file)
            print("move")


if __name__ == '__main__':
    thread2.start()
    time.sleep(3)
    thread1.start()
