import subprocess
import threading
import time

import paho.mqtt.client as mqtt

import webUI

try:
    from audio.GPT_SOVITS import set_character
except:
    pass

import body.action as action


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
        self.client = mqtt.Client(
            client_id="local1",
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2  # 显式声明API版本
        )
        self.father_robot = None
        self.host = host
        self.port = int(port)

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
        self.subscribe("chat/deep_think")
        self.subscribe("motion/larm")
        self.subscribe("motion/rarm")
        self.subscribe("motion/body")
        self.subscribe("motion/foot")
        self.subscribe("motion/action_enable")
        self.subscribe("other/wake_time")
        self.subscribe("other/volume")
        self.subscribe("other/asr_offline")
        self.subscribe("other/chat_offline")
        self.subscribe("other/drag", 2)
        self.subscribe("dialog/act")

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
    # motion: larm rarm body foot
    def on_message(self, client, userdata, msg):
        print(msg.topic + ":" + msg.payload.decode("utf-8"))
        # 假设 msg 和 self.father_robot 是已定义的变量
        thread = threading.Thread(target=self.handle_message, args=(msg, self.father_robot))
        thread.start()

    def handle_message(self, msg, robot_ins):
        if msg.topic == "sound/character":
            temp = int(msg.payload.decode("utf-8"))
            if robot_ins.sound_character != temp:
                set_character(temp)
                robot_ins.set_sound_model(temp)
        elif msg.topic == "sound/temperature":
            temp = float(msg.payload.decode("utf-8"))
            if robot_ins.sound_temperature != temp:
                robot_ins.sound_temperature = temp
        elif msg.topic == "sound/top_k":
            temp = float(msg.payload.decode("utf-8"))
            if robot_ins.sound_top_k != temp:
                robot_ins.sound_top_k = temp
        elif msg.topic == "sound/speed":
            temp = float(msg.payload.decode("utf-8"))
            if robot_ins.sound_speed != temp:
                robot_ins.sound_speed = temp
        elif msg.topic == "chat/model":
            temp = msg.payload.decode("utf-8")
            if robot_ins.model != temp:
                robot_ins.set_chat_model(temp)
        elif msg.topic == "chat/temperature":
            temp = float(msg.payload.decode("utf-8"))
            if robot_ins.chat_temperature != temp:
                robot_ins.chat_temperature = temp
        elif msg.topic == "chat/top_p":
            temp = float(msg.payload.decode("utf-8"))
            if robot_ins.chat_top_p != temp:
                robot_ins.chat_top_p = temp
        elif msg.topic == "other/chat_offline":
            if msg.payload.decode("utf-8") == "1":
                robot_ins.chat_offline = True
            else:
                robot_ins.chat_offline = False
        elif msg.topic == "other/deep_think":
            if msg.payload.decode("utf-8") == "1":
                robot_ins.deep_think= True
            else:
                robot_ins.deep_think = False
        elif msg.topic == "motion/larm":
            temp = float(msg.payload.decode("utf-8"))
            if robot_ins.larm != temp:
                robot_ins.set_larm_rotation(temp, 3)
        elif msg.topic == "motion/rarm":
            temp = float(msg.payload.decode("utf-8"))
            if robot_ins.rarm != temp:
                robot_ins.set_rarm_rotation(temp, 3)
        elif msg.topic == "motion/body":
            temp = float(msg.payload.decode("utf-8"))
            if robot_ins.body != temp:
                robot_ins.set_body_rotation(temp, 3)
        elif msg.topic == "motion/foot":
            temp = float(msg.payload.decode("utf-8"))
            if robot_ins.foot != temp:
                robot_ins.set_foot_rotation(temp, 3)
        elif msg.topic == "motion/action_enable":
            temp = int(msg.payload.decode("utf-8"))
            if robot_ins.action_enable != bool(temp):
                robot_ins.action_enable = bool(temp)
        elif msg.topic == "other/wake_time":
            temp = float(msg.payload.decode("utf-8"))
            if robot_ins.wake_time != temp:
                robot_ins.wake_time = temp
        elif msg.topic == "other/volume":
            temp = float(msg.payload.decode("utf-8"))
            if robot_ins.volume != temp:
                robot_ins.volume = temp
        elif msg.topic == "other/drag":
            if msg.payload.decode("utf-8") == "1":
                self.drag = True
            else:
                self.drag = False
        elif msg.topic == "other/asr_offline":
            if msg.payload.decode("utf-8") == "1":
                robot_ins.asr_offline = True
            else:
                robot_ins.asr_offline = False
        elif msg.topic == "dialog/act":
            print(msg.payload.decode("utf-8"))
            if msg.payload.decode("utf-8") == "0":
                action.emotion_express(robot_ins, "happy")
            elif msg.payload.decode("utf-8") == "1":
                action.emotion_express(robot_ins, "scare")
            elif msg.payload.decode("utf-8") == "2":
                action.emotion_express(robot_ins, "angry")
            elif msg.payload.decode("utf-8") == "3":
                action.emotion_express(robot_ins, "upset")
            elif msg.payload.decode("utf-8") == "4":
                action.emotion_express(robot_ins, "curious")
            elif msg.payload.decode("utf-8") == "5":
                action.emotion_express(robot_ins, "laugh")

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

if __name__ == "__main__":
    MQTT_instance = new_class()
    MQTT_instance.run()