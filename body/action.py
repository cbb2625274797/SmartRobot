import time

import robot
import threading

import json


def get_actions(file_name="happy"):
    if __name__ == '__main__':
        file_path = f"./action_data/{file_name}.json"
    else:
        file_path = f"./body/action_data/{file_name}.json"
    # 从文件读取
    with open(file_path, 'r') as f:
        robot_actions = json.load(f)

    # 打印解析后的数据
    print(robot_actions)
    return robot_actions


def perform_action(robot_ins, action_list, part):
    print(f"部件名称: {part}")
    if part not in action_list:
        print(f"无效的部件名称: {part}")
        return
    else:
        for action in action_list[part]:
            if 'target_angle' in action:
                if part == "body":
                    robot_ins.set_body_rotation(action['target_angle'], action['speed'])
                elif part == "foot":
                    robot_ins.set_foot_rotation(action['target_angle'], action['speed'])
                elif part == "larm":
                    robot_ins.set_larm_rotation(action['target_angle'], action['speed'])
                elif part == "rarm":
                    robot_ins.set_rarm_rotation(action['target_angle'], action['speed'])
                # print(f"  动作: 转动到角度 {action['target_angle']}, 速度 {action['speed']}")
            elif 'sleep' in action:
                time.sleep(action['sleep'])
                print(f"  动作: 休眠 {action['sleep']} 秒")


def emotion_express(father_robot: robot.ROBOT, emotion):
    action_list = get_actions(emotion)

    thread1 = threading.Thread(target=perform_action, args=(father_robot, action_list, "body"))
    thread2 = threading.Thread(target=perform_action, args=(father_robot, action_list, "foot"))
    thread3 = threading.Thread(target=perform_action, args=(father_robot, action_list, "larm"))
    thread4 = threading.Thread(target=perform_action, args=(father_robot, action_list, "rarm"))

    thread1.start()
    thread2.start()
    thread4.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()


if __name__ == '__main__':
    get_actions()
