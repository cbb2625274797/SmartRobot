import socket
import time

import requests
from pydub import AudioSegment
from io import BytesIO
import json
from main import sovits_server

url = sovits_server


def post(refer_wav_path, refer_wav_text, text):
    # 设置URL和要发送的数据
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
    response = requests.post(url, data=json_data, headers=headers, timeout=10)

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


def post_v2(
        refer_wav_path,
        refer_wav_text,
        text, top_k: int = 5,
        top_p: float = 1,
        temperature: float = 1,
        speed_factor: float = 1.0
):
    url_v2_tts = url + '/tts'
    # 设置URL和要发送的数据
    data = {
        "text": text,  # str.(required) text to be synthesized
        "text_lang": "zh",  # str.(required) language of the text to be synthesized
        "ref_audio_path": refer_wav_path,  # str.(required) reference audio path.
        "prompt_text": refer_wav_text,  # str.(optional) prompt text for the reference audio
        "prompt_lang": "zh",  # str.(required) language of the prompt text for the reference audio
        "top_k": top_k,  # int.(optional) top k sampling
        "top_p": top_p,  # float.(optional) top p sampling
        "temperature": temperature,  # float.(optional) temperature for sampling
        "text_split_method": "cut5",  # str.(optional) text split method, see text_segmentation_method.py for details.
        "batch_size": 6,  # int.(optional) batch size for inference
        "batch_threshold": 0.75,  # float.(optional) threshold for batch splitting.
        "split_bucket": True,  # bool.(optional) whether to split the batch into multiple buckets.
        "speed_factor": speed_factor,  # float.(optional) control the speed of the synthesized audio.
        "fragment_interval": 0.3,  # float.(optional) to control the interval of the audio fragment.
        "seed": -1,  # int.(optional) random seed for reproducibility.
        "media_type": "wav",  # str.(optional) media type of the output audio, support "wav", "raw", "ogg", "aac".
        "streaming_mode": False,  # bool.(optional) whether to return a streaming response.
    }
    json_data = json.dumps(data)
    # print(json_data)

    # 设置请求头，指定内容类型为JSON
    headers = {
        'Content-Type': 'application/json',
    }
    # 发送POST请求
    response = requests.post(url_v2_tts, data=json_data, headers=headers, timeout=10)

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


def commanmd(command: str):
    if command == "exit":
        url_command = url + "/control?command=exit"
    elif command == "restart":
        url_command = url + "/control?command=restart"
        print("等待重启...")
    else:
        url_command = url + "/control?command=??"
        print("未知命令")
    try:
        # 发送GET请求
        response = requests.get(url_command)
    except Exception:
        if command == "restart":
            time.sleep(12)
            print("重启成功")
        elif command == "exit":
            exit(0)
            print("无法运行时退出！")


def set_gpt_weights(character: int):
    if character == 0:
        weights_path = "GPT_weights/paimon-e15.ckpt"
    elif character == 1:
        weights_path = "GPT_weights/funignna-e50.ckpt"
    elif character == 2:
        weights_path = "GPT_weights/hutao-e15.ckpt"
    elif character == 3:
        weights_path = "GPT_weights/shenli-e50.ckpt"
    elif character == 4:
        weights_path = "GPT_weights/wanye-e10.ckpt"
    else:
        print("未知角色！")
        return 0

    url_set = url + "/set_gpt_weights?weights_path=" + weights_path
    try:
        # 发送GET请求
        response = requests.get(url_set)
        if response.status_code == 200:
            print("GPT模型切换成功！")
        else:
            print(response.text)
            print("GPT模型切换失败！")
    except Exception:
        print("发送Get失败，请检查GPT-SOVITS服务器！")


def set_sovits_weights(character: int):
    if character == 0:
        weights_path = "SoVITS_weights/paimon_e1_s2105.pth"
    elif character == 1:
        weights_path = "SoVITS_weights/funingna_e8_s1224.pth"
    elif character == 2:
        weights_path = "SoVITS_weights/hutao_e8_s832.pth"
    elif character == 3:
        weights_path = "SoVITS_weights/shenli_e8_s904.pth"
    elif character == 4:
        weights_path = "SoVITS_weights/wanye_e8_s1824.pth"
    else:
        print("未知角色！")
        return 0
    url_set = url + "/set_sovits_weights?weights_path=" + weights_path
    try:
        # 发送GET请求
        response = requests.get(url_set)
        if response.status_code == 200:
            print("SoVITS模型切换成功！")
        else:
            print(response.text)
            print("SoVITS模型切换失败！")
    except Exception:
        print("发送Get失败，请检查GPT-SOVITS服务器！")


# 0 派蒙
# 1	芙宁娜
# 2	胡桃
# 3 神里绫华
# 4	万叶
def set_character(character: int):
    if character == 0:
        print("切换角色：派蒙")
    elif character == 1:
        print("切换角色：芙宁娜")
    elif character == 2:
        print("切换角色：胡桃")
    elif character == 3:
        print("切换角色：神里绫华")
    elif character == 4:
        print("切换角色：万叶")

    set_gpt_weights(character)
    set_sovits_weights(character)
    print("切换结束！")


if __name__ == '__main__':
    set_character(0)
    exit()
    audio1 = post_v2("EmotionEngine/EmotionList/paimon/开心.wav",
                     "要不，我们两个也去看看吧，如果能帮上忙，就可以更早吃上万民堂的料理了",
                     "近日，多国外交部门及驻外使领馆发布公告，提醒本国公民关注当前中东安全局势，非必要不前往或谨慎前往以色列、伊朗等国。我驻以使馆提醒在以中国公民注意安全当地时间12"
                     "日，中国驻以色列使馆再次提醒在以中国公民密切跟踪当地安全形势和使馆发出的安全提醒，时刻绷紧安全防范这根弦，坚持非必要不外出，坚决避免前往高风险地区和敏感地点。使馆表示，当前我有关安全提醒仍处于“提醒中国公民暂勿前往以色列”状态，请大家高度重视，近期暂勿前往。如仍坚持前往，有可能面临极高安全风险，并可能影响获得协助的实效。多国外交部门及驻外使领馆发布提醒12日，法国外交部建议法国公民不要前往伊朗、黎巴嫩、以色列、巴勒斯坦。法国外交部还在社交媒体上表示，法国驻伊朗外交官员的亲属将撤回法国。印度外交部12日发布公告说，鉴于伊朗和以色列目前的局势，建议所有印度公民不要前往伊朗和以色列，直至另行通知。")

    # audio1 = post("EmotionEngine/EmotionList/paimon/开心.wav",
    #               "要不，我们两个也去看看吧，如果能帮上忙，就可以更早吃上万民堂的料理了",
    #               "请确保你的POST请求返回的是有效的音频流数据，并且你正确处理了任何潜在的错误或异常。")
    # 将WAV转换为MP3并保存
    audio1.export("post.mp3", format="mp3")
    print("音频流已保存为 post.mp3")

    exit(0)

    set_character(4)

    exit(0)
    my_dict = {
        "开心": "嗯，能有一个让我暂时安身的地方，我很开心。",
        "害怕": "恐怕那时候的他就已经受了碎神之力的影响。",
        "生气": "要是天目幽野正在无差别，行凶不赶快阻止他，还有更多人会遭遇同样的不幸。",
        "失落": "说的也是，感谢各位的关心。幸好这些事对我而言都是过去了。",
        "好奇": "此事的讨论先告一段落，你们两位为什么会找到这里来？",
        "戏谑": "大姐头，对这种事情恐怕是毫无兴趣，我便想着不如请你来体会一番。"
    }
    # 将字典保存到JSON文件中
    with open('EmotionEngine/EmotionList/wanye/情绪参考文本.json', 'w') as f:
        json.dump(my_dict, f)
    exit(0)
