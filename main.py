import QF_ASK as QF
import MQTT
import audio_process as AU
import threading
import time
import os
import webUI as UI
import pypinyin


def cleanup():
    """
    删除缓存目录的文件
    :return:0/1
    """
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
    return 0


def contains_sublist(lst, sublist):
    return any(lst[i:i + len(sublist)] == sublist for i in range(len(lst) - len(sublist) + 1))


class ROBOT:
    def __init__(self,
                 model,
                 host,
                 name: str = "小斌",
                 mode: str = "text"):
        """
        进行初始化
        :param model:使用的千帆模型
        :param name:机器人名称/唤醒词
        :param mode:text/sound，控制是否语音
        :param host:主机地址
        """
        # 总体参数
        self.mode = mode
        self.name = name
        self.wake_duration = 3
        self.continue_talk = True
        self.volume = 1
        # MQTT参数
        self.MQTT_instance = None
        self.MQTT_port = 1883
        self.host = host
        # 文字大模型API参数
        self.model = model
        self.chat_temperature = 0.95
        self.chat_top_p = 0.75
        # 声音大模型参数
        self.sound_character = "paimon"
        self.sound_speed = 1
        self.sound_temperature = 1
        self.sound_top_k = 0.9

        self.thread1 = threading.Thread(target=self.thread_function_1, args=())
        self.thread2 = threading.Thread(target=self.thread_function_2)
        self.thread3 = threading.Thread(target=self.thread_function_3, args=())
        # 清理临时文件
        cleanup()

    def run(self):
        self.thread3.start()
        self.thread2.start()
        time.sleep(3)
        self.thread1.start()

    def thread_function_1(self):
        """
        进行大模型对话的操作
        :return:
        """
        filepath = "./audio/recorded_audio.wav"
        sleep = True
        if self.mode == "sound":
            while True:
                if sleep:
                    AU.record(self.wake_duration, 16000, filepath)
                    pinyin = pypinyin.pinyin(AU.STT(filepath)[0], style=pypinyin.NORMAL)
                    if contains_sublist(pinyin, pypinyin.pinyin(self.name, style=pypinyin.NORMAL)):
                        sleep = False
                elif not sleep:
                    AU.play("./audio/wakeup.wav", self.volume)  # 播放提示音
                    AU.record(5, 16000, filepath)
                    question = AU.STT(filepath)[0]
                    QF.chat(self.model, question, father_robot=self)
                    if not self.continue_talk:  # 如果不是连续对话，睡眠
                        sleep = True
        else:
            while True:
                time.sleep(1)
                input("按回车继续...")  # 这里程序会暂停，等待用户按下回车
                question = input("请输入你的提问:\n")
                QF.chat(self.model, question, father_robot=self)

    def thread_function_2(self):
        """
        进行MQTT的操作
        :return:
        """
        self.MQTT_instance = MQTT.new_class(self)
        self.MQTT_instance.client_init(self.host, self.MQTT_port)

    def thread_function_3(self):
        """
        进行web的操作（打开WebRTC图形化界面）
        :host:主机地址
        :return:0/1
        """
        web_site = "http://" + self.host
        UI.open_UI(web_site)
        return 0


if __name__ == '__main__':
    host = "192.168.21.193"
    ROBOT_ins = ROBOT("ERNIE-Bot", host, "sound")
    ROBOT_ins.run()
