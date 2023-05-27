from readTemp import readTemp_
from Read import readCard
import sys
import sqlite3
import threading
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QTimer,pyqtSignal
from PyQt5.QtWidgets import QLineEdit,QApplication,QPushButton,QDesktopWidget
import time
from maskdetection import detect_mask
import asyncio
import os
import edge_tts
import pygame
import socket
import xlsxwriter
import yagmail
import random

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.camera_label = QtWidgets.QLabel(self)
        self.temperature_label = QtWidgets.QLabel('   体温检测',self)
        self.mask_label = QtWidgets.QLabel('   口罩识别 ',self)
        self.card_button = QtWidgets.QPushButton('刷卡', self)
        self.admin_button = QtWidgets.QPushButton('信息查询', self)
        self.mission_button = QtWidgets.QPushButton('信息总汇',self)
        self.temperature_text =QtWidgets.QLabel(self)
        self.mask_text =QtWidgets.QLabel(self)
        self.bar_label = QtWidgets.QLabel(self)
        self.reset_button = QtWidgets.QPushButton('重启系统',self)
        
        self.temperature_text.setStyleSheet('background-color: lightblue;')
        self.mask_label.setStyleSheet('background-color: white;')
        self.temperature_label.setStyleSheet('background-color: white;')
        self.mask_text.setStyleSheet('background-color: yellow;')
        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setFixedWidth(800)
        self.text_label.move(20, 20)
        self.text_label.setStyleSheet('color: blue; font-size: 24px')
        # 设置组件位置和大小
        
        self.screen_size = QDesktopWidget().screenGeometry().size()
        self.bar_label.setGeometry(820,90,190,30)
        self.camera_label.setGeometry(0, 0, self.screen_size.width(), self.screen_size.height())
        self.mask_label.setGeometry(820, 50, 100, 50)
        self.mask_text.setGeometry(920,50,100,50)
        self.temperature_label.setGeometry(820, 0, 100, 50)
        self.temperature_text.setGeometry(920, 0, 100, 50)
        self.card_button.setGeometry(870, 140, 120, 60)
        self.admin_button.setGeometry(870, 240, 120, 60)
        self.mission_button.setGeometry(870,340,120,60)
        self.reset_button.setGeometry(940,480,80,50)
        # 设置按钮点击事件
        self.card_button.clicked.connect(self.on_card_button_clicked)
        self.admin_button.clicked.connect(self.on_admin_button_clicked)
        self.reset_button.clicked.connect(self.on_reset_button_clicked)
        self.mission_button.clicked.connect(self.on_mission_button_clicked)
        self.temperature_text.setText("         NULL")
        self.mask_text.setText("         NULL")

        # 启动摄像头
        self.cap = cv2.VideoCapture(0)
        self.timer_camera = QtCore.QTimer()
        self.timer_camera.timeout.connect(self.show_camera)
        
        self.timer_camera.start(30)
    
    def show_camera(self):
        ret, self.frame = self.cap.read()
        if ret:
            self.frame = cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)
            height, width, bytesPerComponent = self.frame.shape
            bytesPerLine = bytesPerComponent * width
            convertToQtFormat = QtGui.QImage(self.frame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
            p = convertToQtFormat.scaled(820, 640, Qt.KeepAspectRatio)
            self.camera_label.setPixmap(QtGui.QPixmap.fromImage(p))

    def on_card_button_clicked(self):
        # 启动刷卡线程
        threading.Thread(target=self.card_thread).start()

    def on_admin_button_clicked(self):
        threading.Thread(target=self.find_thread).start()
        
    def on_mission_button_clicked(self):
        threading.Thread(target=self.mission_thread).start()
    
    def on_reset_button_clicked(self):
        self.speak_text("系统即将重新启动")
        self.cap.release()
        python = sys.executable
        os.execl(python,python,*sys.argv)
        
    def check_internet_connection(self):
        try:
            # 创建一个套接字对象
            socket.create_connection(("www.baidu.com", 80))
            return True
        except OSError:
            pass
        return False
    
    def mission_thread(self):
        if self.check_internet_connection():
            str = '▮'
            self.speak_text("数据处理中")
            pygame.time.delay(1500)
            conn = sqlite3.connect('user_database.db')
            cursor = conn.cursor()
            query = 'SELECT * FROM users'
            cursor.execute(query)
            results = cursor.fetchall()
            workbook = xlsxwriter.Workbook('output.xlsx')
            worksheet = workbook.add_worksheet()

            # 写入表头
            header = [i[0] for i in cursor.description]
            for col, column_name in enumerate(header):
                worksheet.write(0, col, column_name)

            # 写入数据
            for row, row_data in enumerate(results):
                for col, value in enumerate(row_data):
                    worksheet.write(row + 1, col, value)

            # 关闭数据库连接和保存 Excel 文件
            cursor.close()
            conn.close()
            workbook.close()
            for i in range(21):
                str += '▮'
                time.sleep(random.uniform(0,0.6))
                self.bar_label.setText(str)
            str = '▮'
            self.speak_text("数据发送中")
            self.bar_label.setText('')
            yag = yagmail.SMTP(user="", password="", host='')
            # 发送邮件
            yag.send(
                # to 收件人，如果一个收件人用字符串，多个收件人用列表即可
                to=['', ''],
                # cc 抄送，含义和传统抄送一致，使用方法和to 参数一致
                # subject 邮件主题（也称为标题）
                subject='邮件主题',
                # contents 邮件正文
                contents='邮件正文',
                # attachments 附件，和收件人一致，如果一个附件用字符串，多个附件用列表
                attachments='output.xlsx')
            # 记得关掉链接，避免浪费资源
            yag.close()
            for i in range(21):
                str += '▮'
                time.sleep(random.uniform(0,0.6))
                self.bar_label.setText(str)
            self.speak_text("数据发送完毕")
            self.bar_label.setText('')
        else:
           
           self.speak_text("您好，无法连接到互联网，请检查您的网络连接情况")

    def find_thread(self):
        self.temperature_text.setText("         NULL")
        self.mask_text.setText("         NULL")
        self.text_label.setText("您好，请进行刷卡")
        self.speak_text("您好，请进行刷卡")
        while True:
            card_id = readCard()
            time.sleep(1)
            if card_id != "":
                break
            
        self.conn = sqlite3.connect('user_database.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT temperature,mark FROM users WHERE card_id = ?", (card_id,))
        result = self.cursor.fetchone()
        self.cursor.close()
        self.conn.close()
        if result:
            self.speak_text("查询中")
            str = '▮'
            for i in range(21):
                str += '▮'
                time.sleep(random.uniform(0,0.3))
                self.bar_label.setText(str)
            self.bar_label.setText('')
            temperature,mark = result
            if mark == 1:
                self.temperature_text.setText("       %.2f °C" %temperature)
                self.mask_text.setText("       已佩戴")
            else:
                self.temperature_text.setText("       %.2f °C" %temperature)
                self.mask_text.setText("       未佩戴")
            self.text_label.setText("查询完毕")
            self.speak_text("您好，查询结果如右边所示")
        else:
            self.speak_text("查询中")
            str = '▮'
            for i in range(21):
                str += '▮'
                time.sleep(random.uniform(0,0.3))
                self.bar_label.setText(str)
            self.bar_label.setText('')
            self.text_label.setText("无查询结果")
            self.temperature_text.setText("       无结果")
            self.mask_text.setText("       无结果")
            self.speak_text("抱歉，系统里没有该学生的数据")
            
    def card_thread(self):
        # 显示“请进行刷卡”
        self.temperature_text.setText("         NULL")
        self.mask_text.setText("         NULL")
        self.text_label.setText("您好，请进行刷卡")
        self.speak_text('您好，请进行刷卡')
        self.text_label.setText("您好，请进行刷卡")

        while True:
            card_id = readCard()
            time.sleep(1)
            if card_id != "":
                break
    
        # 显示“请进行体温测量”
        mark = 0
        cv2.imwrite('photo.jpg',self.frame)
        result = detect_mask('photo.jpg', conf_thresh=0.5, iou_thresh=0.4, target_shape=(260, 260))
        self.text_label.setText(result + "")
        if result == "该学生已佩戴口罩！":
            mark = 1
            self.mask_text.setText("       已佩戴")
            self.speak_text(result + '接下来请进行体温测量')
        else:
            self.mask_text.setText("       未佩戴")
            self.speak_text(result + '为了您的安全着想,请佩戴好口罩.   接下来请进行体温测量')
        #self.text_label.setText('Taking temperature measurement.')
        while True:
            temperature = readTemp_()
            if temperature >36.2 and temperature < 38:
                break

        if temperature > 37.3:
            # 温度异常
            self.text_label.setText('温度异常,为 %.1f °C' % temperature)
            self.temperature_text.setText("       %.1f °C" %temperature)
            self.speak_text('温度异常,为 %.1f °C' % temperature)
        elif temperature >= 36.2 and temperature <= 37.3:
            # 温度正常
            self.temperature_text.setText("       %.1f °C" %temperature)
            self.text_label.setText('温度正常,为 %.1f °C' % temperature)
            self.speak_text('温度正常,为 %.1f °C' % temperature)
        self.speak_text('信息录入中')
        str = '▮'
        # 将用户数据存入数据库
        user_data = (card_id, temperature,mark)
        self.conn = sqlite3.connect('user_database.db')
        self.cursor = self.conn.cursor()
        #self.cursor.execute('''CREATE TABLE users (
        #card_id INTEGER PRIMARY KEY,
        #temperature REAL,
        #mark REAL
        #);''')
        self.cursor.execute('SELECT * FROM users WHERE card_id=?', (card_id,))
        result = self.cursor.fetchone()
        if result is None:
            self.cursor.execute('INSERT INTO users VALUES (?, ?, ?)', user_data)
        else:
            self.cursor.execute('UPDATE users SET temperature=?,mark = ? WHERE card_id=?', (temperature,mark, card_id))
        self.conn.commit()
        self.conn.close()
        #pygame.time.delay(1000)
        for i in range(21):
            str += '▮'
            time.sleep(random.uniform(0,0.3))
            self.bar_label.setText(str)
        self.bar_label.setText('')
        self.speak_text('信息录入完毕')
    


    async def save_audio(self,text, output_file):
        voice = "zh-CN-XiaoxiaoNeural"

        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)


    def speak_text(self,text):
        temp_file = "temp_audio.mp3"

        # 保存文本到音频文件
        asyncio.run(self.save_audio(text, temp_file))

        # 使用pygame播放音频
        pygame.mixer.init()
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        # 增加一个延迟，单位为毫秒，例如：延迟1秒
        pygame.time.delay(500)
        pygame.mixer.quit()

        # 删除临时音频文件
        # os.remove(temp_file)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
