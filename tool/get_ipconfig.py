import json
import os


def is_root_directory():
    markers = ['ipconfig.json', 'requirements.txt', '.git']
    current_dir = os.getcwd()
    for marker in markers:
        marker_path = os.path.join(current_dir, marker)
        if os.path.exists(marker_path):
            return True
    return False


def run():
    if is_root_directory():
        # 打开并读取JSON文件
        with open('ipconfig.json', 'r', encoding='utf-8') as file:
            ipconfig = json.load(file)
        return ipconfig
    else:
        print("当前目录不是运行根目录，不获取全局ip变量")


if __name__ == "__main__":
    ipconfig = run()
