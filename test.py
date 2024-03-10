import MQTT
import threading
import time


def thread_function_2():
    MQTT.client_init()


def thread_function_1():
    while True:
        print("thread2 is running")
        time.sleep(1)


thread2 = threading.Thread(target=thread_function_2)
thread1 = threading.Thread(target=thread_function_1)

thread1.start()
thread2.start()
