import wiringpi
import numpy as np
import argparse
import time
import bezier

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
        wiringpi.wiringPiSetup()
        self.fd = wiringpi.wiringPiI2CSetupInterface(args.device, i2caddr)
        self.reset()
        self.setPWMFreq(50)

    def write_byte(self, reg, byte):
        if wiringpi.wiringPiI2CWriteReg8(self.fd, reg, byte) < 0:
            print("Error write byte to device")
            return -1
        return 0

    def read_byte(self, reg):
        byte = wiringpi.wiringPiI2CReadReg8(self.fd, reg)
        if byte < 0:
            print("Error read byte from device")
            return -1
        return byte

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

        # 设置MODE1寄存器为睡眠模式
        newmode = (oldmode & 0x7F) | 0x10  # sleep
        self.write_byte(0, newmode)  # go to sleep
        self.write_byte(0XFE, prescale)  # set the prescaler
        # print(prescale)
        self.write_byte(0, oldmode)
        time.sleep(0.005)
        self.write_byte(0, oldmode | 0xa1)  # This sets the MODE1 register to turn on auto increment.
        # print("now " + str(self.read_byte(0)))

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
        print(f'{num}通道从{start_angle}到{stop_angle}')
        self.set_Angle(num, start_angle)
        if start_angle < stop_angle:
            float_array = bezier.angle_bezier_clamped(start_angle, stop_angle, start_angle * 1.1, stop_angle * 0.8,
                                                      round(10 * abs(start_angle - stop_angle) / speed))
        else:
            float_array = bezier.angle_bezier_clamped(start_angle, stop_angle, start_angle * 0.75, stop_angle * 1.1,
                                                      round(10 * abs(start_angle - stop_angle) / speed))
        # print(float_array)
        for i in float_array:
            self.set_Angle(num, i)

    def test(self):
        self.setPWMFreq(50)
        while 1:
            for j in range(0, 16):
                for i in range(0, 180):
                    self.set_Angle(j, i)
                    # time.sleep(0.1)
                    print(f"{j}通道{i}角度")
                # self.set_Angle(j, 90)


if __name__ == '__main__':
    pwm_ins1 = PWM()
    # pwm_ins1.test()
    for j in range(0, 12, 4):
        pwm_ins1.angle_switch(j, 90, 30, 2)
        pwm_ins1.angle_switch(j, 30, 150, 3)
        pwm_ins1.angle_switch(j, 150, 30, 3)
        pwm_ins1.angle_switch(j, 30, 90, 2)
