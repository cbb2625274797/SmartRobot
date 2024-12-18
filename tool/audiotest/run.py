import os

import audio.GPT_SOVITS as SOVITS
from tqdm import tqdm

import audio.audio_process as audio_process
import time


def read(filename):
    # 打开文件
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 如果需要去除每行末尾的换行符
    lines = [line.strip() for line in lines]
    return lines


def generate(list, index_in, c_num):
    characters = ["paimon", "funingna", "hutao", "shenli", "wanye"]
    execution_time = []
    sentences = read(list)
    for index, sentence in tqdm(enumerate(sentences), total=len(sentences)):
        filename = f"./tools/audiotest/{characters[c_num]}.{index_in + index}.MP3"
        # print(filename)
        # 想要切换到的目录
        new_dir = "C:/Users/cbb/OneDrive/毕业设计文档同步/SmartRobot/"
        os.chdir(new_dir)
        start_time = time.perf_counter()
        audio_process.SOVITS_TTS(characters[c_num], "开心", sentence, filename)
        end_time = time.perf_counter()
        new_dir = "C:/Users/cbb/OneDrive/毕业设计文档同步/SmartRobot/tools/audiotest"
        os.chdir(new_dir)
        execution_time.append(len(sentence) / (end_time - start_time))
    return sum(execution_time) / len(execution_time)


if __name__ == '__main__':
    character_num = 1
    SOVITS.set_character(1)
    generate("list6.txt", 0, 0)
    # for i in range(0, 5):
    #     character_num = i
    #     SOVITS.set_character(i)
        #time.sleep(10)
        # list1_speed = generate("list1.txt", 0, i)
        # list2_speed = generate("list2.txt", 10, i)
        # list3_speed = generate("list3.txt", 25, i)
        # list4_speed = generate("list4.txt", 35, i)
        # print(list1_speed + list2_speed / 2, list3_speed + list4_speed / 2)
