import base64

import cv2


def get_image(filepath):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("无法打开摄像头")
    else:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("未能捕获图像")
                break
            cv2.imwrite(filepath, frame)
            print("照片已保存为", filepath)
            break
        cap.release()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


if __name__ == '__main__':
    get_image("./test.jpg")
