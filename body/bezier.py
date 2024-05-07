import matplotlib.pyplot as plt
import numpy as np


def angle_bezier_clamped(start_angle, end_angle, control1, control2, num_points: int):
    """
    生成从起始角度到终止角度的贝塞尔曲线角度数组，角度范围限制在0到180度之间。

    :param start_angle: 起始角度
    :param end_angle: 终止角度
    :param control1: 第一个控制角度
    :param control2: 第二个控制角度
    :param num_points: 生成的点数
    :return: 贝塞尔曲线上的角度数组
    """
    # 确保角度在0到180度之间
    start_angle = np.clip(start_angle, 0, 180)
    end_angle = np.clip(end_angle, 0, 180)
    control1 = np.clip(control1, 0, 180)
    control2 = np.clip(control2, 0, 180)

    # 生成时间点
    t = np.linspace(0, 1, num_points)

    # 计算三次贝塞尔曲线上的角度
    angles = (1 - t) ** 3 * start_angle + 3 * (1 - t) ** 2 * t * control1 + 3 * (
            1 - t) * t ** 2 * control2 + t ** 3 * end_angle

    # 将角度调整到0到180度之间
    angles = np.clip(angles, 0, 180)

    return angles


if __name__ == '__main__':
    # 定义起始角度、终止角度和两个控制角度
    start_angle = 30
    end_angle = 150
    control1 = 20
    control2 = 160
    # 生成贝塞尔曲线的角度
    bezier_angles = angle_bezier_clamped(start_angle, end_angle, control1, control2,100)
    print(bezier_angles)
    # 生成对应的时间点
    time_points = np.linspace(0, 1, len(bezier_angles))

    # 绘制角度随时间变化的曲线
    plt.plot(time_points, bezier_angles)
    plt.xlabel('Time')
    plt.ylabel('Angle (degrees)')
    plt.title('Angle Variation over Time using Bezier Curve')
    plt.grid(True)
    plt.show()
