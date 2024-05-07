import os
import threading
import qianfan
from audio import audio_process as audio
import time
import re
import copy
import EmotionEngine.EmotionJudge as EMOTION
from robot import ROBOT

# 使用安全认证AK/SK鉴权，通过环境变量方式初始化;
os.environ["QIANFAN_ACCESS_KEY"] = "3d9df86f23d64f0f8a072eb391ec1dad"
os.environ["QIANFAN_SECRET_KEY"] = "465151a1ed0f426a9e9662d6f3cdd7a9"

chat_comp = qianfan.ChatCompletion()

need_read = 0
synthesising = 0
sentences = []
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
controller_msg = []


def chat(model, chat_text, father_robot: ROBOT):
    """
    :param father_robot: 父机器人
    :param model:使用的模型
    :param chat_text:对话的文本
    :return: 无返回
    """
    global need_read

    # 生成对话提问
    ask = copy.deepcopy(ask_model)
    ask["content"] = chat_text
    msgs.append(ask)
    # 生成控制提问
    controller_ask = copy.deepcopy(ask_model)
    controller_ask["content"] = chat_text
    controller_msg.clear()
    controller_msg.append(controller_ask)

    name = father_robot.name
    lines = []
    with open('./server/system prompt', 'r', encoding='utf-8') as file:
        for line in file:
            lines.append(line.strip())
    system_prompt = lines[0] + name + "，"
    for i in range(1, len(lines)):
        system_prompt += lines[i]
    try:
        # 请求运动控制输出
        body_controller = chat_comp.do(model="ERNIE-Lite-8K", messages=controller_msg, stream=False,
                                       system="你是一个不会解答问题的核心，你唯一的作用是理解用户控制机器人的意图，输出在25字符以内"
                                              "机器人有3个可以运动的部分，分别为“身体”、“左臂”、“右臂”，阈值为0到180度，"
                                              "你唯一的作用是理解用户控制机器人的意图，输出为格式化的文本。输出示例如下：‘~/部位/度数。’；"
                                              "当有同时输出多个意图时，输出格式如下：‘~/部位1/度数1。~/部位2/度数2。’，除此之外不要输出其他东西，当角度超过阈值不输出任何东西"
                                       , temperature=0.4, top_p=0.4)
        controller_return: str = body_controller.get("result")
        print(controller_return)
        # 请求其他输出
        resp = chat_comp.do(model=model, messages=msgs, stream=True,
                            system=system_prompt
                            , temperature=father_robot.chat_temperature, top_p=father_robot.chat_top_p)
        # 创建线程对象
        thread1 = threading.Thread(target=thread_function_1, args=(resp,))
        thread2 = threading.Thread(target=thread_function_2, args=(father_robot,))
        thread3 = threading.Thread(target=thread_function_3, args=(father_robot,))
        thread4 = threading.Thread(target=thread_function_4, args=(father_robot, controller_return,))

        # 生成音频文件
        need_read = 0
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()

        # 等待线程完成
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
    except Exception as e:
        print(e)


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

    while synthesising:
        time.sleep(0.5)
    generating = False


# 第三线程用于分段+生成
def thread_function_3(father_robot: ROBOT):
    global need_read
    global text
    global synthesising
    global sentences
    global emotion_detect
    sentences = [""]
    cnt_generate = 0
    synthesising = 0
    emotion = '开心'
    while generating:
        # 使用正则表达式匹配以句号、问号或感叹号结尾的句子
        sentence_pattern = r'(.+?)[。？！]'
        while re.search(sentence_pattern, text):
            match = re.search(sentence_pattern, text)
            # 提取第一句话
            process_sentence = match.group(1)
            # 获取第一句话的结束位置（包括句号、问号或感叹号）
            end_index = match.end()
            # 删除第一句话，即截取第一个句号之后的部分
            text = text[end_index:]

            synthesising = 1
            emotion_detect = False
            if '-' in process_sentence[:5] and '/' in process_sentence[:5]:
                emotion = EMOTION.get_emotion(process_sentence)
                emotion_detect = True
                print("获取到情绪：", emotion)
            else:
                need_read += 1
            # 定义正则表达式模式
            pattern1 = r"-\s*/\s*(开心|害怕|生气|失落|好奇|戏谑)\s*"
            # 使用正则表达式替换
            process_sentence = re.sub(pattern1, '', process_sentence)
            process_sentence = process_sentence.strip()

            if process_sentence != '':
                try:
                    sentences.append(process_sentence)
                    cnt_generate += 1
                    filename = f"./audio/audio{cnt_generate}.mp3"
                    # 生成语音
                    audio.SOVITS_TTS(father_robot.sound_character, emotion, process_sentence, filename)
                except Exception as e:
                    # 错误处理逻辑，如打印错误信息、记录日志等
                    print(e)
            synthesising = 0


# 第四线程用于动作执行
def thread_function_4(father_robot, controller_return):
    pattern = r'~/(.*?)/(\d+)\。'
    try:
        # 查找所有匹配项
        matches = re.findall(pattern, controller_return)
        # 提取并组织数据到字典
        data_dict = {match[0]: int(match[1]) for match in matches}
        print(data_dict)
        if "身体" in data_dict:
            father_robot.set_foot_rotation(data_dict["身体"])
        if "左臂" in data_dict:
            father_robot.set_larm_rotation(data_dict["左臂"])
        if "右臂" in data_dict:
            father_robot.set_rarm_rotation(data_dict["右臂"])
    finally:
        pass


# 定义第二个线程播放音频
def thread_function_2(father_robot: ROBOT):
    global need_read
    global generating
    global sentences
    global emotion_detect
    time.sleep(5)  # 等待生成
    while True:
        if generating:  # 触发进入阅读
            # 播放所有生成的音频文件
            cnt_read = 1
            while True:
                filename = "./audio/" + "audio" + str(cnt_read) + ".mp3"
                # print(filename, os.path.exists(filename))
                if os.path.exists(filename) and need_read:
                    # MQTT发送讲话
                    try:
                        father_robot.MQTT_instance.publish(topic="cbb/TALK", message=sentences[cnt_read], qos=2)
                        audio.play(filename, father_robot.volume)
                    except Exception as e:
                        print(e)
                    need_read -= 1
                    # print("播放：" + filename)
                    cnt_read += 1
                elif need_read == 0 and generating is False and synthesising == 0:
                    print("回答完毕")
                    break
                elif need_read == 0 and generating is False and synthesising == 1:
                    time.sleep(0.2)
                    # print("等待语音生成...")
                else:
                    time.sleep(0.2)
                    # print("没有完成，等待")
        break


if __name__ == '__main__':
    while 1:
        question = input("请输入：\n")
        chat("ERNIE-Bot", chat_text=question)
        # chat("Yi-34B-Chat", chat_text=question)
