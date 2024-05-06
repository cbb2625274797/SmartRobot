import MQTT
import threading
import time
import os
import robot


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
        self.ROBOT_instance = robot.ROBOT("ERNIE-Bot", host=MQTT_server, mode="text")
        self.ROBOT_instance.run()

    def thread_function_2(self):
        """
        进行MQTT的操作
        :return:
        """
        self.MQTT_instance = MQTT.new_class(self.host, self.MQTT_port)
        self.MQTT_instance.run()


sovits_server = 'http://192.168.145.193:9880'
UI_server = 'http://192.168.145.193:8080'
MQTT_server = "192.168.145.193"

if __name__ == '__main__':
    # 清理临时文件
    cleanup()

    # host = "192.168.21.193"
    time.sleep(1)
    instance = orangepi_server(MQTT_server)
    instance.run()
