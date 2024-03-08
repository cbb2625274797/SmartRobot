import sys

import requests
import json
from pydub import AudioSegment
from io import BytesIO
import json


# request会有问题，不支持使用
def request(text):
    # 设置请求的URL
    url = ('http://192.168.112.15:9880?refer_wav_path=C:/Users/cbb/Downloads/Compressed/雷电将军/vocal'
           '/vo_SGLQ002_9_raidenEi_01.wav&prompt_text=看你们的表情，应该读到了不错的故事吧&prompt_language=中文&text='
           + text + '&text_language=中文')

    # 发送GET请求
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 将响应内容读取为字节流
        audio_stream = BytesIO(response.content)

        # 假设音频流是WAV格式
        audio = AudioSegment.from_wav(audio_stream)
        return audio
    else:
        # 请求失败，打印错误信息
        print('请求失败，状态码：', response.status_code)


def post(refer_wav_path, refer_wav_text, text):
    # 设置URL和要发送的数据
    url = 'http://192.168.112.15:9880'
    data = {
        "refer_wav_path": refer_wav_path,
        "prompt_text": refer_wav_text,
        "prompt_language": "zh",
        "text": text,
        "text_language": "zh"
    }
    json_data = json.dumps(data)
    # print(json_data)

    # 设置请求头，指定内容类型为JSON
    headers = {
        'Content-Type': 'application/json',
    }
    # 发送POST请求
    response = requests.post(url, data=json_data, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        # 将响应内容读取为字节流
        audio_stream = BytesIO(response.content)

        # 假设音频流是WAV格式
        audio = AudioSegment.from_wav(audio_stream)
        return audio
    else:
        print("请求失败，状态码:", response.status_code)
        # 处理错误情况
        print(response.text)


if __name__ == '__main__':
    my_dict = {
        "开心": "开心",
        "害怕": "害怕",
        "生气": "生气",
        "失落": "失落",
        "好奇": "好奇",
        "戏谑": "戏谑"
    }
    # 将字典保存到JSON文件中
    with open('EmotionEngine/paimon/情绪代码.json', 'w') as f:
        json.dump(my_dict, f)
    exit(0)
    # 从JSON文件中读取字典
    with open('EmotionEngine/情绪代码.json', 'r') as f:
        loaded_dict = json.load(f)
    print(loaded_dict["1"])
    exit(0)

    audio1 = post("EmotionEngine/EmotionList/paimon/开心.wav",
                  "要不，我们两个也去看看吧，如果能帮上忙，就可以更早吃上万民堂的料理了",
                  "请确保你的POST请求返回的是有效的音频流数据，并且你正确处理了任何潜在的错误或异常。此外，根据你的具体需求，你可能还需要调整音频的质量、比特率等参数，这可以通过export方法的参数来实现。")
    # 将WAV转换为MP3并保存
    audio1.export("post.mp3", format="mp3")
    print("音频流已保存为 post.mp3")

    audio2 = request(
        "请确保你的POST请求返回的是有效的音频流数据，并且你正确处理了任何潜在的错误或异常。此外，根据你的具体需求，你可能还需要调整音频的质量、比特率等参数，这可以通过export方法的参数来实现。")
    audio1.export("get.mp3", format="mp3")
    print("音频流已保存为 get.mp3")
