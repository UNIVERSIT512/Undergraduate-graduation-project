# coding=utf-8
import RPi.GPIO as GPIO
import MFRC522
 
# 创建一个MFRC522对象
MIFAREReader = MFRC522.MFRC522()
 
# 读取卡片ID的函数,能读到就返回卡片的ID,不能就返回空字符串
def readCard():
    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL) 
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
 
    # 如果卡片有ID
    if status == MIFAREReader.MI_OK:
        s = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
        return s
    else:
        return ""