import cv2
import tkinter as tk
from PIL import Image, ImageTk

class CameraApp:
    def __init__(self, window, video_source=0):
        self.window = window
        self.window.title("Camera Application")

        # 打开视频流
        self.cap = cv2.VideoCapture(video_source)

        # 获取视频的帧率
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))

        # 创建画布
        self.canvas = tk.Canvas(window, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        # 显示帧数的标签
        self.fps_label = tk.Label(window, text='FPS: {}'.format(self.fps))
        self.fps_label.pack()

        # 启动定时器，每隔一段时间调用更新函数以刷新画面
        self.delay = int(1000 / self.fps)
        self.update()

        # 关闭窗口时释放资源
        self.window.protocol("WM_DELETE_WINDOW", self.close)

    def update(self):
        # 读取一帧
        ret, frame = self.cap.read()

        if ret:
            # 将图像转换为PIL格式
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image=image)

            # 在画布上显示图像
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            self.canvas.image = photo

        # 在标签上显示帧率
        self.fps_label.config(text='FPS: {:.2f}'.format(self.fps))

        # 定时器调用更新函数以刷新画面
        self.window.after(self.delay, self.update)

    def close(self):
        # 释放资源
        self.cap.release()
        self.window.destroy()

# 创建Tkinter窗口并启动程序
window = tk.Tk()
app = CameraApp(window)
window.mainloop()
