import os


def get_project_root():
    # 获取当前文件的完整路径
    current_file_path = os.path.abspath(__file__)

    # 获取当前文件所在的目录
    current_directory = os.path.dirname(current_file_path)

    # 设置最大循环次数
    max_iterations = 1000000
    iterations = 0

    while os.path.basename(current_directory) != "SmartRobot" and iterations < max_iterations:
        current_directory = os.path.dirname(current_directory)
        iterations += 1

    # 如果循环次数达到上限，返回当前目录
    if iterations == max_iterations:
        return current_directory

    return current_directory


project_root = get_project_root()
chat_system_prompt = project_root + '/server/system prompt'
