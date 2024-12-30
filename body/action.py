import time

import robot
import threading


# def happy_action(father_robot: robot.ROBOT):
#
#     father_robot.set_body_rotation(90)
#     father_robot.set_foot_rotation(90)
#     father_robot.set_larm_rotation(90)
#     father_robot.set_rarm_rotation(90)
#
#     father_robot.set_foot_rotation(70, 2)
#     father_robot.set_larm_rotation(50, 3)
#     father_robot.set_rarm_rotation(50, 3)
#     father_robot.set_foot_rotation(110, 2)
#     father_robot.set_larm_rotation(130, 3)
#     father_robot.set_rarm_rotation(130, 3)
#
#     father_robot.set_body_rotation(90)
#     father_robot.set_larm_rotation(90)
#     father_robot.set_foot_rotation(90)
#     father_robot.set_rarm_rotation(90)


def happy_action(father_robot: robot.ROBOT):
    def thread_function_1():
        father_robot.set_body_rotation(90)
        father_robot.set_body_rotation(90)

    def thread_function_2():
        father_robot.set_foot_rotation(90)
        # father_robot.set_foot_rotation(70, 1.5)
        # time.sleep(1)
        # father_robot.set_foot_rotation(110, 1.5)
        father_robot.set_foot_rotation(90)

    def thread_function_3():
        father_robot.set_larm_rotation(90)
        father_robot.set_larm_rotation(50, 2)
        time.sleep(1)
        father_robot.set_larm_rotation(130, 2)
        father_robot.set_larm_rotation(90)

    def thread_function_4():
        father_robot.set_rarm_rotation(90)
        father_robot.set_rarm_rotation(130, 2)
        time.sleep(1)
        father_robot.set_rarm_rotation(50, 2)
        father_robot.set_rarm_rotation(90)

    thread1 = threading.Thread(target=thread_function_1, args=())
    thread2 = threading.Thread(target=thread_function_2, args=())
    thread3 = threading.Thread(target=thread_function_3, args=())
    thread4 = threading.Thread(target=thread_function_4, args=())

    thread1.start()
    time.sleep(0.1)
    thread2.start()
    time.sleep(0.1)
    thread3.start()
    time.sleep(0.1)
    thread4.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()


def scare_action(father_robot: robot.ROBOT):
    def thread_function_1():
        father_robot.set_body_rotation(90)
        father_robot.set_body_rotation(90)

    def thread_function_2():
        father_robot.set_foot_rotation(90)
        father_robot.set_foot_rotation(85, 2)
        father_robot.set_foot_rotation(95, 2)
        father_robot.set_foot_rotation(85, 2)
        father_robot.set_foot_rotation(95, 2)
        father_robot.set_foot_rotation(90)

    def thread_function_3():
        father_robot.set_larm_rotation(90)
        father_robot.set_larm_rotation(85, 2)
        father_robot.set_larm_rotation(95, 2)
        father_robot.set_larm_rotation(85, 2)
        father_robot.set_larm_rotation(95, 2)
        father_robot.set_larm_rotation(90)

    def thread_function_4():
        father_robot.set_rarm_rotation(90)
        father_robot.set_rarm_rotation(85, 2)
        father_robot.set_rarm_rotation(95, 2)
        father_robot.set_rarm_rotation(85, 2)
        father_robot.set_rarm_rotation(95, 2)
        father_robot.set_rarm_rotation(90)

    thread1 = threading.Thread(target=thread_function_1, args=())
    thread2 = threading.Thread(target=thread_function_2, args=())
    thread3 = threading.Thread(target=thread_function_3, args=())
    thread4 = threading.Thread(target=thread_function_4, args=())

    thread1.start()
    time.sleep(0.1)
    thread2.start()
    time.sleep(0.1)
    thread3.start()
    time.sleep(0.1)
    thread4.start()


    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()


def angry_action(father_robot: robot.ROBOT):
    def thread_function_1():
        father_robot.set_body_rotation(90)
        father_robot.set_body_rotation(90)

    def thread_function_2():
        father_robot.set_foot_rotation(90)
        father_robot.set_foot_rotation(90)

    def thread_function_3():
        father_robot.set_larm_rotation(90)
        father_robot.set_larm_rotation(135, 3)
        time.sleep(1)
        father_robot.set_larm_rotation(60, 3)
        father_robot.set_larm_rotation(90)

    def thread_function_4():
        father_robot.set_rarm_rotation(90)
        father_robot.set_rarm_rotation(135, 3)
        time.sleep(1)
        father_robot.set_rarm_rotation(60, 3)
        father_robot.set_rarm_rotation(90)

    thread1 = threading.Thread(target=thread_function_1, args=())
    thread2 = threading.Thread(target=thread_function_2, args=())
    thread3 = threading.Thread(target=thread_function_3, args=())
    thread4 = threading.Thread(target=thread_function_4, args=())

    thread1.start()
    time.sleep(0.1)
    thread2.start()
    time.sleep(0.1)
    thread3.start()
    time.sleep(0.1)
    thread4.start()


    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()


def upset_action(father_robot: robot.ROBOT):
    def thread_function_1():
        father_robot.set_body_rotation(90)
        # father_robot.set_body_rotation(80, 0.5)
        # time.sleep(5)
        father_robot.set_body_rotation(90)

    def thread_function_2():
        father_robot.set_foot_rotation(90)
        # father_robot.set_foot_rotation(60, 0.75)
        # father_robot.set_foot_rotation(120, 0.75)
        # time.sleep(5)
        father_robot.set_foot_rotation(90)

    def thread_function_3():
        father_robot.set_larm_rotation(90)
        father_robot.set_larm_rotation(75, 0.75)
        father_robot.set_larm_rotation(105, 0.75)
        time.sleep(5)
        father_robot.set_larm_rotation(90)

    def thread_function_4():
        father_robot.set_rarm_rotation(90)
        father_robot.set_rarm_rotation(75, 0.75)
        father_robot.set_rarm_rotation(105, 0.75)
        time.sleep(5)
        father_robot.set_rarm_rotation(90)

    thread1 = threading.Thread(target=thread_function_1, args=())
    thread2 = threading.Thread(target=thread_function_2, args=())
    thread3 = threading.Thread(target=thread_function_3, args=())
    thread4 = threading.Thread(target=thread_function_4, args=())

    thread1.start()
    time.sleep(0.1)
    thread2.start()
    time.sleep(0.1)
    thread3.start()
    time.sleep(0.1)
    thread4.start()


    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()


def laugh_action(father_robot: robot.ROBOT):
    def thread_function_1():
        father_robot.set_body_rotation(90)
        father_robot.set_body_rotation(85, 1)
        father_robot.set_body_rotation(95, 1)
        father_robot.set_body_rotation(90)

    def thread_function_2():
        father_robot.set_foot_rotation(90)
        father_robot.set_foot_rotation(95, 0.5)
        father_robot.set_foot_rotation(90)

    def thread_function_3():
        father_robot.set_larm_rotation(90)
        father_robot.set_larm_rotation(130, 3)
        time.sleep(1)
        father_robot.set_larm_rotation(60, 1)
        father_robot.set_larm_rotation(90)

    def thread_function_4():
        father_robot.set_rarm_rotation(90)
        father_robot.set_rarm_rotation(130, 1)
        time.sleep(1)
        father_robot.set_rarm_rotation(60, 3)
        father_robot.set_rarm_rotation(90)

    thread1 = threading.Thread(target=thread_function_1, args=())
    thread2 = threading.Thread(target=thread_function_2, args=())
    thread3 = threading.Thread(target=thread_function_3, args=())
    thread4 = threading.Thread(target=thread_function_4, args=())

    thread1.start()
    time.sleep(0.1)
    thread2.start()
    time.sleep(0.1)
    thread3.start()
    time.sleep(0.1)
    thread4.start()


    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()


def curious_action(father_robot: robot.ROBOT):
    def thread_function_1():
        father_robot.set_body_rotation(90)
        father_robot.set_body_rotation(90)

    def thread_function_2():
        father_robot.set_foot_rotation(90)
        father_robot.set_foot_rotation(85)
        time.sleep(1)
        father_robot.set_foot_rotation(95)
        father_robot.set_foot_rotation(90)

    def thread_function_3():
        father_robot.set_larm_rotation(90)
        father_robot.set_larm_rotation(120)
        time.sleep(1.2)
        father_robot.set_larm_rotation(60)
        father_robot.set_larm_rotation(90)

    def thread_function_4():
        father_robot.set_rarm_rotation(90)
        father_robot.set_rarm_rotation(60)
        time.sleep(1.3)
        father_robot.set_rarm_rotation(120)
        father_robot.set_rarm_rotation(90)

    thread1 = threading.Thread(target=thread_function_1, args=())
    thread2 = threading.Thread(target=thread_function_2, args=())
    thread3 = threading.Thread(target=thread_function_3, args=())
    thread4 = threading.Thread(target=thread_function_4, args=())

    thread1.start()
    time.sleep(0.1)
    thread2.start()
    time.sleep(0.1)
    thread3.start()
    time.sleep(0.1)
    thread4.start()


    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
