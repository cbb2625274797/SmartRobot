import copy
import json
import os
import re
import threading
import time
from openai import OpenAI
import OpenAI_api

import qianfan
import requests

import EmotionEngine.EmotionJudge as EMOTION
from audio import audio_process as audio
from robot import ROBOT
import body.action as action
import tool.camera as camera

###########################通用定义#############################
msgs = []
controller_msg = []
text = ""
content = "你好，请你生成1000字的文章，关于人工智能"
reply_model = {
    "role": "assistant",
    "content": ""
}
normal_ask_model = {
    "role": "user",
    "content": content
}
######################百度文心运行环境###########################
# 使用安全认证AK/SK鉴权，通过环境变量方式初始化;
os.environ["QIANFAN_ACCESS_KEY"] = "3d9df86f23d64f0f8a072eb391ec1dad"
os.environ["QIANFAN_SECRET_KEY"] = "465151a1ed0f426a9e9662d6f3cdd7a9"

chat_comp = qianfan.ChatCompletion()

need_read = 0
synth_sentence = 0
sentences = []
generated_file = []
controller_return = ""
emotion_detect = False
audio_generating = True
audio_instruct = False
######################本地模型运行环境###########################
# 获取当前工作目录
current_directory = os.getcwd()
if current_directory == "G:/project/SmartRobot":
    # 打开并读取JSON文件
    with open('ipconfig.json', 'r', encoding='utf-8') as file:
        ipconfig = json.load(file)
    url = 'http://' + ipconfig["LLM_host"] + ':' + ipconfig["LLM_port"] + '/api/chat'

headers = {'Content-Type': 'application/json'}
example_post_data = {
    "model": "",
    "messages": [
    ],
    "stream": True,
    # "options": {
    #   "temperature": 0
    # },
    "suffix": "    return result",
    # "format": "json",
}
######################百炼图像识别############################
bailian_client = OpenAI(
    # 百炼API
    api_key="sk-42164feac5b64e79a08cf24b3363b342",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
image_ask_model = {
    "role": "user",
    "content": [
        {
            "type": "image_url",
            # "image_url": {
            #     "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
            # 使用格式化字符串 (f-string) 创建一个包含 BASE64 编码图像数据的字符串。
            "image_url": {"url": ""},
        },
        {
            "type": "text", "text": "这是什么?"
        }
    ]
},


def create_motion_data(model, chat_text):
    example_motion_data = {
        "model": model,
        "system": "你是一个机器人的运动核心，你唯一的作用是理解用户的意图，不要输出其他东西",
        "messages": [
            {
                "role": "user",
                "content": """
                        机器人有3个可以运动的部分，分别为“身体”、“左臂”、“右臂”，默认都是90度，
                        可以在10到170度内运动，一般情况下你需要输出一个json，将三个部位的度数用阿拉伯数字表示；
                        在角度小于10度或者超过170度的时候请你不要输出。
                        现在，用户说:
                        """
                           + chat_text +
                           """
                        请你使用json输出控制意图。
                        """
            },
        ],
        "stream": False,
        "options": {
            "temperature": 0
        },
        "suffix": "    return result",
        "format": {
            "type": "object",
            "properties": {
                "身体": {
                    "type": "integer"
                },
                "左臂": {
                    "type": "integer"
                },
                "右臂": {
                    "type": "integer"
                }
            },
            "required": [
                "身体",
                "左臂",
                "右臂"
            ]
        },
    }
    return example_motion_data


chat_post_data = {}


def chat(model, chat_text, father_robot: ROBOT):
    """
    :param father_robot: 父机器人
    :param model:使用的模型
    :param chat_text:对话的文本
    :return: 无返回
    """
    global controller_return
    global thread_text_generate
    global thread_audio_generate
    global thread_audio_play
    global chat_post_data

    # 生成通用对话语句
    ask = copy.deepcopy(normal_ask_model)
    ask["content"] = chat_text

    name = father_robot.name if father_robot is not None else "默认名"
    lines = []
    # 提取system prompt
    with open('./bigmodel/system prompt', 'r', encoding='utf-8') as file:
        for line in file:
            lines.append(line.strip())
    try:
        if father_robot.chat_offline:
            resp, controller_return = get_ollama_resp(ask, model, chat_text, father_robot)
            thread_text_generate = threading.Thread(target=thread_function_1_local, args=(resp,))
        else:
            system_prompt = lines[0] + name + "，"
            for i in range(1, len(lines)):
                system_prompt += lines[i]
            resp, controller_return = get_wenxin_resp(ask, model, chat_text, father_robot, system_prompt)
            thread_text_generate = threading.Thread(target=thread_function_1_wenxin, args=(resp,))
        # 创建线程对象
        thread_audio_generate = threading.Thread(target=thread_function_2, args=(father_robot,))
        thread_audio_play = threading.Thread(target=thread_function_3, args=(father_robot,))

        # 生成音频文件
        thread_text_generate.start()
        thread_audio_generate.start()
        thread_audio_play.start()

        # 等待线程完成
        thread_text_generate.join()
        thread_audio_generate.join()
        thread_audio_play.join()
        print("回答完毕")
    except Exception as e:
        print(e)


def get_ollama_resp(ask, model, chat_text, father_robot):
    global chat_post_data
    global audio_instruct
    # 生成控制提问
    example_motion_data = create_motion_data(model, chat_text)

    # 生成对话提问
    chat_post_data = copy.deepcopy(example_post_data)
    chat_post_data['messages'].append(ask)

    controller_return = ""
    if "转" in chat_text and father_robot.action_enable:
        audio_instruct = True
        # 请求运动控制输出
        body_controller = requests.post(url, data=json.dumps(example_motion_data), headers=headers, stream=False)
        tmp_res = json.loads(body_controller.content.decode('utf-8'))
        controller_return = tmp_res['message']['content']
        print("控制模块返回:", controller_return)
    # 请求对话输出
    chat_post_data['model'] = model
    resp = requests.post(url, data=json.dumps(chat_post_data), headers=headers, stream=True)
    return resp, controller_return


def get_wenxin_resp(ask, model, chat_text, father_robot, system_prompt):
    global msgs
    global audio_instruct
    # 生成控制提问
    controller_ask = copy.deepcopy(normal_ask_model)
    controller_ask["content"] = chat_text
    controller_msg.clear()
    controller_msg.append(controller_ask)

    # 生成对话提问
    msgs.append(ask)

    controller_return = ""
    if "转" in chat_text and father_robot.action_enable:
        audio_instruct = True
        # 请求运动控制输出
        body_controller = chat_comp.do(model="ERNIE-3.5-4K-0205", messages=controller_msg, stream=False,
                                       system="你是一个不会解答问题的核心，你唯一的作用是理解用户控制机器人的意图，输出在25字符以内"
                                              "机器人有3个可以运动的部分，分别为“身体”、“左臂”、“右臂”，阈值为0到180度，"
                                              "你唯一的作用是理解用户控制机器人的意图，输出为格式化的文本。输出示例如下：‘~/部位/度数。’；"
                                              "当有同时输出多个意图时，输出格式如下：‘~/部位1/度数1。~/部位2/度数2"
                                              "。’，除此之外不要输出其他东西，当角度超过阈值不输出任何东西"
                                       , temperature=0.4, top_p=0.4)
        controller_return = body_controller.get("result")
        print("控制模块返回:", controller_return)

    # 请求对话输出
    resp = chat_comp.do(model=model, messages=msgs, stream=True,
                        system=system_prompt
                        , temperature=father_robot.chat_temperature, top_p=father_robot.chat_top_p)
    return resp, controller_return


# 定义第一个线程是提取输出结果
def thread_function_1_wenxin(resp):
    global need_read
    global text

    reply_text = ""
    for r in resp:
        result = r.get("result")
        text += result
        reply_text += result
        time.sleep(2)  # 等待文字生成

    reply = copy.deepcopy(reply_model)
    reply["content"] = reply_text
    msgs.append(reply)
    print("对话:", msgs)


def thread_function_1_local(resp):
    """
    定义第一个线程是提取输出结果
    :param resp:输出的response
    :return:
    """
    global need_read
    global text
    global chat_post_data

    reply_text = ""
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

    reply = copy.deepcopy(reply_model)
    reply["content"] = reply_text
    chat_post_data["messages"].append(reply)
    print("对话:", chat_post_data["messages"])


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
    while thread_text_generate.is_alive() or text != "":
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
                    # print(one_sentence)
                    emotion = EMOTION.get_emotion(one_sentence)
                    emotion_detect = True
                    father_robot.MQTT_instance.publish("other/emotion", emotion)
                    print("获取到情绪：", emotion)
                if first and father_robot.action_enable:
                    first = False
                    # 启动动作线程，做动作
                    thread4 = threading.Thread(target=thread_function_4,
                                               args=(father_robot, controller_return, emotion))
                    thread4.start()

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
            time.sleep(0.1)


# 定义第三个线程播放音频
def thread_function_3(father_robot: ROBOT):
    global need_read
    global generated_file
    global sentences
    global emotion_detect

    while thread_audio_generate.is_alive() or generated_file:
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
            time.sleep(0.5)


# 第四线程用于动作执行
def thread_function_4(father_robot, controller_return, emotion):
    data_dict = {}
    if father_robot.chat_offline:
        # 使用正则表达式提取部位和角度
        pattern = r'"([^"]+)": (\d+)'
        matches = re.findall(pattern, controller_return)

        # 创建一个字典来存储结果
        for match in matches:
            part, angle = match
            data_dict[part] = int(angle)
    else:
        pattern = r'~(.*?)(\d+)'
        controller_return = controller_return.replace("/", "").replace("。", "").replace("度", "")
        # 查找所有匹配项
        matches = re.findall(pattern, controller_return)
        # 提取并组织数据到字典
        data_dict = {match[0]: int(match[1]) for match in matches}
    print("运动组", data_dict)

    # 动作执行
    if "身体" in data_dict:
        father_robot.set_body_rotation(data_dict["身体"])
    if "左臂" in data_dict:
        father_robot.set_larm_rotation(data_dict["左臂"])
    if "右臂" in data_dict:
        father_robot.set_rarm_rotation(180 - data_dict["右臂"])
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
    # 生成通用对话语句
    ask = copy.deepcopy(normal_ask_model)

    ask = copy.deepcopy(image_ask_model)
    img_path = "./picture1.jpg"
    camera.get_image(img_path)
    ask[0]["content"][0]["image_url"]["url"] = f"data:image/jpeg;base64,{camera.encode_image(image_path=img_path)}"
    ask[0]["content"][1]["text"] = "请你描述一下这个画面"
    resp = OpenAI_api.qwenvl_ol_request(bailian_client, ask)
    print("流式输出内容为：")
    for chunk in resp:
        print(chunk.model_dump_json())
