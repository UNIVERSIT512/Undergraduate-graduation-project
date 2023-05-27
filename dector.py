# coding=UTF-8
import RPi.GPIO as GPIO
import time
 
# 设置警告信息为不输出
GPIO.setwarnings(False)
# 使用BCM针脚编号方式
GPIO.setmode(GPIO.BCM)
# 控制引脚GPIO22
trig = 20
# 接收引脚GPIO17
echo = 16
vcc_pin = 19
# 设置trig引脚为输出模式，初始化输出为低电平
GPIO.setup(trig, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(vcc_pin, GPIO.OUT, initial=GPIO.HIGH)
# 设置echo引脚为输入模式
GPIO.setup(echo, GPIO.IN)
HIGH = 1
LOW = 0
 
 
# 测量函数
def measure():
    # 树莓派向trig引脚发送信号，一个持续10us的方波脉冲
    GPIO.output(trig, HIGH)
    time.sleep(0.00001)
    GPIO.output(trig, LOW)
 
    # HC - SR04接收到脉冲信号，开始发送超声波并将Echo引脚置为高电平
    # echo引脚之前一直接收低电平信号，一旦收到高电平信号就开始记录时间
    while GPIO.input(echo) == LOW:
        pass
    start = time.time()
    # 当 HC-SR04 接收到返回的超声波 时，把Echo引脚置为低电平
    # 也就是说echo引脚接收到的高电平结束，终止计时
    while GPIO.input(echo) == HIGH:
        pass
    end = time.time()
 
    # 计算距离，单位厘米，这里的340m/s是超声波在空气中的传播速度
    distance = round((end - start)*340/2*100, 2)
    return distance
    
 
# 循环测距，间隔为1秒

# 清理脚本使用过的 GPIO 通道
#GPIO.cleanup()