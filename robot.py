import audio_process as AU
import threading
import webUI as UI
import pypinyin
from body import PWM


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
        import QF_ASK as QF
        self.MQTT_instance = None
        self.QF = QF
        self.host = host
        # 总体参数
        self.mode = mode
        self.name = name
        self.wake_time = 3
        self.continue_talk = True
        self.volume = 1
        # 文字大模型API参数
        self.model = model
        self.chat_temperature = 0.95
        self.chat_top_p = 0.75
        # 声音大模型参数
        self.sound_character = "paimon"
        self.sound_speed = 1
        self.sound_temperature = 1
        self.sound_top_k = 0.9
        # 姿态参数
        self.larm = 90
        self.rarm = 90
        self.body = 90
        self.foot = 90
        self.cooldowm = 0
        self.PWM_instance1 = PWM.PWM()

        self.thread1 = threading.Thread(target=self.thread_function_1, args=())
        self.thread3 = threading.Thread(target=self.thread_function_3, args=())

    def run(self):
        self.thread1.start()
        self.thread3.start()

    def set_foot_rotation(self, target_angle: float):
        """
        进行足部旋转
        :param target_angle: 旋转角度
        :return:
        """
        print("足部旋转到", target_angle, "度")
        self.PWM_instance1.angle_switch(0, self.foot, target_angle, 1)
        self.foot = target_angle
        return True

    def set_body_rotation(self, target_angle: float):
        """
        进行身体旋转
        """
        print("身体旋转到", target_angle, "度")
        self.PWM_instance1.angle_switch(1, self.body, target_angle, 1)
        self.body = target_angle
        return True

    def set_larm_rotation(self, target_angle: float):
        """
        进行左臂旋转
        """
        print("左臂旋转到", target_angle, "度")
        self.PWM_instance1.angle_switch(2, self.larm, target_angle, 1)
        self.larm = target_angle
        return True

    def set_rarm_rotation(self, target_angle: float):
        """
        进行右臂旋转
        """
        print("右臂旋转到", target_angle, "度")
        self.PWM_instance1.angle_switch(3, self.rarm, target_angle, 1)
        self.rarm = target_angle
        return True

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
                    AU.record(self.wake_time, 16000, filepath)
                    pinyin = pypinyin.pinyin(AU.STT(filepath)[0], style=pypinyin.NORMAL)
                    if contains_sublist(pinyin, pypinyin.pinyin(self.name, style=pypinyin.NORMAL)):
                        sleep = False
                elif not sleep:
                    AU.play("./audio/wakeup.wav", self.volume)  # 播放提示音
                    AU.record(5, 16000, filepath)
                    question = AU.STT(filepath)[0]
                    self.QF.chat(self.model, question, father_robot=self)
                    if not self.continue_talk:  # 如果不是连续对话，睡眠
                        sleep = True
        else:
            while True:
                input("按回车继续...")  # 这里程序会暂停，等待用户按下回车
                question = input("请输入你的提问:\n")
                self.QF.chat(self.model, question, father_robot=self)

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
    ROBOT_ins = ROBOT("ERNIE-Bot", host, mode="text")
    ROBOT_ins.run()
