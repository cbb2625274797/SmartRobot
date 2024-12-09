import subprocess
import threading
import time

import paho.mqtt.client as mqtt

import webUI
try:
    from audio.GPT_SOVITS import set_character
except:
    pass


def start_server(cmd_file_path):
    arg1 = 'start'
    # 构建完整的命令字符串，包括参数
    command = f'{cmd_file_path} {arg1} '
    # 使用subprocess运行.cmd文件
    process = subprocess.Popen(command, shell=True)
    print("MQTT服务器开启:")
    print(process)
    return process


def stop_server(cmd_file_path):
    arg1 = 'stop'
    # 构建完整的命令字符串，包括参数
    command = f'{cmd_file_path} {arg1} '
    # 使用subprocess运行.cmd文件
    process = subprocess.Popen(command, shell=True)
    print("MQTT服务器关闭:")
    print(process)
    return process


class new_class:
    def __init__(self, host="192.168.31.3", port=1883):
        # 创建一个MQTT客户端实例
        self.drag = False
        self.client = mqtt.Client("local1")
        self.father_robot = None
        self.host = host
        self.port = port

    def run(self):
        # 绑定回调函数
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # 连接到MQTT服务器
        self.client.connect(self.host, self.port, 20)

        self.subscribe("sound/character", 2)
        self.subscribe("sound/temperature")
        self.subscribe("sound/top_k")
        self.subscribe("sound/speed")
        self.subscribe("chat/model", 2)
        self.subscribe("chat/temperature")
        self.subscribe("chat/top_p")
        self.subscribe("motion/larm")
        self.subscribe("motion/rarm")
        self.subscribe("motion/leg")
        self.subscribe("motion/foot")
        self.subscribe("motion/action_enable")
        self.subscribe("other/wake_time")
        self.subscribe("other/volume")
        self.subscribe("other/asr_offline")
        self.subscribe("other/chat_offline")
        self.subscribe("other/drag", 2)

        # 线程控制
        thread1 = threading.Thread(target=self.thread_function_1, args=())
        thread1.start()
        while True:
            while self.drag:
                thread2 = threading.Thread(target=self.thread_function_2, args=())
                thread2.start()
                thread2.join()
            time.sleep(0.02)

    def thread_function_1(self):
        # 开始循环，等待MQTT事件
        self.client.loop_forever()

    def thread_function_2(self):
        while self.drag:
            self.client.publish("other/x", webUI.mouse_location().x * 2, qos=0)
            self.client.publish("other/y", webUI.mouse_location().y * 2, qos=0)
            time.sleep(0.04)

    # 当连接到MQTT服务器时的回调函数
    def on_connect(self, client, userdata, flags, rc):
        # 订阅一个或多个主题
        print(f"Connected with result code {rc}")

    # 主题：
    # sound : character  temperature top_k speed
    # chat: model temperature top_p
    # other: wake_time volume
    # motion: larm rarm leg foot
    def on_message(self, client, userdata, msg):
        print(msg.topic + ":" + msg.payload.decode("utf-8"))
        if msg.topic == "sound/character":
            temp = int(msg.payload.decode("utf-8"))
            if self.father_robot.sound_character != temp:
                set_character(temp)
                self.father_robot.set_sound_model(temp)
        elif msg.topic == "sound/temperature":
            temp = float(msg.payload.decode("utf-8"))
            if self.father_robot.sound_temperature != temp:
                self.father_robot.sound_temperature = temp
        elif msg.topic == "sound/top_k":
            temp = float(msg.payload.decode("utf-8"))
            if self.father_robot.sound_top_k != temp:
                self.father_robot.sound_top_k = temp
        elif msg.topic == "sound/speed":
            temp = float(msg.payload.decode("utf-8"))
            if self.father_robot.sound_speed != temp:
                self.father_robot.sound_speed = temp
        elif msg.topic == "chat/model":
            temp = msg.payload.decode("utf-8")
            if self.father_robot.model != temp:
                self.father_robot.set_chat_model(temp)
        elif msg.topic == "chat/temperature":
            temp = float(msg.payload.decode("utf-8"))
            if self.father_robot.chat_temperature != temp:
                self.father_robot.chat_temperature = temp
        elif msg.topic == "chat/top_p":
            temp = float(msg.payload.decode("utf-8"))
            if self.father_robot.chat_top_p != temp:
                self.father_robot.chat_top_p = temp
        elif msg.topic == "other/chat_offline":
            if msg.payload.decode("utf-8") == "1":
                self.father_robot.chat_offline = True
            else:
                self.father_robot.chat_offline = False
        elif msg.topic == "motion/larm":
            temp = float(msg.payload.decode("utf-8"))
            if self.father_robot.larm != temp:
                self.father_robot.set_larm_rotation(temp, 2)
                time.sleep(0.2)
        elif msg.topic == "motion/rarm":
            temp = float(msg.payload.decode("utf-8"))
            if self.father_robot.rarm != temp:
                self.father_robot.set_rarm_rotation(temp, 2)
                time.sleep(0.2)
        elif msg.topic == "motion/leg":
            temp = float(msg.payload.decode("utf-8"))
            if self.father_robot.body != temp:
                self.father_robot.set_body_rotation(temp, 2)
                time.sleep(0.2)
        elif msg.topic == "motion/foot":
            temp = float(msg.payload.decode("utf-8"))
            if self.father_robot.foot != temp:
                self.father_robot.set_foot_rotation(temp, 2)
                time.sleep(0.2)
        elif msg.topic == "motion/action_enable":
            temp = int(msg.payload.decode("utf-8"))
            if self.father_robot.action_enable != bool(temp):
                self.father_robot.action_enable = bool(temp)
        elif msg.topic == "other/wake_time":
            temp = float(msg.payload.decode("utf-8"))
            if self.father_robot.wake_time != temp:
                self.father_robot.wake_time = temp
        elif msg.topic == "other/volume":
            temp = float(msg.payload.decode("utf-8"))
            if self.father_robot.volume != temp:
                self.father_robot.volume = temp
        elif msg.topic == "other/drag":
            if msg.payload.decode("utf-8") == "1":
                self.drag = True
            else:
                self.drag = False
        elif msg.topic == "other/asr_offline":
            if msg.payload.decode("utf-8") == "1":
                self.father_robot.asr_offline = True
            else:
                self.father_robot.asr_offline = False

    def subscribe(self, topic_name, qos=0):
        self.client.subscribe(topic_name, qos=qos)
        print("subscribe:" + topic_name)

    def publish(self, topic, message, qos: int = 1):
        """
        :param topic:发布主题
        :param message:发布的消息
        :param qos:QOS
        :return:无返回
        """
        self.client.publish(topic, message, qos=qos)
        print('publish', topic, ":", message)
