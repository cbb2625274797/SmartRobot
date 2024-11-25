import json
import time
import wave

import librosa
import numpy as np
import pyaudio
import pygame
import sounddevice as sd
import webrtcvad
from aip import AipSpeech
from scipy.io.wavfile import write

from audio import GPT_SOVITS as SOVITS


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
    # print("录音已保存为 'recorded_audio.wav'")


def record_until_silence(duration, samplerate: int, filepath, max_time=10):
    # 初始化参数
    THRESHOLD_SECONDS = duration  # 静音持续时间，超过这个时间就停止录音
    CHUNK_SIZE = 160  # 每次读取的样本数量
    FORMAT = pyaudio.paInt16  # 格式
    CHANNELS = 1  # 单声道
    RATE: int = samplerate  # 采样率
    VAD_MODE = 1  # webrtcvad的模式，3是最严格的模式
    # 初始化PyAudio
    p = pyaudio.PyAudio()

    # 创建WebRTC的VAD对象
    vad = webrtcvad.Vad(VAD_MODE)

    # 打开音频流
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK_SIZE)

    # 初始化变量
    frames = []
    start_time = time.time()
    last_speech_time = start_time

    while True:
        # 读取音频数据
        data = stream.read(CHUNK_SIZE)

        # 将数据转换为numpy数组
        frame = np.frombuffer(data, dtype=np.int16)

        # 运行VAD
        if vad.is_speech(frame.tobytes(), RATE):
            last_speech_time = time.time()
            print(last_speech_time)

        # 检查是否超过了静音阈值
        if time.time() - last_speech_time > THRESHOLD_SECONDS:
            print("静音时间超过阈值，停止录音")
            # 保存语音帧
            frames.append(frame)
            return True
            break
        elif time.time() - start_time > max_time:
            # 保存语音帧
            frames.append(frame)
            print("录音时间超过阈值，停止录音")
            return False
            break

    # 停止录音
    stream.stop_stream()
    stream.close()
    p.terminate()

    # 将所有帧合并成一个大的numpy数组
    audio_data = np.concatenate(frames, axis=0)

    with wave.open(filepath, 'wb') as wave_file:
        FORMAT = 2
        wave_file.setparams((CHANNELS, FORMAT, RATE, len(audio_data), 'NONE', 'not compressed'))
        wave_file.writeframes(audio_data.astype(np.int16).tobytes())

    # 返回音频数据
    return audio_data, RATE


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


def is_audio_silent(audio_file_path, threshold=0.7):
    # 加载音频文件
    y, sr = librosa.load(audio_file_path, mono=True, sr=None)  # mono=True表示单声道
    if sr != 16000:
        raise ValueError("音频采样率必须为16kHz，但给定的采样率为{} kHz".format(sr / 1000))

    # 转换为16位PCM格式
    y_16bit = (y * (2 ** 15)).astype(np.int16)

    # 初始化VAD
    vad = webrtcvad.Vad(3)  # 模式3是最严格的

    # 分割音频为10毫秒的帧
    frames = np.array_split(y_16bit, int(len(y_16bit) / 160))  # 160 samples = 10 ms

    # 运行VAD
    is_speech = [bool(vad.is_speech(frame.tobytes(), sr)) for frame in frames]

    speech_frames = sum(is_speech)
    total_frames = len(is_speech)
    # 计算静音比例
    silence_ratio = (total_frames - speech_frames) / len(is_speech)

    # 判断静音
    if silence_ratio > threshold:  # 如果70%以上的帧被认为是静音，则认为整个音频是静音
        return True
    else:
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
    pygame.mixer.music.set_volume(volume)  # 设置音量
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
    record_until_silence(2, 16000, "recorded_audio.wav")
