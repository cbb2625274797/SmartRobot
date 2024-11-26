import os
import glob


def count_lines_of_code(directory):
    total_lines = 0
    total_files = 0
    for filename in glob.iglob(os.path.join(directory, '**', '*.py'), recursive=True):
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            # 过滤空行和以#开头的注释行
            non_empty_and_non_comment_lines = [line for line in lines if
                                               line.strip() and not line.strip().startswith('#')]
            total_lines += len(non_empty_and_non_comment_lines)
            total_files += 1
    return total_lines, total_files


# 指定项目根目录
project_directory = 'C:/Users/cbb/OneDrive/毕业设计文档同步/SmartRobot'  # 请替换为你的项目路径

lines, files = count_lines_of_code(project_directory)
print(f"项目中共有 {files} 个Python文件，总代码行数为 {lines} 行。")
