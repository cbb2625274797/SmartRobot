import QF_ASK as QF
import MQTT
import audio_process as AU
import threading
import time
import os
import glob

filepath = "./audio/recorded_audio.wav"


def thread_function_1(mode: str):
    if mode == "sound":
        while True:
            init()
            time.sleep(1)
            input("按回车继续...")  # 这里程序会暂停，等待用户按下回车
            AU.record(5, 16000, filepath)
            question = AU.STT(filepath)[0]
            QF.chat("Yi-34B-Chat", question)
    else:
        while True:
            init()
            time.sleep(1)
            input("按回车继续...")  # 这里程序会暂停，等待用户按下回车
            question = input("请输入你的提问:\n")
            QF.chat("Yi-34B-Chat", question)


def thread_function_2():
    # MQTT.stop_server()
    time.sleep(1)
    # MQTT.start_server()
    # time.sleep(3)
    MQTT.client_init()


mode = "text"
thread1 = threading.Thread(target=thread_function_1, args=(mode,))
thread2 = threading.Thread(target=thread_function_2)


def init():
    directory = "./audio"
    # 遍历文件列表并删除每个文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查文件扩展名是否为.mp3
            if file.endswith(".mp3"):
                # 构建文件的完整路径
                file_path = os.path.join(root, file)
                try:
                    # 删除文件
                    os.remove(file_path)
                    print(f"{file_path} 已被删除")
                except OSError as e:
                    # 打印删除失败的原因
                    print(f"无法删除 {file_path}。原因: {e.strerror}")
        print("缓存路径清空")


if __name__ == '__main__':

    thread2.start()
    time.sleep(3)
    thread1.start()
