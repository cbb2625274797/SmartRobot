import threading
import time

import MQTT


class SERVER:
    def __init__(self, emqx_path, host="127.0.0.1", port: int = 1883):
        """
        初始化
        :param emqx_path: emqx的路径
        :param host: 本机地址
        :param port: MQTT端口
        """
        self.host = host
        self.port = port
        self.emqx_path = emqx_path
        self.stop_flag = False

        self.thread1 = threading.Thread(target=self.thread_function_1)
        self.thread2 = threading.Thread(target=self.thread_function_2)

    def thread_function_1(self):
        """
        负责MQTT的通信
        :return:
        """
        self.MQTT_start()
        MQTT.client_init(self.host, self.port)

    def thread_function_2(self):
        """
        其他逻辑处理
        :return:
        """
        while True:
            time.sleep(1)
            if self.stop_flag:
                self.stop()
                self.stop_flag = False

    def run(self):
        self.thread1.start()
        self.thread2.start()

    def stop(self):
        self.MQTT_stop()

    def MQTT_start(self):
        # 指定.cmd文件的路径
        MQTT.stop_server(self.emqx_path)
        time.sleep(3)
        MQTT.start_server(self.emqx_path)

    def MQTT_stop(self):
        # 指定.cmd文件的路径
        MQTT.stop_server(self.emqx_path)


if __name__ == '__main__':
    server_ins = SERVER('E:/emqx4/bin/emqx.cmd')
    server_ins.run()
    time.sleep(10)
    server_ins.stop_flag = True
