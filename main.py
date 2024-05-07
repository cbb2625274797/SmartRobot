import MQTT
import threading
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

        self.thread1 = threading.Thread(target=self.thread_function_1, args=())
        self.thread2 = threading.Thread(target=self.thread_function_2)

    def run(self):
        self.thread2.start()
        self.thread1.start()

        self.thread1.join()
        self.ROBOT_instance.MQTT_instance = self.MQTT_instance
        self.MQTT_instance.father_robot = self.ROBOT_instance

    def thread_function_1(self):
        """
        新建机器人
        :return:
        """
        self.ROBOT_instance = robot.ROBOT("ERNIE-3.5-4K-0205", host=MQTT_server, mode="text")
        self.ROBOT_instance.run()

    def thread_function_2(self):
        """
        进行MQTT的操作
        :return:
        """
        self.MQTT_instance = MQTT.new_class(self.host, self.MQTT_port)
        self.MQTT_instance.run()


sovits_server = 'http://192.168.215.15:9880'
UI_server = 'http://192.168.215.15:8080'
MQTT_server = "192.168.215.15"

if __name__ == '__main__':
    # 运行
    instance = orangepi_server(MQTT_server)
    instance.run()
