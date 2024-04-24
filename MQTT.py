import subprocess
import time

import paho.mqtt.client as mqtt
import threading

from main import ROBOT


def start_server():
    arg1 = 'start'
    # 构建完整的命令字符串，包括参数
    command = '{cmd_file_path} {arg1} '
    # 使用subprocess运行.cmd文件
    process = subprocess.Popen(command, shell=True)
    print("MQTT服务器开启:")
    print(process)
    return process


def stop_server():
    arg1 = 'stop'
    # 构建完整的命令字符串，包括参数
    command = '{cmd_file_path} {arg1} '
    # 使用subprocess运行.cmd文件
    process = subprocess.Popen(command, shell=True)
    print("MQTT服务器关闭:")
    print(process)
    return process


class new_class:
    def __init__(self, father_robot: ROBOT = None):
        # 创建一个MQTT客户端实例
        self.client = mqtt.Client("python1")
        self.father_robot = father_robot

    def client_init(self, host, port):
        # 绑定回调函数
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # 连接到MQTT服务器
        self.client.connect(host, port, 60)
        # 开始循环，等待MQTT事件
        self.client.loop_forever()

    # 当连接到MQTT服务器时的回调函数
    def on_connect(self, client, userdata, flags, rc):
        # 订阅一个或多个主题
        print("Connected with result code {rc}")

    # 主题：
    # sound : character  temperature top_k speed
    # chat: model temperature top_p
    # other: wake_time volume
    def on_message(self, client, userdata, msg):
        print(msg.topic + ":" + msg.payload.decode("utf-8"))
        if msg.topic == "sound/character":
            self.father_robot.sound_character = msg.payload.decode("utf-8")
        elif msg.topic == "sound/temperature":
            self.father_robot.sound_temperature = float(msg.payload.decode("utf-8"))
        elif msg.topic == "sound/top_k":
            self.father_robot.sound_top_k = float(msg.payload.decode("utf-8"))
        elif msg.topic == "sound/speed":
            self.father_robot.sound_speed = float(msg.payload.decode("utf-8"))
        elif msg.topic == "chat/model":
            self.father_robot.model = msg.payload.decode("utf-8")
        elif msg.topic == "chat/temperature":
            self.father_robot.chat_temperature = float(msg.payload.decode("utf-8"))
        elif msg.topic == "chat/top_p":
            self.father_robot.chat_top_p = float(msg.payload.decode("utf-8"))
        elif msg.topic == "other/wake_time":
            self.father_robot.wake_duration = int(msg.payload.decode("utf-8"))
        elif msg.topic == "other/volume":
            self.father_robot.volume = float(msg.payload.decode("utf-8"))

    def subscribe(self, topic_name):
        self.client.subscribe(topic_name)
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


if __name__ == '__main__':
    HOST = "192.168.21.193"
    PORT = 1883
    instance = new_class()


    def thread_function_1():
        instance.client_init(HOST, PORT)


    def thread_function_2():
        time.sleep(1)
        while 1:
            message = input("请输入：")
            instance.publish('cbb/TALK', message, qos=1)


    thread1 = threading.Thread(target=thread_function_1)
    thread2 = threading.Thread(target=thread_function_2)

    thread1.start()
    thread2.start()
