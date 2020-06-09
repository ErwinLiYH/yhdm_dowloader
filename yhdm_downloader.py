from PySide2.QtWidgets import QApplication,QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile,QObject,Signal
from PySide2.QtGui import QIcon
import resourse
from threading import Thread
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from os import path
from time import sleep

class main_win:
    info = ''
    def __init__(self):
        self.ui_file = QFile("yhdm.ui")
        self.ui_file.open(QFile.ReadOnly)
        self.loader = QUiLoader()
        self.ui = self.loader.load(self.ui_file)
        self.ui_file.close()
        self.ui.pushButton_2.clicked.connect(self.download)
        self.ui.pushButton.clicked.connect(self.show_vice_win)
        self.ms_warning = my_signal()
        self.ms_warning.warning.connect(self.warning)
        self.ms_warning.text_append.connect(self.Append)
        self.ui.show()
        
    def download(self):
        self.url = self.ui.lineEdit.text()
        self.path_ = self.ui.lineEdit_2.text()
        self.name = self.ui.lineEdit_3.text()
        print(self.url,self.path_,self.name)
        def run():
            self.ui.pushButton_2.setEnabled(False)
            try:
                if path.exists(self.path_):
                    self.info = '开始连接'
                    self.ms_warning.text_append.emit(self.info)
                    sleep(0.1)
                    conn = requests.get(self.url)
                    if conn.status_code == 200:
                        self.info = '连接成功'
                        self.ms_warning.text_append.emit(self.info)
                        sleep(0.1)
                        soup = BeautifulSoup(conn.text,"html.parser")
                        a = soup.find(name='div',id = 'playbox')
                        dow_url = a['data-vid'].split('$')[0]
                        print(dow_url)
                        self.info = '资源地址:'+dow_url
                        self.ms_warning.text_append.emit(self.info)
                        sleep(0.1)
                        if dow_url.startswith('http'):                 # normal case
                            self.info = '开始下载......'
                            self.ms_warning.text_append.emit(self.info)
                            sleep(0.1)
                            conn2 = requests.get(dow_url)
                            if conn2.status_code == 200:
                                self.info = '下载完成，开始写入'
                                self.ms_warning.text_append.emit(self.info)
                                sleep(0.1)
                                with open(self.path_+'/'+self.name,'wb') as mp4:
                                    mp4.write(conn2.content)
                                self.info = '写入完成，文件地址:'+self.path_+'/'+self.name
                                self.ms_warning.text_append.emit(self.info)
                                sleep(0.1)
                            else:
                                self.info = '连接失败，状态码：'+str(conn2.status_code)
                                self.ms_warning.text_append.emit(self.info)
                                sleep(0.1)
                        else:                                          # flash case
                            self.info = 'special case: flash player'
                            self.ms_warning.text_append.emit(self.info)
                            sleep(0.1)
                            self.info = 'special case: 开始解析，请勿关闭浏览器'
                            self.ms_warning.text_append.emit(self.info)
                            sleep(0.1)
                            driver = webdriver.Chrome('./chromedriver.exe')
                            driver.get(self.url)
                            sleep(2)
                            url_el = driver.find_element_by_tag_name('iframe')
                            mp4_url = url_el.get_attribute('src')
                            self.info = '进度 1 结束'
                            self.ms_warning.text_append.emit(self.info)
                            sleep(0.1)
                            driver.get(mp4_url)
                            sleep(2)
                            url_el = driver.find_element_by_tag_name('iframe')
                            mp4_url = url_el.get_attribute('src')
                            self.info = '进度 2 结束'
                            self.ms_warning.text_append.emit(self.info)
                            sleep(0.1)
                            driver.get(mp4_url)
                            sleep(2)
                            url_el = driver.find_element_by_xpath('//*[@id="a1"]/div[2]/video')
                            mp4_url = url_el.get_attribute('src')
                            self.info = '进度 3 结束\n视频地址: '+mp4_url
                            self.ms_warning.text_append.emit(self.info)
                            sleep(0.1)
                            self.info = '开始下载......'
                            self.ms_warning.text_append.emit(self.info)
                            sleep(0.1)
                            conn3 = requests.get(mp4_url)
                            self.info = '下载完成，开始写入'
                            self.ms_warning.text_append.emit(self.info)
                            sleep(0.1)
                            if conn3.status_code ==200:
                                with open(self.path_+'/'+self.name,'wb') as mp4:
                                    mp4.write(conn3.content)
                                self.info = '写入完成，文件地址:'+self.path_+'/'+self.name
                                self.ms_warning.text_append.emit(self.info)
                                sleep(0.1)
                            else:
                                self.info = '连接失败，状态码：'+str(conn3.status_code)
                                self.ms_warning.text_append.emit(self.info)
                                sleep(0.1)
                    else:
                        self.info = '连接失败'+str(conn.status_code)
                        self.ms_warning.text_append.emit(self.info)
                else:
                    print('此路径不存在')
                    self.info = '此路径不存在:'+self.path_
                    self.ms_warning.text_append.emit(self.info)
            except Exception as e:
                self.error = str(e)
                self.ms_warning.warning.emit(self.error)
            self.ui.pushButton_2.setEnabled(True)
        download_thread = Thread(target=run)
        download_thread.start()
    def show_vice_win(self):
        self.vice_windows = vice_win()

    def warning(self):
        QMessageBox.warning(self.ui,'INPUT ERROR',self.error)

    def Append(self):
        self.ui.plainTextEdit.appendPlainText(self.info)

class vice_win:
    def __init__(self):
        self.ui_file = QFile("vice.ui")
        self.ui_file.open(QFile.ReadOnly)
        self.loader = QUiLoader()
        self.ui = self.loader.load(self.ui_file)
        self.ui_file.close()
        self.ui.show()

class my_signal(QObject):
    warning = Signal(str)
    text_append = Signal(str)

app = QApplication([])
main_win1 = main_win()
app.setWindowIcon(QIcon('image/sakura.png'))
app.exec_()