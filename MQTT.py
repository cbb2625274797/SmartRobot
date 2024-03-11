import subprocess
import paho.mqtt.client as mqtt

HOST = "192.168.37.15"
PORT = 1883
# 创建一个MQTT客户端实例
client = mqtt.Client("python1")


def start_server():
    # 指定.cmd文件的路径
    cmd_file_path = 'E:/emqx4/bin/emqx.cmd'
    arg1 = 'start'
    # 构建完整的命令字符串，包括参数
    command = f'{cmd_file_path} {arg1} '
    # 使用subprocess运行.cmd文件
    process = subprocess.Popen(command, shell=True)
    print("MQTT服务器开启:")
    print(process)
    return process


def stop_server():
    # 指定.cmd文件的路径
    cmd_file_path = 'E:/emqx4/bin/emqx.cmd'
    arg1 = 'stop'
    # 构建完整的命令字符串，包括参数
    command = f'{cmd_file_path} {arg1} '
    # 使用subprocess运行.cmd文件
    process = subprocess.Popen(command, shell=True)
    print("MQTT服务器关闭:")
    print(process)
    return process


def client_init():
    # 绑定回调函数
    client.on_connect = on_connect
    client.on_message = on_message

    # 如果需要用户名和密码，可以添加认证
    # client.username_pw_set(username, password)
    # 连接到MQTT服务器
    client.connect(HOST, 1883, 60)
    # 开始循环，等待MQTT事件
    subscribe("pc2")
    subscribe("pc1")
    client.loop_forever()


# 当连接到MQTT服务器时的回调函数
def on_connect(client, userdata, flags, rc):
    # 订阅一个或多个主题
    print(f"Connected with result code {rc}")


def subscribe(topic_name):
    client.subscribe(topic_name)
    print("subscribe:" + topic_name)


def on_message(client, userdata, msg):
    print(msg.topic + ":" + msg.payload.decode("utf-8"))


if __name__ == '__main__':
    stop_server()
    start_server()
