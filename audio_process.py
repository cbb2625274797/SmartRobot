from aip import AipSpeech
import pygame
import os
import pyttsx3
import sounddevice as sd
from scipy.io.wavfile import write
import GPT_SOVITS as SOVITS


# 设置录音参数
def record(duration, samplerate, filename):
    # 使用sounddevice录制音频
    print("开始录音...")
    myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()  # 等待录音结束
    print("录音结束")

    # 将录制的音频保存为WAV文件
    write(filename, samplerate, myrecording)
    print(f"音频文件已保存为 {filename}")


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
    # 识别本地文件
    # print(return_value.get('result')[0])
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


def SOVITS_TTS(text, filename):
    audio = SOVITS.post("./EmotionEngine/EmotionList/paimon/开心.wav", "要不，我们两个也去看看吧，如果能帮上忙，就可以更早吃上万民堂的料理了", text)
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
