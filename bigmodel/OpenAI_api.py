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


if __name__ == "__main__":
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
