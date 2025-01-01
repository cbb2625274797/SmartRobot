import threading
import time

import MQTT
import robot
import json


class orangepi_client:
    def __init__(self,):
        """
        进行初始化
        :param host:主机地址
        """
        # MQTT参数
        self.ROBOT_instance = None
        self.MQTT_instance = None
        self.MQTT_init_ok = False
        self.robot_init_ok = False
        self.client_init_ok = False

        # 打开并读取JSON文件
        with open('ipconfig.json', 'r', encoding='utf-8') as file:
            self.ipconfig = json.load(file)
        self.thread_robot = threading.Thread(target=self.thread_function_1, args=())
        self.thread_mqtt = threading.Thread(target=self.thread_function_2)

    def run(self):
        self.thread_mqtt.start()
        self.thread_robot.start()
        while not self.MQTT_init_ok or not self.robot_init_ok:
            if not self.MQTT_init_ok:
                print("MQTT初始化中...")
            elif not self.robot_init_ok:
                print("机器人初始化中...")
            time.sleep(1)
        self.ROBOT_instance.MQTT_instance = self.MQTT_instance
        self.MQTT_instance.father_robot = self.ROBOT_instance

        self.client_init_ok = True
        print("初始化完成")

    def thread_function_1(self):
        """
        新建机器人
        :return:
        """
        # self.ROBOT_instance = robot.ROBOT("ERNIE-3.5-8K", host=MQTT_server, mode="text")
        self.ROBOT_instance = robot.ROBOT("Qwen2.5_32b_q2", mode="audio")
        # self.ROBOT_instance = robot.ROBOT("ERNIE-4.0-8K", mode="audio")
        self.robot_init_ok = True
        while not self.client_init_ok:
            time.sleep(0.1)
        self.ROBOT_instance.run()

    def thread_function_2(self):
        """
        进行MQTT的操作
        :return:
        """
        self.MQTT_instance = MQTT.new_class(self.ipconfig["MQTT_server"], self.ipconfig["MQTT_port"])
        self.MQTT_init_ok = True
        while not self.client_init_ok:
            time.sleep(0.1)
        self.MQTT_instance.run()


if __name__ == '__main__':
    # 运行
    instance = orangepi_client()
    instance.run()
