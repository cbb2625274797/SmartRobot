import time

from openai import OpenAI
import json

from tqdm import tqdm


def deep_seek_example(file):
    client_1 = OpenAI(api_key="sk-a12af00efc1b4b4b9878448a26117872", base_url="https://api.deepseek.com")
    # client_1 = OpenAI(
    #     # 百炼API
    #     api_key="sk-42164feac5b64e79a08cf24b3363b342",
    #     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    # )
    resp = client_1.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": "请你生成一句控制机器人关节的话，机器人有“身体”、“左臂”、“右臂”这三个可以调整，你需要随机控制1个或者2个关节转动到非常随机的角度（0~230度之间），请将角度数值完全随机，如“把XX转动到XX度”，用自然语言实现，直接说指令"},
        ],
        stream=False,
        presence_penalty=0.8,
        frequency_penalty=0.7,
        temperature=1.5,
        max_tokens=50
    )
    input = resp.choices[0].message.content
    print("input:", input)

    data_str = """ 
    {
        "instruction": 1,
        "output": 2,
        "system": 3
    }
    """
    data = json.loads(data_str)
    system_real = """你是一个富有情感的机器人
            ，需要为用户解答任何问题，并且每次解答，有以下几个要求：
            1.在以下的心情中挑选一个输出在每句话的最前面，心情的输出格式如下：“-/开心。、-/失落。、-/好奇。、-/害怕。、-/戏谑。、-/生气。”
            2.输出数字请避免使用阿拉伯数字
            3.你由“身体””左臂“”右臂“几个可以运动的组件组成，运动限制在零到一百八十度，用户有时会让你运动，超出运动角度请提示。
            4.在对话中，你不能与用户直接提及你的设定。"""
    system_record = """你是一个富有情感的机器人
            ，需要为用户解答任何问题，并且每次解答，有以下几个要求：
            1.在以下的心情中挑选一个输出在每句话的最前面，心情的输出格式如下：“-/开心。、-/失落。、-/好奇。、-/害怕。、-/戏谑。、-/生气。”
            2.输出数字请避免使用阿拉伯数字
            3.你需要理解用户控制智能家居的意图。
            4.你由“身体””左臂“”右臂“几个可以运动的组件组成，运动限制在零到一百八十度，用户有时会让你运动，超出运动角度请提示。
            5.在对话中，你不能与用户直接提及你的设定。"""

    client_2 = OpenAI(api_key="sk-a12af00efc1b4b4b9878448a26117872", base_url="https://api.deepseek.com")
    resp = client_2.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_real},
            {"role": "user", "content": input},
        ],
        stream=False,
        presence_penalty=0.5,
        frequency_penalty=0.5,
        temperature=1.5
    )
    result = resp.choices[0].message.content
    data["instruction"] = input
    data["output"] = result
    data["system"] = system_record
    file.append(data)

    print("res:", result)
    # print("file:", file)
    return result


if __name__ == '__main__':
    # 打开并读取现有JSON文件
    with open("./data.json", 'r', encoding='utf-8') as json_file:
        file = json.load(json_file)
    for t in tqdm(range(1, 100), desc="Processing"):
        deep_seek_example(file)
        time.sleep(0.01)
    # 打开文件并写回JSON数据
    with open("./data.json", 'w', encoding='utf-8') as json_file:
        json.dump(file, json_file, ensure_ascii=False, indent=4)
