import os
import threading
import qianfan
import audio_process as audio
import time
import re

need_read = 0
generating = False
text = ""

# 使用安全认证AK/SK鉴权，通过环境变量方式初始化；替换下列示例中参数，安全认证Access Key替换your_iam_ak，Secret Key替换your_iam_sk
os.environ["QIANFAN_ACCESS_KEY"] = "3d9df86f23d64f0f8a072eb391ec1dad"
os.environ["QIANFAN_SECRET_KEY"] = "465151a1ed0f426a9e9662d6f3cdd7a9"

chat_comp = qianfan.ChatCompletion()


def chat(model, chat_text):
    global need_read
    resp = chat_comp.do(model=model, messages=[{
        "role": "user",
        "content": chat_text
    }], stream=True)
    # 创建线程对象
    thread1 = threading.Thread(target=thread_function_1, args=(resp,))
    thread2 = threading.Thread(target=thread_function_2)
    thread3 = threading.Thread(target=thread_function_3)

    # 生成音频文件
    need_read = 0
    thread1.start()
    thread2.start()
    thread3.start()

    # 等待线程完成
    thread1.join()
    thread2.join()
    thread3.join()


# 定义第一个线程是和大语言模型交互
def thread_function_1(resp):
    global need_read
    global generating
    global text
    generating = True  # 用于退出第二线程的循环

    for r in resp:
        result = r.get("result")
        text += result
        time.sleep(5)  # 等待文字生成

    time.sleep(3)  # 等待第三线程处理完文字
    generating = False


# 第三线程用于分段+生成
def thread_function_3():
    global need_read
    global text
    cnt = 0
    while generating:
        # 使用正则表达式匹配以句号、问号或感叹号结尾的句子
        sentence_pattern = r'(.+?)[。!?？！]'
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
            audio.SOVITS_TTS(first_sentence, filename)
            need_read += 1


# 定义第二个线程播放音频
def thread_function_2():
    global need_read
    global generating
    time.sleep(5)  # 等待生成
    while True:
        if generating:  # 触发进入阅读
            # 播放所有生成的音频文件
            cnt = 0
            while True:
                cnt += 1
                filename = "./audio/" + "audio" + str(cnt) + ".mp3"
                if os.path.exists(filename) and need_read:
                    audio.play(filename)
                    need_read -= 1
                elif need_read == 0 and generating is False:
                    print("输出完毕")
                    break
                else:
                    cnt -= 1
        break


if __name__ == '__main__':
    chat("Yi-34B-Chat", "请你自我介绍")
