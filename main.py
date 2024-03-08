import QF_ASK as QF
import audio_process as AU
import os
import glob

filepath = "./audio/recorded_audio.wav"


def init():
    # 使用glob模块匹配路径下的所有文件
    files = glob.glob("audio/")
    # 遍历文件列表并删除每个文件
    for file in files:
        if os.path.isfile(file):  # 确保只删除文件，不删除目录
            os.remove(file)


if __name__ == '__main__':
    init()

    # AU.record(5, 16000, filepath)

    # text = AU.STT(filepath)[0]
    # print(text)

    QF.chat("Yi-34B-Chat", "'你好'的英文怎么说，然后能够列举下‘你好’的另一些英文表达吗？")

    """ 
    while True:
        ask = input("输入：\n")
        QF.chat(ask)
    """
