import copy
import json
import re
import threading
import time

import requests

import EmotionEngine.EmotionJudge as EMOTION
import body.action as action
from audio import audio_process as audio
from bigmodel import ollama_api as ollama
from config.ip_config import LLM_server
from robot import ROBOT

ask_request = copy.deepcopy(ollama.example_post_data)
controller_request = copy.deepcopy(ollama.example_post_data)


def chat(model, chat_text, father_robot: ROBOT):
    """
    :param father_robot: 父机器人
    :param model:使用的模型
    :param chat_text:对话的文本
    :return: 无返回
    """
    global controller_return
    global thread1
    global thread2
    global thread3
    global ask_request
    global controller_request
    # 生成对话提问
    ask_request = ollama.add_ask(ask_request, chat_text)
    ask_request = ollama.set_model(ask_request, model)
    print(ask_request)
    # 生成控制提问
    controller_request = ollama.clear_msg_content(controller_request)  # 清空对话内容
    controller_request = ollama.add_ask(controller_request, chat_text)
    controller_request = ollama.set_model(controller_request, model)
    print(controller_request)
    controller_return = ""

    name = father_robot.name if father_robot is not None else "默认名"
    lines = []
    # 提取system prompt
    from config.file_config import chat_system_prompt
    with open(chat_system_prompt, 'r', encoding='utf-8') as file:
        for line in file:
            lines.append(line.strip())
    system_prompt = lines[0] + name + "，"
    for i in range(1, len(lines)):
        system_prompt += lines[i]

    try:
        if "转" in chat_text:
            # 请求运动控制输出
            body_controller = requests.post(LLM_server, data=json.dumps(controller_request), stream=False)
            # system="你是一个不会解答问题的机器人核心，你唯一的作用是理解用户控制机器人的意图"
            #        "机器人有3个可以运动的部分，分别为“身体”、“左臂”、“右臂”，阈值为0到180度，"
            #        "你唯一的作用是理解用户控制机器人的意图，输出为格式化的文本。输出示例如下：‘~/部位/度数。’；"
            #        "当有同时输出多个意图时，输出格式如下：‘~/部位1/度数1。~/部位2/度数2"
            #        "。’，除此之外不要输出其他东西，当角度超过阈值不输出任何东西"
            tmp_resp = json.loads(body_controller.content.decode('utf-8'))
            controller_return = tmp_resp['message']['content']
            print(controller_return)

        # 请求对话输出
        resp = requests.post(LLM_server, data=json.dumps(ask_request), stream=True)
        # 创建线程对象
        thread1 = threading.Thread(target=thread_function_1, args=(resp,))
        thread2 = threading.Thread(target=thread_function_2, args=(father_robot,))
        thread3 = threading.Thread(target=thread_function_3, args=(father_robot,))

        # 生成音频文件
        thread1.start()
        thread2.start()
        thread3.start()

        # 等待线程完成
        thread1.join()
        thread2.join()
        thread3.join()
        print("回答完毕")
    except Exception as e:
        print(e)


def thread_function_1(resp):
    """
    定义第一个线程是提取输出结果
    :param resp:输出的response
    :return:
    """
    global need_read
    global text_generating
    global text
    global ask_request

    reply_text = ""
    text = ""
    if resp.status_code == 200:
        # 迭代响应内容
        for line in resp.iter_lines():
            # 跳过数据流中的空行
            if line:
                # 解码行数据
                decoded_line = line.decode('utf-8')
                # 解析JSON数据（如果返回的是JSON格式）
                try:
                    result = json.loads(decoded_line)

                    text += result['message']['content']  # 消耗性
                    reply_text += result['message']['content']  # 用于保存输出

                    # 处理chunk数据
                    # print(chunk['message']['content'], end='')  # 示例处理：打印每一块数据
                except json.JSONDecodeError:
                    print(f"非JSON格式的数据：{decoded_line}")
    else:
        print(f"Failed to get response, status code: {resp.status_code}")

    ask_request = ollama.add_reply(ask_request, reply_text)
    print(ask_request["messages"])


# 第二线程用于分段+生成
def thread_function_2(father_robot: ROBOT):
    global text
    global sentences
    global generated_file
    global emotion_detect
    global first
    sentences = []
    generated_file = []
    cnt_generate = 1
    first = True
    emotion = '开心'
    while thread1.is_alive() or text != "":
        if text != "":
            # 使用正则表达式匹配以句号、问号或感叹号结尾的句子
            sentence_pattern = r'(.+?)[。？！]'
            while re.search(sentence_pattern, text):
                match = re.search(sentence_pattern, text)
                print("匹配到句子：", match.group(1))
                # 提取第一句话
                one_sentence = match.group(1)
                # 获取第一句话的结束位置（包括句号、问号或感叹号）
                end_index = match.end()
                # 删除缓冲区内第一句话
                text = text[end_index:]

                # 获取情绪
                emotion_detect = False
                if '-' in one_sentence[:5] and '/' in one_sentence[:5]:
                    print(one_sentence)
                    emotion = EMOTION.get_emotion(one_sentence)
                    emotion_detect = True
                    father_robot.MQTT_instance.publish("other/emotion", emotion)
                    print("获取到情绪：", emotion)
                if first:
                    first = False
                    # 启动动作线程，做动作
                    thread4 = threading.Thread(target=thread_function_4,
                                               args=(father_robot, controller_return, emotion))
                    thread4.start()
                try:
                    father_robot.MQTT_instance.publish("other/emotion", emotion)
                except Exception as e:
                    print('错误:', e)
                # 定义正则表达式模式
                pattern1 = r"-\s*/\s*(开心|害怕|生气|失落|好奇|戏谑)\s*"
                # 使用正则表达式替换
                one_sentence = re.sub(pattern1, '', one_sentence)
                one_sentence = one_sentence.strip()

                if one_sentence != '':
                    sentences.append(one_sentence)
                    filename = f"./audio/audio{cnt_generate}.mp3"
                    try:
                        # 生成语音
                        audio.SOVITS_TTS(father_robot.sound_character, emotion, sentences[cnt_generate - 1], filename)
                        generated_file.append(filename)
                        cnt_generate += 1
                    except Exception as e:
                        # 错误处理逻辑，如打印错误信息、记录日志等
                        print(e)
        else:
            time.sleep(0.2)


# 定义第三个线程播放音频
def thread_function_3(father_robot: ROBOT):
    global need_read
    global generated_file
    global sentences
    global emotion_detect
    global first

    while thread2.is_alive() or generated_file:
        if generated_file:
            # 播放所有生成的音频文件
            filename = generated_file[0]
            cnt_read = int(re.search(r'/audio/audio(\d+)', filename).group(1))  # 提取第几句
            # MQTT发送讲话
            try:
                father_robot.MQTT_instance.publish(topic="cbb/TALK", message=sentences[cnt_read - 1], qos=2)
                audio.play(filename, father_robot.volume)
                generated_file.pop(0)
            except Exception as e:
                print(e)
        else:
            time.sleep(0.2)
    first = True


# 第四线程用于动作执行
def thread_function_4(father_robot, controller_return, emotion):
    data_dict = {}
    pattern = r'~(.*?)(\d+)'
    controller_return = controller_return.replace("/", "").replace("。", "").replace("度", "")
    print(controller_return)
    try:
        # 查找所有匹配项
        matches = re.findall(pattern, controller_return)
        # 提取并组织数据到字典
        data_dict = {match[0]: int(match[1]) for match in matches}
        print(data_dict)
        if "身体" in data_dict:
            father_robot.set_body_rotation(data_dict["身体"])
        if "左臂" in data_dict:
            father_robot.set_larm_rotation(data_dict["左臂"])
        if "右臂" in data_dict:
            father_robot.set_rarm_rotation(180 - data_dict["右臂"])
    finally:
        if data_dict == {}:
            if emotion == '开心':
                action.happy_action(father_robot)
            elif emotion == '害怕':
                action.scare_action(father_robot)
            elif emotion == '生气':
                action.angry_action(father_robot)
            elif emotion == '失落':
                action.upset_action(father_robot)
            elif emotion == '好奇':
                action.curious_action(father_robot)
            elif emotion == '戏谑':
                action.laugh_action(father_robot)


if __name__ == '__main__':
    while True:
        question = input("请输入：\n")
        chat('qwen2.5_3b', question, None)
