import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class WorkerThread(QThread):
    progressChanged = pyqtSignal(int)

    def run(self):
        for i in range(101):
            self.progressChanged.emit(i)
            self.msleep(100)

class ProgressWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Progress Bar Example")
        self.setGeometry(200, 200, 300, 150)

        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(30, 40, 240, 25)

        self.workerThread = WorkerThread()
        self.workerThread.progressChanged.connect(self.updateProgressBar)
        self.workerThread.start()

    def updateProgressBar(self, value):
        self.progressBar.setValue(value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = ProgressWindow()
    mainWindow.show()
    sys.exit(app.exec_())
