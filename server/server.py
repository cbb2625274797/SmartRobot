import os
import subprocess
import threading
import time

import MQTT


class SERVER:
    def __init__(self, emqx_path, pixel_bat_path, sovits_bat_path, game_exe_path, host="127.0.0.1", port: int = 1883):
        """
        初始化
        :param emqx_path: emqx的路径
        :param pixel_bat_path: 视频服务器的启动脚本路径
        :param sovits_bat_path: 语音脚本的路径
        :param host: 本机地址
        :param port: MQTT端口
        """
        self.host = host
        self.port = port
        self.emqx_path = emqx_path
        self.pixel_bat_path = pixel_bat_path
        self.sovits_bat_path = sovits_bat_path
        self.game_exe_path = game_exe_path
        self.stop_flag = False

        self.thread1 = threading.Thread(target=self.thread_function_1)
        self.thread3 = threading.Thread(target=self.thread_function_3)
        self.thread4 = threading.Thread(target=self.thread_function_4)
        self.thread5 = threading.Thread(target=self.thread_function_5)

    def thread_function_1(self):
        """
        EMQX（负责MQTT的通信）
        :return:
        """
        self.MQTT_start()
        # MQTT.client_init(self.host, self.port)

    def thread_function_3(self):
        """
        视频流送服务器
        :return:
        """
        # 使用subprocess.run()方法执行bat文件
        try:
            subprocess.run([self.pixel_bat_path], check=True, shell=True)
            print("pixel streaming 文件关闭。")
        except subprocess.CalledProcessError as e:
            print(f"执行批处理文件时发生错误：{e}")

    def thread_function_4(self):
        """
        音频合成服务器
        :return:
        """
        # 定义要切换到的新路径
        new_path = "G:/AI/GPT-SoVITS-beta0306"  # 请将此路径替换为你想切换到的实际路径
        # 尝试切换工作目录
        try:
            os.chdir(new_path)
        except FileNotFoundError:
            print(f"错误：路径 {new_path} 不存在，请检查路径是否正确。")

        # 使用subprocess.run()方法执行bat文件
        try:
            subprocess.run([self.sovits_bat_path], check=True, shell=True)
            print("GPT-SOVITS 服务器关闭。")
        except subprocess.CalledProcessError as e:
            print(f"执行批处理文件时发生错误：{e}")

    def thread_function_5(self):
        """
        视频主体
        :return:
        """
        time.sleep(5)
        # 打开UI可执行文件
        args = [
            "-AudioMixer",
            "-PixelStreamingIP=localhost",
            "-PixelStreamingPort=8888",
            "-ResX=800",
            "-ResY=480"
        ]
        # 构建完整的命令
        command = [self.game_exe_path] + args
        # 使用subprocess.run执行命令
        try:
            subprocess.run(command, check=True)
            print("SMART_ROBOT.exe 已退出。")
        except subprocess.CalledProcessError as e:
            print(f"运行 SMART_ROBOT.exe 时出现错误: {e}")

    def run(self):
        self.thread1.start()
        self.thread3.start()
        self.thread4.start()
        self.thread5.start()

    def MQTT_start(self):
        # 指定.cmd文件的路径
        MQTT.stop_server(self.emqx_path)
        time.sleep(3)
        MQTT.start_server(self.emqx_path)

    def MQTT_stop(self):
        # 指定.cmd文件的路径
        MQTT.stop_server(self.emqx_path)


if __name__ == '__main__':
    MQTT_server_path = r"E:/emqx4/bin/emqx.cmd"
    pixel_bat_path = r"G:/SMART_ROBOT/PixelStreamingInfrastructure-UE5.3/SignallingWebServer/runAWS_WithTURN.bat"
    sovits_bat_path = r"G:/AI/GPT-SoVITS-beta0306/开启v2接口服务.bat"
    game_exe_path = "G:/SMART_ROBOT/Windows/SMART_ROBOT.exe"

    # 开启
    server_ins = SERVER(MQTT_server_path, pixel_bat_path, sovits_bat_path, game_exe_path)
    server_ins.run()
