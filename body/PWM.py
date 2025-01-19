try:
    import wiringpi
except Exception as e:
    pass
import argparse
import time

import body.bezier as bezier

# import bezier
parser = argparse.ArgumentParser(description='i2c')
parser.add_argument("--device", type=str, default="/dev/i2c-2", help='specify the i2c node')
args = parser.parse_args()

i2caddr = 0x40
PCA9685_SUBADR1 = 0x2
PCA9685_SUBADR2 = 0x3
PCA9685_SUBADR3 = 0x4

PCA9685_MODE1 = 0x0
PCA9685_PRESCALE = 0xFE

LED0_ON_L = 0x6
LED0_ON_H = 0x7
LED0_OFF_L = 0x8
LED0_OFF_H = 0x9

ALLLED_ON_L = 0xFA
ALLLED_ON_H = 0xFB
ALLLED_OFF_L = 0xFC
ALLLED_OFF_H = 0xFD


def map_range(value):
    # 归一化原始值
    normalized = value / 180
    # 应用归一化值到目标范围
    mapped_value = 102.4 + normalized * 409.6

    return mapped_value


class PWM:
    def __init__(self):
        try:
            wiringpi.wiringPiSetup()
            self.fd = wiringpi.wiringPiI2CSetupInterface(args.device, i2caddr)
        except Exception as e:
            print(e)
        finally:
            self.reset()
            self.setPWMFreq(50)
            self.Mqtt_ins = None

    def write_byte(self, reg, byte):
        try:
            if wiringpi.wiringPiI2CWriteReg8(self.fd, reg, byte) < 0:
                print("Error write byte to device")
                return -1
        except Exception as e:
            print(e)
        return 0

    def read_byte(self, reg):
        try:
            byte = wiringpi.wiringPiI2CReadReg8(self.fd, reg)
            if byte < 0:
                print("Error read byte from device")
                return -1
            return byte
        except Exception as e:
            print(e)

    def reset(self):
        self.write_byte(PCA9685_MODE1, 0x0)

    def setPWMFreq(self, freq: float):
        # print("调整频率" + str(freq))
        freq *= 0.9
        # PCA9685的时钟频率是25MHz
        prescaleval = 25000000
        prescaleval /= 4096
        prescaleval /= freq
        prescaleval -= 1

        prescale = round(prescaleval)
        oldmode = self.read_byte(0)

        try:
            # 设置MODE1寄存器为睡眠模式
            newmode = (oldmode & 0x7F) | 0x10  # sleep
            self.write_byte(0, newmode)  # go to sleep
            self.write_byte(0XFE, prescale)  # set the prescaler
            # print(prescale)
            self.write_byte(0, oldmode)
            time.sleep(0.005)
            self.write_byte(0, oldmode | 0xa1)  # This sets the MODE1 register to turn on auto increment.
            # print("now " + str(self.read_byte(0)))
        except Exception as e:
            print(e)

    def setPWM(self, num, on, off):
        self.write_byte(num * 4 + LED0_ON_L, on)
        self.write_byte(num * 4 + LED0_ON_H, on >> 8)
        self.write_byte(num * 4 + LED0_OFF_L, off)
        self.write_byte(num * 4 + LED0_OFF_H, off >> 8)

    def set_Angle(self,
                  num,
                  angle: float
                  ):
        """
        num通道转动到angle角度，最快
        :param num:
        :param angle:
        :return:
        """
        # print(f'{num}通道:{angle} 角度')
        # 匹配到对应位深度
        val = map_range(min(angle, 180))
        val_int = round(val)
        self.setPWM(num, 4095 - val_int, 0)

    def angle_switch(self,
                     num,
                     start_angle: float,
                     stop_angle: float,
                     speed: float
                     ):
        """
        按照特定速度从start_angle转到stop_angle
        :param num:通道编号
        :param start_angle:
        :param stop_angle:
        :param speed:
        :return:
        """
        # 同步转动
        if num == 0:
            self.Mqtt_ins.publish("motion1/foot", str(stop_angle))
        elif num == 4:
            self.Mqtt_ins.publish("motion1/body", str(stop_angle))
        elif num == 8:
            self.Mqtt_ins.publish("motion1/larm", str(stop_angle))
        elif num == 12:
            self.Mqtt_ins.publish("motion1/rarm", str(180 - stop_angle))

        # print(f'{num}通道从{start_angle}到{stop_angle}')
        if num == 0:
            start_angle = start_angle + 5
            stop_angle = stop_angle + 5
        elif num == 4:
            start_angle = start_angle - 3
            stop_angle = stop_angle - 3
        elif num == 8:
            start_angle = start_angle - 5
            stop_angle = stop_angle - 5
        elif num == 12:
            start_angle = start_angle - 2
            stop_angle = stop_angle - 2
            start_angle = 180 - start_angle
            stop_angle = 180 - stop_angle

        # 从开始位置运动
        # self.set_Angle(num, start_angle)
        # 生成运动曲线
        if start_angle < stop_angle:
            float_array = bezier.angle_bezier_clamped(start_angle, stop_angle, start_angle * 1.1, stop_angle * 0.8,
                                                      round(10 * abs(start_angle - stop_angle) / speed))
        else:
            float_array = bezier.angle_bezier_clamped(start_angle, stop_angle, start_angle * 0.75, stop_angle * 1.1,
                                                      round(10 * abs(start_angle - stop_angle) / speed))

        # 执行运动曲线
        if num == 0:
            for i in float_array:
                self.Mqtt_ins.father_robot.foot = i
                self.set_Angle(num, i)
        if num == 4:
            for i in float_array:
                self.Mqtt_ins.father_robot.body = i
                self.set_Angle(num, i)
        if num == 8:
            for i in float_array:
                self.Mqtt_ins.father_robot.larm = i
                self.set_Angle(num, i)
        if num == 12:
            for i in float_array:
                self.Mqtt_ins.father_robot.rarm = i
                self.set_Angle(num, i)
        time.sleep(speed * 0.4)


if __name__ == '__main__':
    pwm_ins1 = PWM()
    pwm_ins1.test()
    speed = 2
    for j in range(90, 120):
        pwm_ins1.angle_switch(0, j, j + 1, speed)
        pwm_ins1.angle_switch(4, j, j + 1, speed)
        pwm_ins1.angle_switch(8, j, j + 1, speed)
        pwm_ins1.angle_switch(12, j, j + 1, speed)
    time.sleep(2)
    for j in range(120, 90, -1):
        pwm_ins1.angle_switch(0, j, j - 1, speed)
        pwm_ins1.angle_switch(4, j, j - 1, speed)
        pwm_ins1.angle_switch(8, j, j - 1, speed)
        pwm_ins1.angle_switch(12, j, j - 1, speed)
    time.sleep(10)
    for j in range(0, 13, 4):
        pwm_ins1.angle_switch(j, 90, 30, 2)
        pwm_ins1.angle_switch(j, 30, 150, 3)
        pwm_ins1.angle_switch(j, 150, 30, 3)
        pwm_ins1.angle_switch(j, 30, 90, 2)
