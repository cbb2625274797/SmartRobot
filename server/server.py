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

        self.thread1 = threading.Thread(target=self.thread_function_1)  # emqx
        self.thread3 = threading.Thread(target=self.thread_function_3)  # pixel streaming
        self.thread4 = threading.Thread(target=self.thread_function_4)  # 音频合成服务器
        self.thread5 = threading.Thread(target=self.thread_function_5)  # 运行游戏

    def thread_function_1(self):
        """
        EMQX（负责MQTT的通信）
        :return:
        """
        try:
            self.MQTT_start()
            # MQTT.client_init(self.host, self.port)
        except Exception as e:
            print(f"MQTT服务器启动失败：{e}")

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
            print(f"视频流送服务器启动失败：{e}")

    def thread_function_4(self):
        """
        音频合成服务器
        :return:
        """
        # 定义要切换到的新路径
        new_path = os.path.dirname(sovits_bat_path)  # 请将此路径替换为你想切换到的实际路径
        # 尝试切换工作目录
        try:
            os.chdir(new_path)
        except Exception as e:
            print(e)

        # 使用subprocess.run()方法执行bat文件
        try:
            subprocess.run([self.sovits_bat_path], check=True, shell=True)
            print("GPT-SOVITS 服务器关闭。")
        except subprocess.CalledProcessError as e:
            print(f"音频服务器启动失败：{e}")

    def thread_function_5(self):
        """
        视频主体
        :return:
        """
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
        time.sleep(10)
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
    import os
    project_path = ""
    # 获取根目录
    root_dir = os.path.dirname(os.path.abspath(__file__))
    while not os.path.exists(os.path.join(root_dir, 'ipconfig.json')):
        project_path = os.path.dirname(root_dir)
        project_path = os.path.dirname(project_path)
        break

    if project_path == "":
        print("找不到根目录，请确保文件完整")
        exit()
    else:
        MQTT_server_path = project_path + "/emqx4/bin/emqx.cmd"
        pixel_bat_path = project_path + "/SMART_ROBOT_UE5.5\PixelStreamingInfrastructure\SignallingWebServer\platform_scripts\cmd\start.bat"
        sovits_bat_path = project_path + "/GPT-SoVITS2-241224/开启v2接口服务.bat"
        game_exe_path = project_path + "/SMART_ROBOT_UE5.5\Windows\SMART_ROBOT.exe"

        # 开启
        server_ins = SERVER(MQTT_server_path, pixel_bat_path, sovits_bat_path, game_exe_path)
        server_ins.run()
