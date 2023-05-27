本设计由树莓派主控，搭配摄像头模块、刷卡模块、体温测量模块、音响模块和触摸屏模块完成。系统为树莓派的官方linux系统。

---

# 硬件组成
### 结构图
![image.png](https://cdn.nlark.com/yuque/0/2023/png/35345331/1685179893092-51906b4e-7e0c-45e2-9471-6cfa50213ad4.png#averageHue=%23f9f9f9&clientId=u4434ff2b-6ea4-4&from=paste&height=441&id=ubc148ee9&originHeight=744&originWidth=1157&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=31560&status=done&style=none&taskId=uf08e65de-b466-4e52-baad-36bf799001c&title=&width=686.4000244140625)
### 实物连接
![fd6f3e5b51faedc47fd333da72e93ad.jpg](https://cdn.nlark.com/yuque/0/2023/jpeg/35345331/1685180175060-af75f871-b211-4f12-8932-bbbb73192240.jpeg#averageHue=%2348503f&clientId=u4434ff2b-6ea4-4&from=paste&height=401&id=u09af6c31&originHeight=1080&originWidth=1920&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=293888&status=done&style=none&taskId=u57091395-784e-467b-9b17-c8e0892c4c1&title=&width=712.4000244140625)
### 硬件组成列表：

- 树莓派4B 2G版本
- 触摸屏 淘宝买的150块烂屏幕
- 音响模块 随便买的 还行
- 摄像头模块 淘宝随便买的烂摄像头
- 刷卡模块 RFID-RC522
- 温度测量模块 MLX90614

---

# 软件组成
### 结构图
![image.png](https://cdn.nlark.com/yuque/0/2023/png/35345331/1685180232536-bc9c9730-8c66-450a-b4a5-d96e66df0c0b.png#averageHue=%23f9f9f9&clientId=u4434ff2b-6ea4-4&from=paste&height=460&id=udb78fb59&originHeight=816&originWidth=909&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=33362&status=done&style=none&taskId=ua5099d81-b79f-4e48-882b-89d8a567c8a&title=&width=512.2000122070312)
系统启动后，程序首先对刷卡程序、体温测量程序、pyqt界面相应的库和人脸识别程序进行初始化，然后与sqlite数据库进行连接，并开启opencv摄像头进程，后续通过用户与系统的互动再开启刷卡进程，完成体温测量，口罩识别，语音播报操作。并将每个学生的id与体温数据通过sqlite储存起来。老师可以通过“信息总汇”键将学生数据发送到自己邮箱立，查询学生数据，学生也可以通过“信息查询”刷卡获得自己的信息。
### 环境配置工作：

- opencv-python
- pyqt5 #python自带
- sqlite #python自带
- RFID-RC522的配置 [参考博客](https://blog.csdn.net/qq_40259641/article/details/108749501)
- MLX90614的配置 [ 参考博客](https://www.cnblogs.com/likehc/p/15374827.html)
- edge-tts [GitHub链接](https://github.com/rany2/edge-tts)
- 口罩识别  [GitHub链接](https://github.com/AIZOOTech/FaceMaskDetection) #用gpt改成了调用接口
- socket，yagmail #发送邮箱需要用到
- xlsxwriter 用sqlite表格转化为excel文件
