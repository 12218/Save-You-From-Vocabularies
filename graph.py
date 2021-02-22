from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel,QAction, qApp, QInputDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys
import get_list
import Baidu
import requests
import mp3play
import threading
import time

class root(QMainWindow):
    def __init__(self):
        super().__init__()
        self.position = 0 # 单词列表位置
        self.sentence_position = 0 # 例句列表位置
        self.word_visible = 0 # 单词区域是否可见
        self.liju_visible = 0 # 例句区域是否可见
        self.fanyi_visible = 0 # 翻译区域是否可见
        self.current_word = '' # 现在显示的单词
        self.information = '' # 错误提示
        self.text = '' # 输入的词汇
        self.word_list = []
        self.liju_list = [] # 例句列表
        self.fanyi_list = [] # 翻译列表
        self.word_qss = '''
            QLabel{background-color: white; font-size: 18px; font-family: Microsoft YaHei; border-radius: 5px;}
            QLabel:hover{border: 1px solid lightblue;}
        '''
        self.word_qss_changed = '''
            QLabel{color: rgb(128, 128, 128); background-color: rgb(128, 128, 128); font-size: 18px; font-family: Microsoft YaHei; border-radius: 5px;}
            QLabel:hover{border: 1px solid gray;}
        '''
        self.qss = '''
            QLabel{background-color: white; font-size: 16px; font-family: Microsoft YaHei; border-radius: 5px;}
            QLabel:hover{border: 1px solid lightblue;}
        ''' # 文字框原样式
        self.qss_changed = '''
            QLabel{color: rgb(128, 128, 128); background-color: rgb(128, 128, 128); font-size: 16px; font-family: Microsoft YaHei; border-radius: 5px;}
            QLabel:hover{border: 1px solid gray;}
        ''' # 文字框隐藏样式
        self.initUI()

    def initUI(self):
        self.resize(600, 420)
        self.setFixedSize(self.width(), self.height()) # 限定宽高
        self.setWindowTitle('Save You From Vocabularies')
        self.statusBar().showMessage('准备就绪') # 状态栏

        icon = QIcon('resources/icon.png')
        self.setWindowIcon(icon) # 设置图标

        # 设定一个名为exitAct的动作，用于退出程序
        exitAct = QAction('退出', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(qApp.quit) # 绑定退出动作

        # 设定一个名为addWords的动作，用于添加单词
        addWords = QAction('添加单词', self)
        addWords.setShortcut('Ctrl+I')
        addWords.triggered.connect(self.input_words)

        menubar = self.menuBar()
        startMenu = menubar.addMenu('开始')
        startMenu.addAction(exitAct) # 将exitAct添加到菜单栏
        startMenu.addAction(addWords) # 将addWords添加到菜单栏

        # 单词部分
        word_label = QLabel('单词', self)
        word_label.setStyleSheet('font-size: 20px; font-family: Microsoft YaHei;')
        word_label.move(70, 50)

        self.word_button = QPushButton('', self)
        self.word_button.setStyleSheet('border-image: url(resources/eye_on.png)')
        self.word_button.resize(30, 30)
        self.word_button.move(20, 50)
        self.word_button.clicked.connect(self.word_function)

        self.word_text = QLabel('', self) # 例句文字显示部分
        self.word_text.setTextInteractionFlags(Qt.TextSelectableByMouse) # 使文字可被选择复制
        self.word_text.setStyleSheet(self.word_qss) # 设置文字框样式
        self.word_text.resize(250, 30)
        self.word_text.move(130, 50)

        # 例句部分
        liju_label = QLabel('例句', self)
        liju_label.setStyleSheet('font-size: 20px; font-family: Microsoft YaHei;')
        liju_label.move(70, 100)

        self.liju_button = QPushButton('', self)
        self.liju_button.setStyleSheet('border-image: url(resources/eye_on.png)')
        self.liju_button.resize(30, 30)
        self.liju_button.move(20, 100)
        self.liju_button.clicked.connect(self.liju_function)

        self.liju_text = QLabel('', self) # 例句文字显示部分
        self.liju_text.setWordWrap(True) # 自动换行
        self.liju_text.setAlignment(Qt.AlignTop) # 从顶部开始显示文字
        self.liju_text.setTextInteractionFlags(Qt.TextSelectableByMouse) # 使文字可被选择复制
        self.liju_text.setStyleSheet(self.qss) # 设置文字框样式
        self.liju_text.resize(560, 110)
        self.liju_text.move(20, 130)

        # 播放例句按钮
        self.liju_play = QPushButton('', self)
        self.liju_play.setStyleSheet('''
            QPushButton{border-image: url(resources/play.png)}
            QPushButton:hover{border-image: url(resources/play_blue.png)}
            ''')
        self.liju_play.resize(30, 30)
        self.liju_play.move(130, 100)
        self.liju_play.clicked.connect(self.liju_play_function)

        # 翻译部分
        fanyi_label = QLabel('翻译', self)
        fanyi_label.setStyleSheet('font-size: 20px; font-family: Microsoft YaHei;')
        fanyi_label.move(70, 250)

        self.fanyi_button = QPushButton('', self)
        self.fanyi_button.setStyleSheet('border-image: url(resources/eye_on.png)')
        self.fanyi_button.resize(30, 30)
        self.fanyi_button.move(20, 250)
        self.fanyi_button.clicked.connect(self.fanyi_function)

        self.fanyi_text = QLabel('', self) # 翻译文字显示部分
        self.fanyi_text.setWordWrap(True) # 自动换行
        self.fanyi_text.setAlignment(Qt.AlignTop) # 从顶部开始显示文字
        self.fanyi_text.setTextInteractionFlags(Qt.TextSelectableByMouse) # 使文字可被选择复制
        self.fanyi_text.setStyleSheet(self.qss) # 设置文字框样式
        self.fanyi_text.resize(560, 110)
        self.fanyi_text.move(20, 280)

        # 单词切换按钮
        self.next_button = QPushButton('', self)
        self.next_button.setStyleSheet('''
            QPushButton{border-image: url(resources/next.png)}
            QPushButton:hover{border-image: url(resources/next_blue.png)}
            ''')
        self.next_button.resize(30, 30)
        self.next_button.move(400, 50)
        self.next_button.clicked.connect(self.next_function)

        # 句子切换按钮
        self.next_sentence_button = QPushButton('', self)
        self.next_sentence_button.setStyleSheet('''
            QPushButton{border-image: url(resources/next.png)}
            QPushButton:hover{border-image: url(resources/next_blue.png)}
            ''')
        self.next_sentence_button.resize(30, 30)
        self.next_sentence_button.move(180, 100)
        self.next_sentence_button.clicked.connect(self.next_liju_function)

        self.show()

    def input_words(self):
        text, ok = QInputDialog.getMultiLineText(self, '输入单词', '请输入需要学习的单词')
        if ok:
            self.position = 0 # 单词列表位置置零
            self.sentence_position = 0 # 例句列表位置置零
            self.text = text
            self.word_list = self.text.split('\n')
            while '' in self.word_list:
                # 删除空行
                self.word_list.remove('')
            # print(word_list)
            # print(type(word_list))

    # 切换下一单词函数
    def next_function(self):
        if len(self.word_list) == 0:
            # print('No Words Now')
            # self.word_text.setText('还未输入单词')
            self.info('还未输入单词\n菜单栏"开始->添加单词"')
        else:
            if self.position <= len(self.word_list) - 1: # 判断是否越界
                # print(self.position)
                self.word_text.setText(self.word_list[self.position])
                self.current_word = self.word_list[self.position]
                self.position += 1
                self.statusBar().showMessage('第' + str(self.position) + '个单词, 第' + str(self.sentence_position) + '个例句')
                # self.search()
                self.client_th = threading.Thread(target = self.search)
                self.client_th.setDaemon(True)
                self.client_th.start()
            else:
                # print('No word left')
                self.word_text.setText('已学习完所有单词')
                self.info('已学习完所有单词')
                self.statusBar().showMessage('已完成单词学习')

    # 切换下一例句函数
    def next_liju_function(self):
        if len(self.liju_list) == 0:
            # self.liju_text.setText('没有例句')
            self.info('没有输入例句')
        else:
            if self.sentence_position <= len(self.liju_list) - 1: # 判断是否越界
                # print(self.sentence_position)
                self.liju_text.setText(self.liju_list[self.sentence_position])
                self.fanyi_text.setText(self.fanyi_list[self.sentence_position])
                self.sentence_position += 1
                self.statusBar().showMessage('第' + str(self.position) + '个单词, 第' + str(self.sentence_position) + '个例句')
            else:
                # self.liju_text.setText('已学习完所有例句')
                self.info('已学习完所有例句')

    # 查例句函数
    def search(self):
        baidu = Baidu.getJson(self.current_word) # 得到现在显示的单词
        json = baidu.fetch_json() # 获取json值

        try:
            if json['trans_result'] == 0:
                # print('请求失败 Baidu.py')
                self.info('请求失败 Baidu.py出现问题')
            else:
                root = get_list.json_list(json)
                self.liju_list, self.fanyi_list = root.turn_list() # 得到例句和翻译的列表
                # print(self.liju_list)
                # print(self.fanyi_list)
        except:
            # print('包含错误单词或请求失败')
            self.info('包含错误单词或请求失败!')

    # 单词按钮函数
    def word_function(self):
        if self.word_visible == 0:
            self.word_button.setStyleSheet('border-image: url(resources/eye_off.png)')
            self.word_text.setStyleSheet(self.word_qss_changed) # 设置文字框隐藏样式
            self.word_visible = 1
        elif self.word_visible == 1:
            self.word_button.setStyleSheet('border-image: url(resources/eye_on.png)')
            self.word_text.setStyleSheet(self.word_qss)  # 设置文字框原样式
            self.word_visible = 0

    # 例句按钮函数
    def liju_function(self):
        if self.liju_visible == 0:
            self.liju_button.setStyleSheet('border-image: url(resources/eye_off.png)')
            self.liju_text.setStyleSheet(self.qss_changed) # 设置文字框隐藏样式
            self.liju_visible = 1
        elif self.liju_visible == 1:
            self.liju_button.setStyleSheet('border-image: url(resources/eye_on.png)')
            self.liju_text.setStyleSheet(self.qss)  # 设置文字框原样式
            self.liju_visible = 0

    # 翻译按钮函数
    def fanyi_function(self):
        if self.fanyi_visible == 0:
            self.fanyi_button.setStyleSheet('border-image: url(resources/eye_off.png)')
            self.fanyi_text.setStyleSheet(self.qss_changed) # 设置文字框隐藏样式
            self.fanyi_visible = 1
        elif self.fanyi_visible == 1:
            self.fanyi_button.setStyleSheet('border-image: url(resources/eye_on.png)')
            self.fanyi_text.setStyleSheet(self.qss) # 设置文字框原样式
            self.fanyi_visible = 0

    # 播放例句函数
    def liju_play_function(self):
        try:
            if self.liju_text.text() == '':
                self.info('无输入例句!')
            else:
                response = requests.get('https://fanyi.baidu.com/gettts?lan=uk&text=' + self.liju_text.text() + '&spd=3&source=web')
                with open('mp3/audio.mp3', 'wb') as file:
                    file.write(response.content)
                file.close()

                # 播放例句
                # self.client_th.terminate()
                self.client_th = threading.Thread(target = self.play_sound)
                self.client_th.setDaemon(True)
                self.client_th.start()
        except:
            # print('无法播放音频')
            self.info('无法播放音频')

    # 播放音频的函数
    def play_sound(self):
        clip = mp3play.load('./mp3/audio.mp3')
        clip.play()
        time.sleep(10)
        clip.stop()

    # 错误提示框
    def info(self, information):
        reply = QMessageBox.information(self, '提示', information, QMessageBox.Close, QMessageBox.Close)
        # if reply == QMessageBox.Ok:
        #     self.la.setText('你选择了Ok！')
        # else:
        #     self.la.setText('你选择了Close！')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = root()
    sys.exit(app.exec_())