import copy
import os
import qianfan

# 使用安全认证AK/SK鉴权，通过环境变量方式初始化;
os.environ["QIANFAN_ACCESS_KEY"] = "3d9df86f23d64f0f8a072eb391ec1dad"
os.environ["QIANFAN_SECRET_KEY"] = "465151a1ed0f426a9e9662d6f3cdd7a9"

reply_model = {
    "role": "assistant",
    "content": "content"
}
ask_model = {
    "role": "user",
    "content": "content"
}


def chat(model, chat_text, round):
    chat_comp = qianfan.ChatCompletion()
    msgs = []

    # 生成对话提问
    ask = copy.deepcopy(ask_model)
    ask["content"] = chat_text
    msgs.append(ask)
    message = ""
    lines = []
    controller_msg = []
    # 提取system prompt
    with open('../bigmodel/system prompt', 'r', encoding='utf-8') as file:
        for line in file:
            lines.append(line.strip())
    system_prompt = lines[0] + "name" + "，"
    for i in range(1, len(lines)):
        system_prompt += lines[i]

    controller_ask = copy.deepcopy(ask_model)
    controller_ask["content"] = chat_text

    controller_msg.clear()
    controller_msg.append(controller_ask)

    body_controller = chat_comp.do(model=model, messages=controller_msg, stream=False,
                                   system="你是一个不会解答问题的核心，你唯一的作用是理解用户控制机器人的意图，输出在25字符以内"
                                          "机器人有3个可以运动的部分，分别为“身体”、“左臂”、“右臂”，阈值为0到180度，"
                                          "你唯一的作用是理解用户控制机器人的意图，输出为格式化的文本。输出示例如下：‘~/部位/度数。’；"
                                          "当有同时输出多个意图时，输出格式如下：‘~/部位1/度数1。~/部位2/度数2"
                                          "。’，除此之外不要输出其他东西，当角度超过阈值不输出任何东西"
                                   , temperature=0.4, top_p=0.4)
    controller_return = body_controller.get("result")
    print("机械控制输出轮次", round, "：", controller_return)

    # 请求其他输出
    # resp = chat_comp.do(model=model, messages=msgs, stream=False, system=system_prompt)
    # chat_return = resp.get("result")
    # print("对话输出轮次", round, "：", chat_return)


if __name__ == '__main__':
    for i in range(10):
        chat("Yi-34B-Chat", "你是一个不会解答问题的核心，你唯一的作用是理解用户控制机器人的意图，输出在25字符以内机器人有3个可以运动的部分，分别为“身体”、“左臂”、“右臂”，阈值为0到180"
                            "度，你唯一的作用是理解用户控制机器人的意图，输出为格式化的文本。输出示例如下：‘~/部位/度数。’；当有同时输出多个意图时，输出格式如下：‘~/部位1/度数1。~/部位2"
                            "/度数2。’，除此之外不要输出其他东西，当角度超过阈值不输出任何东西。现在，我说：身体旋转143度，你该怎么回答？", i)
