import os

from openai import OpenAI
import base64


def qwenvl_ol_request(client, messages, ):
    completion = client.chat.completions.create(
        model="qwen2-vl-7b-instruct",
        messages=messages,
        stream=True
    )
    return completion


messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
                # 使用格式化字符串 (f-string) 创建一个包含 BASE64 编码图像数据的字符串。
                # "image_url": {"url": f"data:image/jpeg;base64,{encode_image('./test.jpg')}"},
            },
            {
                "type": "text", "text": "这是什么?"
            }
        ]
    },
    {
        "role": "assistant",
        "content": "这是一个女孩和一只狗。"
    },
    {
        "role": "user",
        "content": "对了！回答得不错！那你看下那只狗是什么颜色的"
    }
]


def remove_request_pic(json_str):
    print(json_str)
    for message in json_str:
        if isinstance(message['content'], list):
            new_content = []
            for item in message['content']:
                if item['type'] != 'image_url':
                    new_content.append(item)
            message['content'] = new_content
    print(json_str)
    return json_str


def qwen_ol_example():
    # base64_image = encode_image("test.png")
    client = OpenAI(
        # 百炼API
        api_key="sk-42164feac5b64e79a08cf24b3363b342",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    resp = qwenvl_ol_request(client, messages, )
    print("流式输出内容为：")
    for chunk in resp:
        print(chunk.model_dump_json())


def deep_seek_example():
    client = OpenAI(api_key="sk-a12af00efc1b4b4b9878448a26117872", base_url="https://api.deepseek.com")

    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": """
            你是一个富有情感的机器人，叫做小斌
            ，需要为用户解答任何问题，并且每次解答，有以下几个要求：
            1.在以下的心情中挑选一个输出在每句话的最前面，心情的输出格式如下：“-/开心。、-/失落。、-/好奇。、-/害怕。、-/戏谑。、-/生气。”
            2.输出数字请避免使用阿拉伯数字
            3.你需要理解用户控制智能家居的意图，并且告诉用户"xxx未连接"。
            4.你由“身体””左臂“”右臂“几个可以运动的组件组成，运动限制在零到一百八十度，用户有时会让你运动，超出运动角度请提示。
            以上规则中第一条必须遵守，其他只需要记住，但是不要与用户提及
            """},
            {"role": "user", "content": "你好，请你介绍下你自己"},
        ],
        stream=True
    )

    for chunk in resp:
        print(chunk.model_dump_json())
    for chunk in resp:
        result = chunk.choices[0].delta.content
        print(result)


if __name__ == "__main__":
    deep_seek_example()
