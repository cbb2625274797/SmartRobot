import os
import platform
import threading
import time

import pypinyin

import webUI as UI
from audio import audio_process as AU
from body import PWM

import audio.audio_recognition as ASR


def cleanup():
    """
    删除缓存目录的文件
    :return:0/1
    """
    cnt = 0
    directory = "./audio"
    # 遍历文件列表并删除每个文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查文件扩展名是否为.mp3
            if file.endswith(".mp3"):
                file_path = os.path.join(root, file)
                try:
                    # 删除文件
                    os.remove(file_path)
                    cnt += 1
                except OSError as e:
                    # 打印删除失败的原因
                    print(f"无法删除 {file_path}。原因: {e.strerror}")
    print(f"缓存路径清空,删除了{cnt}个文件")
    return 0


def contains_sublist(lst, sub_list):
    # 使用join()方法将列表元素拼接成字符串
    result_string = ''.join([item for sublist in sub_list for item in sublist])
    target_string = ''.join([item for sublist in lst for item in sublist])
    return result_string in target_string


class ROBOT:
    def __init__(self,
                 model,
                 host,
                 name: str = "小斌",
                 mode: str = "text"):
        """
        进行初始化
        :param model:使用的模型
        :param name:机器人名称/唤醒词
        :param mode:text/sound，控制是否语音
        :param host:主机地址
        """
        from bigmodel import large_language_model_interface as LLM_interface
        self.MQTT_instance = None
        self.LLM_interface = LLM_interface
        self.host = host
        # 总体参数
        self.asr_offline = True
        self.asr_model = self.ASR_init()
        self.mode = mode
        self.name = name
        self.wake_time = 3
        self.continue_talk = True
        self.volume = 1
        # 文字大模型API参数
        self.chat_offline = True
        self.model = model
        self.chat_temperature = 0.95
        self.chat_top_p = 0.75
        # 声音大模型参数
        self.sound_character = "paimon"
        self.sound_speed = 1
        self.sound_temperature = 1
        self.sound_top_k = 0.9
        # 姿态参数
        self.action_enable = True
        self.larm = 90
        self.rarm = 90
        self.body = 90
        self.foot = 90
        self.PWM_instance1 = PWM.PWM()
        self.thread_openweb = threading.Thread(target=self.web_open_thread, args=())
        self.thread_chat = threading.Thread(target=self.chat_thread, args=())

    def ASR_init(self):
        print("ASR模型组件初始化...需要较长时间...")
        asr_model = ASR.load_model()
        wav_path = './audio/wakeup.wav'
        result = ASR.inference(wav_path, asr_model)
        print("ASR模型组件初始化完成！")
        return asr_model

    def run(self):
        self.thread_openweb.start()
        while self.PWM_instance1.Mqtt_ins is None:
            time.sleep(0.1)
            self.PWM_instance1.Mqtt_ins = self.MQTT_instance
        print("机器人已运行")
        self.thread_chat.start()

    def set_body_rotation(self, target_angle: float, speed: float = 1):
        """
        进行身体旋转
        :param speed: 速度
        :param target_angle: 旋转角度
        :return:
        """
        print("身体旋转到", target_angle, "度")
        self.PWM_instance1.angle_switch(4, self.foot, target_angle, speed)
        self.foot = target_angle
        return True

    def set_foot_rotation(self, target_angle: float, speed: float = 1):
        """
        进行足部旋转
        """
        print("足部旋转到", target_angle, "度")
        self.PWM_instance1.angle_switch(0, self.body, target_angle, speed)
        self.body = target_angle
        return True

    def set_larm_rotation(self, target_angle: float, speed: float = 1):
        """
        进行左臂旋转
        """
        print("左臂旋转到", target_angle, "度")
        self.PWM_instance1.angle_switch(8, self.larm, target_angle, speed)
        self.larm = target_angle
        return True

    def set_rarm_rotation(self, target_angle: float, speed: float = 1):
        """
        进行右臂旋转
        """
        print("右臂旋转到", target_angle, "度")
        self.PWM_instance1.angle_switch(12, self.rarm, target_angle, speed)
        self.rarm = target_angle
        return True

    def set_chat_model(self, model: str):
        """
        设置大模型
        :param model:大模型种类。参考：https://cloud.baidu.com/doc/WENXINWORKSHOP/s/xlmokikxe
        :return:
        """
        print("切换大模型：", model)
        self.model = model
        try:
            AU.SOVITS_TTS(self.sound_character, "开心", "切换大模型成功,可以继续对话了", "./audio/switch.mp3")
            AU.play("./audio/switch.mp3", self.volume)
        except Exception as e:
            print(e)
        return 0

    def set_sound_model(self, character_code: int):
        """
        设置声音模型
        :param character_code:角色:0-paimon 1-funingna 2-hutao 3-shenli 4-wanye
        :return:
        """
        if character_code == 0:
            self.sound_character = "paimon"
        elif character_code == 1:
            self.sound_character = "funingna"
        elif character_code == 2:
            self.sound_character = "hutao"
        elif character_code == 3:
            self.sound_character = "shenli"
        elif character_code == 4:
            self.sound_character = "wanye"

        try:
            AU.SOVITS_TTS(self.sound_character, "开心", "切换语音模型成功,可以继续对话了", "./audio/switch.mp3")
            AU.play("./audio/switch.mp3", self.volume)
        except Exception as e:
            print(e)
        return 0

    def chat_thread(self):
        """
        进行大模型对话的操作
        :return:
        """
        filepath = "./audio/recorded_audio.wav"
        sleep = True
        if self.mode == "audio":
            while True:
                if sleep:
                    AU.record(self.wake_time, 16000, filepath)
                    # threshold = 1 / self.wake_time
                    # if not AU.is_audio_silent("./audio/recorded_audio.wav", threshold):
                    if AU.audio_is_silent(filepath):
                        print("音频为空")
                    else:
                        if not self.asr_offline:
                            # 旧版在线语音识别
                            pinyin = pypinyin.pinyin(AU.STT(filepath)[0], style=pypinyin.NORMAL)
                        else:
                            # 新版离线语音识别
                            question = ASR.inference(filepath, self.asr_model)[0]['preds'][0]
                            print(question)
                            pinyin = pypinyin.pinyin(question, style=pypinyin.NORMAL)
                        # 判断是否包含唤醒词
                        if contains_sublist(pinyin, pypinyin.pinyin(self.name, style=pypinyin.NORMAL)):
                            sleep = False
                elif not sleep:
                    cleanup()
                    AU.play("./audio/wakeup.wav", self.volume)  # 播放提示音
                    self.MQTT_instance.publish("other/status", "聆听")
                    AU.record(5, 16000, filepath)
                    # 静音判断
                    if AU.audio_is_silent(filepath):
                        print("音频为空")
                    else:
                        if not self.asr_offline:
                            question = AU.STT(filepath)[0]
                        else:
                            question = ASR.inference(filepath, self.asr_model)[0]['preds'][0]
                        if question == "":
                            print("音频为空")
                            pass
                        elif "请你退下" in question:
                            self.MQTT_instance.publish("other/status", "休眠")
                            sleep = True
                        else:
                            if not self.chat_offline:
                                self.LLM_interface.chat(self.model, question, self)
                            else:
                                self.LLM_interface.chat(self.model, question, self)
                            if not self.continue_talk:  # 如果不是连续对话，睡眠
                                sleep = True
                                self.MQTT_instance.publish("other/status", "休眠")
        else:
            while True:
                input("按回车继续...")  # 这里程序会暂停，等待用户按下回车
                cleanup()
                AU.play("./audio/wakeup.wav", self.volume)  # 播放提示音
                question = input("请输入你的提问:\n")
                if not self.chat_offline:
                    self.LLM_interface.chat(self.model, question, self)
                else:
                    self.LLM_interface.chat(self.model, question, self)

    def web_open_thread(self):
        """
        进行web的操作（打开WebRTC图形化界面）
        :host:主机地址
        :return:0/1
        """
        web_site = "http://" + self.host
        system_name = platform.system().lower()
        if system_name == "windows":
            print("当前系统：", system_name, "，不需要开启webUI")
        else:
            UI.open_UI(web_site)
        return 0
