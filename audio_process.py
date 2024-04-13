from aip import AipSpeech
import pygame
import json
import pyttsx3
import sounddevice as sd
from scipy.io.wavfile import write
import GPT_SOVITS as SOVITS
import numpy as np


# 设置录音参数
def record(duration, samplerate, filepath):
    # 使用sounddevice录制音频
    print("开始录音...")
    myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()  # 等待录音结束
    print("录音结束")

    # WAV文件需要的采样率（通常为整数）和位深度（通常为16）
    wav_fs = int(samplerate)
    wav_dtype = np.int16  # 16位整数

    # 确保录音数据的位深度与WAV文件匹配
    if myrecording.dtype != wav_dtype:
        recording = (myrecording * (2 ** 15 - 1)).astype(wav_dtype)

        # 保存为WAV文件
    write(filepath, wav_fs, recording)
    print("录音已保存为 'output.wav'")


""" 你的 APPID AK SK """
APP_ID = '53924893'
API_KEY = '635cemfBDH2Bc1E6kGBDntrW'
SECRET_KEY = 'WYQ0EOTQ0lPHJXUTlLFyLBCYVyTfN4Sd'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 读取文件
def get_file_content(filepath):
    with open(filepath, 'rb') as fp:
        return fp.read()


def STT(filepath):
    return_value = client.asr(get_file_content(filepath), 'wav', 16000, {'dev_pid': 1537})
    # 识别文件
    print(return_value)
    print(return_value.get('result')[0])
    return return_value.get('result')


def BD_TTS(text, filename):
    result = client.synthesis(text, 'zh', 1, {
        'vol': 5, 'per': 5003
    })
    # print(result)
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open(filename, 'wb') as f:
            f.write(result)


def PYTTS(text, filename):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def SOVITS_TTS(character: str, emotion: str, text, filename):
    # 从JSON文件中读取字典
    with open('EmotionEngine/EmotionList/' + character + '/情绪参考文本.json', 'r') as f:
        loaded_dict = json.load(f)
    refer_text = loaded_dict[emotion]
    refer_path = "./EmotionEngine/EmotionList/" + character + "/" + emotion + ".wav"
    audio = SOVITS.post(refer_path, refer_text, text)
    # 将WAV转换为MP3并保存
    audio.export(filename, format="mp3")


def play(mp3_file_path):
    # 初始化pygame音频模块
    pygame.mixer.init()
    # 加载MP3文件
    pygame.mixer.music.load(mp3_file_path)
    # 播放MP3文件
    pygame.mixer.music.play()
    # 等待播放完成（如果需要）
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    # 退出pygame（可选）
    pygame.quit()


if __name__ == '__main__':
    pass
    # record(5, 16000, "./audio/recorded_audio.wav")

    # STT("./audio/recorded_audio.wav")
    # SOVITS_TTS("paimon", '开心',
    #            "携手最具影响力的中文知识平台，用知识的价值提升品牌的价值。",
    #            "TTS.mp3")
