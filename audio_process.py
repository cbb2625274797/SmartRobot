from aip import AipSpeech
import pygame
import json
import speech_recognition as sr
import pypinyin
import sounddevice as sd
from scipy.io.wavfile import write
import GPT_SOVITS as SOVITS
import numpy as np
import datetime


# 设置录音参数
def record(duration, samplerate, filepath):
    # 使用sounddevice录制音频
    global recording
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
    # print(return_value)
    try:
        print(return_value.get('result')[0])
        return return_value.get('result')
    except Exception:
        return ""


def BD_TTS(text, filename):
    result = client.synthesis(text, 'zh', 1, {
        'vol': 5, 'per': 5003
    })
    # print(result)
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open(filename, 'wb') as f:
            f.write(result)


def remove_element(lst, element):
    while element in lst:
        lst.remove(element)
    return lst


def contains_sublist(lst, sublist):
    return any(lst[i:i + len(sublist)] == sublist for i in range(len(lst) - len(sublist) + 1))


def recognize():
    datetime1 = datetime.datetime.now()
    audio_file = "./audio/recorded_audio.wav"
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    try:
        str = r.recognize_sphinx(audio, language="zh-CN")
        pinyin = pypinyin.pinyin(str, style=pypinyin.NORMAL)
        r = remove_element(pinyin, [' '])
        if contains_sublist(r, [['bei'], ['jing']]):
            return True
        datetime2 = datetime.datetime.now()
        print("识别耗时：", datetime2 - datetime1)
        print("识别结果：", r)
    except Exception as e:
        print(e)
        return False
    return False


def SOVITS_TTS(character: str, emotion: str, text, filename):
    # 从JSON文件中读取字典
    with open('EmotionEngine/EmotionList/' + character + '/情绪参考文本.json', 'r') as f:
        loaded_dict = json.load(f)
    refer_text = loaded_dict[emotion]
    refer_path = "./EmotionEngine/EmotionList/" + character + "/" + emotion + ".wav"
    audio = SOVITS.post_v2(refer_wav_path=refer_path, refer_wav_text=refer_text, text=text)
    # 将WAV转换为MP3并保存
    audio.export(filename, format="mp3")


def play(file_path, volume: float = 1):
    # 初始化pygame音频模块
    pygame.mixer.init()
    pygame.mixer.music.set_volume(volume)  # 设置为一半音量
    # 加载MP3、wav文件
    pygame.mixer.music.load(file_path)
    # 播放MP3、wav文件
    pygame.mixer.music.play()
    # 等待播放完成（如果需要）
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    # 退出pygame（可选）
    pygame.quit()


if __name__ == '__main__':
    play("./audio/wakeup.wav")
    # print(STT("16k.wav"))
    # SOVITS_TTS("hutao", "开心", "大家好，我是普通的TTS应用生成的音频", "GPTSOVITS.mp3")
    pass
    # record(5, 16000, "./audio/recorded_audio.wav")

    # STT("./audio/recorded_audio.wav")
    # SOVITS_TTS("paimon", '开心',
    #            "携手最具影响力的中文知识平台，用知识的价值提升品牌的价值。",
    #            "TTS.mp3")
