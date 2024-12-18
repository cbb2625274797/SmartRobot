import json

from openai import OpenAI
import os
import base64

bailian_client = OpenAI(
        # 百炼API
        api_key="sk-42164feac5b64e79a08cf24b3363b342",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def request(url):
    completion = bailian_client.chat.completions.create(
            model="qwen2-vl-7b-instruct",
            messages=messages,
            stream=True
    )
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
                # 使用格式化字符串 (f-string) 创建一个包含 BASE64 编码图像数据的字符串。
                # "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
            },
            {
                "type": "text", "text": "这是什么?"
            }
        ]
    },
    {
        "role": "assistant", "content": "这是一个女孩和一只狗。"
    },
    {
        "role": "user", "content": "对了！回答得不错！那你看下那只狗是什么颜色的"
    }
]


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


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


if __name__ == "__main__":
    # base64_image = encode_image("test.png")
    client = OpenAI(
            # 百炼API
            api_key="sk-42164feac5b64e79a08cf24b3363b342",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = bailian_client.chat.completions.create(
            model="qwen2-vl-7b-instruct",
            messages=messages,
            stream=True
    )
    print("流式输出内容为：")
    for chunk in completion:
        print(chunk.model_dump_json())
    messages = remove_request_pic(messages)

    completion = client.chat.completions.create(
            model="qwen2-vl-7b-instruct",
            messages=messages,
            stream=True
    )
    print("流式输出内容为：")
    for chunk in completion:
        print(chunk.model_dump_json())
