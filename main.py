import threading
import time

import MQTT
import robot


class orangepi_server:
    def __init__(self, host, ):
        """
        进行初始化
        :param host:主机地址
        """
        # MQTT参数
        self.ROBOT_instance = None
        self.MQTT_instance = None
        self.MQTT_port = 1883
        self.host = host

        self.thread_robot_ins = threading.Thread(target=self.robot_thread)
        self.thread_mqtt_ins = threading.Thread(target=self.mqtt_thread)

    def run(self):
        self.thread_mqtt_ins.start()
        self.thread_robot_ins.start()

        while not self.ROBOT_instance:  # 等待机器人初始化完成
            time.sleep(0.01)
        self.ROBOT_instance.MQTT_instance = self.MQTT_instance

        while not self.MQTT_instance.init_ok:  # 等待MQTT初始化完成
            time.sleep(0.01)
        self.MQTT_instance.father_robot = self.ROBOT_instance

        print("初始化完成")

    def robot_thread(self):
        """
        新建机器人
        :return:
        """
        # self.ROBOT_instance = robot.ROBOT("ERNIE-3.5-4K-0205", host=MQTT_server, mode="text")·
        self.ROBOT_instance = robot.ROBOT("qwen2.5_3b", host=MQTT_ip, mode="text")
        self.ROBOT_instance.run()

    def mqtt_thread(self):
        """
        进行MQTT的操作
        :return:
        """
        self.MQTT_instance = MQTT.new_class(self.host, self.MQTT_port)
        self.MQTT_instance.run()


if __name__ == '__main__':
    from config.ip_config import MQTT_ip

    # 运行
    instance = orangepi_server(MQTT_ip)
    instance.run()
