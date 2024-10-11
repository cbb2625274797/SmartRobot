import copy

content = "你好，请你生成1000字的文章，关于人工智能"
LLM_name = 'qwen2.5_32b_q2_k'

ask_model = {
    "role": "user",
    "content": content
}
reply_model = {
    "role": "assistant",
    "content": ""
}

example_post_data = {
    "model": LLM_name,
    "messages": [

    ],
    "stream": True,
    "suffix": "    return result",
    "format": "json",
}


def add_ask(msg, chat_text):
    ask = copy.deepcopy(ask_model)
    ask["content"] = chat_text
    msg['messages'].append(ask)
    return msg


def set_model(msg, mdoel_name):
    msg['model'] = mdoel_name
    return msg


def clear_msg_content(msg):
    msg['messages'] = []
    return msg


def add_reply(msg, reply_text):
    reply = copy.deepcopy(reply_model)
    reply["content"] = reply_text
    msg['messages'].append(reply)
    return msg
