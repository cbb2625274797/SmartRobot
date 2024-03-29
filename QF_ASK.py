import os
import threading
import qianfan
import audio_process as audio
import time
import re
import copy

# 使用安全认证AK/SK鉴权，通过环境变量方式初始化;
os.environ["QIANFAN_ACCESS_KEY"] = "3d9df86f23d64f0f8a072eb391ec1dad"
os.environ["QIANFAN_SECRET_KEY"] = "465151a1ed0f426a9e9662d6f3cdd7a9"

chat_comp = qianfan.ChatCompletion()

need_read = 0
synthesising = 0
generating = False
text = ""
reply_model = {
    "role": "assistant",
    "content": "content"
}
ask_model = {
    "role": "user",
    "content": "content"
}
msgs = []


def chat(model, chat_text):
    global need_read

    ask = copy.deepcopy(ask_model)
    ask["content"] = chat_text
    msgs.append(ask)
    resp = chat_comp.do(model=model, messages=msgs, stream=True)

    # 创建线程对象
    thread1 = threading.Thread(target=thread_function_1, args=(resp,))
    thread2 = threading.Thread(target=thread_function_2)
    thread3 = threading.Thread(target=thread_function_3)
    # thread4 = threading.Thread(target=thread_function_4)

    # 生成音频文件
    need_read = 0
    thread1.start()
    thread2.start()
    thread3.start()
    # thread4.start()

    # 等待线程完成
    thread1.join()
    thread2.join()
    thread3.join()
    # thread4.join()


# 定义第一个线程是提取输出结果
def thread_function_1(resp):
    global need_read
    global generating
    global text
    generating = True  # 用于退出第二线程的循环

    reply_text = ""
    for r in resp:
        result = r.get("result")
        text += result
        reply_text += result
        time.sleep(2)  # 等待文字生成

    reply = copy.deepcopy(reply_model)
    reply["content"] = reply_text
    msgs.append(reply)
    print(msgs)

    if synthesising == 1:
        generating = False


# 第三线程用于分段+生成
def thread_function_3():
    global need_read
    global text
    global synthesising
    cnt = 0
    synthesising = 0
    while generating:
        # 使用正则表达式匹配以句号、问号或感叹号结尾的句子
        sentence_pattern = r'(.+?)[。!?？！ *]'
        while re.search(sentence_pattern, text):
            match = re.search(sentence_pattern, text)
            # 提取第一句话
            first_sentence = match.group(1)
            print(first_sentence)
            # 获取第一句话的结束位置（包括句号、问号或感叹号）
            end_index = match.end()
            # 删除第一句话，即截取第一个句号之后的部分
            text = text[end_index:]

            cnt += 1
            filename = "./audio/" + "audio" + str(cnt) + ".mp3"
            synthesising = 1
            audio.SOVITS_TTS("paimon", 0, first_sentence, filename)
            synthesising = 0
            need_read += 1


''''
# 第四线程用于情感分析
def thread_function_4():
    print("analysing")
    time.sleep(3)
'''


# 定义第二个线程播放音频
def thread_function_2():
    global need_read
    global generating
    time.sleep(5)  # 等待生成
    while True:
        if generating:  # 触发进入阅读
            # 播放所有生成的音频文件
            cnt = 1
            while True:
                filename = "./audio/" + "audio" + str(cnt) + ".mp3"
                if os.path.exists(filename) and need_read:
                    audio.play(filename)
                    need_read -= 1
                    # print("播放：" + filename)
                    cnt += 1
                elif need_read == 0 and generating is False and synthesising == 0:
                    print("回答完毕")
                    break
                elif need_read == 0 and generating is False and synthesising == 1:
                    time.sleep(0.1)
                    # print("等待语音生成...")
                else:
                    time.sleep(0.1)
                    # print("没有完成，等待")
        break


if __name__ == '__main__':
    chat("Yi-34B-Chat", "你可以介绍一下华盛顿的地理位置吗")
