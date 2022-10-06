from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from database import Database
from files import Files
from time import sleep
import threading
import time
import cv2
from PIL import Image
import numpy
import os
from ffpyplayer.player import MediaPlayer
import sys

database = Database()
files = Files()

class VideoPlayer:
    def __init__(self, filename,volume = 1.0):
        if not os.path.exists(filename):raise FileNotFound(filename)
        self.close = False
        self.state = None
        self.frame = None
        self.l=None
        self.filename = filename
        self.skip_interval=5

        self.player = MediaPlayer(filename, ff_opts={'sync': 'audio', 'paused': False, 'volume': volume, 't': 1e7+1, 'ss': 0})
        time.sleep(1)
        self.duration=self.player.get_metadata()['duration']
        handler_thread = threading.Thread(target=self.play, args=(), daemon=True)
        handler_thread.start()

    def play(self):
        while True:
            frame, self.val = self.player.get_frame()
            if self.val == 'eof':self.close=True
            if self.close == True:
                self.player.toggle_pause()
                self.player.close_player()
                time.sleep(2)
                break

            if isinstance(self.val, str) or self.val == 0.0:waitkey = 32
            else:waitkey = int(self.val * 100)
            pressed_key = cv2.waitKey(waitkey) & 0xFF

            if frame is None:continue

            image, pts = frame
            self.frame = (image, self.val)
            x, y = image.get_size()
            data = image.to_bytearray()[0]
            image =  Image.frombytes("RGB", (x, y), bytes(data))
            image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
            self.frame=frame

            if self.l!=None:
                h, w, ch = image.shape
                Image2 = QImage(image.data, w, h, ch * w, QImage.Format_RGB888)
                self.pixmap=QPixmap.fromImage(Image2)
                self.l.setPixmap(self.pixmap)
                self.l.setFixedWidth(self.l.pixmap().width())
                self.l.setFixedHeight(self.l.pixmap().height())
                self.l.parent().update()
            del image


    def seek_p(self):
            if int(self.player.get_pts()) + self.skip_interval < int(self.duration):
                self.player.seek(self.skip_interval, relative=True, accurate=False)
    def seek_m(self):
        if int(self.player.get_pts()) - self.skip_interval > 0:
            self.player.seek(-self.skip_interval, relative=True, accurate=False)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.mainTitle = QtWidgets.QLabel(self.centralwidget)
        self.mainTitle.setGeometry(QtCore.QRect(220, 50, 371, 61))
        font = QtGui.QFont()
        font.setFamily("Microsoft Tai Le")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.mainTitle.setFont(font)
        self.mainTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.mainTitle.setObjectName("Title")
        #User Password
        self.usernameTitle = QtWidgets.QLabel(self.centralwidget)
        self.usernameTitle.setGeometry(QtCore.QRect(70, 180, 371, 61))
        font = QtGui.QFont()
        font.setFamily("Microsoft Tai Le")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.usernameTitle.setFont(font)
        self.usernameTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.usernameTitle.setObjectName("usernameTitle")
        self.passwordTitle = QtWidgets.QLabel(self.centralwidget)
        self.passwordTitle.setGeometry(QtCore.QRect(60, 260, 371, 61))
        font = QtGui.QFont()
        font.setFamily("Microsoft Tai Le")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.passwordTitle.setFont(font)
        self.passwordTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.passwordTitle.setObjectName("passwordTitle")
        self.usernameTextEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.usernameTextEdit.setGeometry(QtCore.QRect(370, 190, 271, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft Tai Le")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.usernameTextEdit.setFont(font)
        self.usernameTextEdit.setObjectName("usernameTextEdit")
        self.passwordTextEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.passwordTextEdit.setGeometry(QtCore.QRect(370, 270, 271, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft Tai Le")
        font.setPointSize(18)
        self.passwordTextEdit.setFont(font)
        self.passwordTextEdit.setObjectName("passwordTextEdit")
        #Join Button
        self.joinButton = QtWidgets.QPushButton(self.centralwidget)
        self.joinButton.setGeometry(QtCore.QRect(430, 350, 161, 41))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.joinButton.setFont(font)
        self.joinButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.joinButton.setStyleSheet("background-color: white;")
        self.joinButton.setObjectName("joinButton")
        #Bt Not have Accound
        self.dontHaveAccountLabal = QtWidgets.QLabel(self.centralwidget)
        self.dontHaveAccountLabal.setGeometry(QtCore.QRect(160, 470, 361, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft Tai Le")
        font.setPointSize(16)
        self.dontHaveAccountLabal.setFont(font)
        self.dontHaveAccountLabal.setObjectName("dontHaveAccountLabel")
        #Bt Create Accound
        self.createAccountButton = QtWidgets.QPushButton(self.centralwidget)
        self.createAccountButton.setGeometry(QtCore.QRect(510, 470, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft Tai Le")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.createAccountButton.setFont(font)
        self.createAccountButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.createAccountButton.setStyleSheet("background-color: white;")
        self.createAccountButton.setObjectName("createAccountButton")
        #Br Final Button Text
        self.createFinalButton = QtWidgets.QPushButton(self.centralwidget)
        self.createFinalButton.setGeometry(QtCore.QRect(430, 350, 161, 41))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.createFinalButton.setFont(font)
        self.createFinalButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.createFinalButton.setStyleSheet("background-color: white;")
        self.createFinalButton.setObjectName("createFinalButton")
        self.goToJoinButton = QtWidgets.QPushButton(self.centralwidget)
        self.goToJoinButton.setGeometry(QtCore.QRect(510, 470, 111, 31))
        #Bt Join
        font = QtGui.QFont()
        font.setFamily("Microsoft Tai Le")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.goToJoinButton.setFont(font)
        self.goToJoinButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.goToJoinButton.setStyleSheet("background-color: white;")
        self.goToJoinButton.setObjectName("goToJoinButton")
        # Bt have accound
        self.alreadyHaveAccountLabel = QtWidgets.QLabel(self.centralwidget)
        self.alreadyHaveAccountLabel.setGeometry(QtCore.QRect(230, 470, 241, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft Tai Le")
        font.setPointSize(16)
        self.alreadyHaveAccountLabel.setFont(font)
        self.alreadyHaveAccountLabel.setObjectName("alreadyHaveAccountLabel")

        #List Files
        self.listFiles = QtWidgets.QListWidget(self.centralwidget)
        self.listFiles.setGeometry(QtCore.QRect(20, 20, 200, 400))
        font = QtGui.QFont()
        font.setFamily("Microsoft Tai Le")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(28)
        self.listFiles.setFont(font)
        #self.listFiles.setAlignment(QtCore.Qt.AlignLeft)
        self.listFiles.setObjectName("listfilesList")

        #Video Player

        self.boxplayer = QtWidgets.QHBoxLayout(self.centralwidget)
        self.boxplayer.setGeometry(QtCore.QRect(20, 20, 200, 400))
        self.boxplayer.addWidget(self.listFiles)
        self.controls = QtWidgets.QVBoxLayout(self.centralwidget)
        self.boxplayer.addLayout(self.controls)
        #self.controls.setGeometry(QtCore.QRect(200, 20, 640, 480))

        self.video = QtWidgets.QLabel(self.centralwidget);
        self.controls.addWidget(self.video)

        self.pbplay = QPushButton('play');
        self.controls.addWidget(self.pbplay);
        self.pbplay.clicked.connect(self.play)

        self.pbstop = QPushButton('stop');
        self.controls.addWidget(self.pbstop);
        self.pbstop.clicked.connect(self.close)

        self.pbpause = QPushButton('pause');
        self.controls.addWidget(self.pbpause);
        self.pbpause.clicked.connect(self.pause)


        #Bt Login page
        self.detailsWongLabel = QtWidgets.QLabel(self.centralwidget)
        self.detailsWongLabel.setGeometry(QtCore.QRect(340, 150, 331, 21))

        #Text Login or Password Incorrect
        font = QtGui.QFont()
        font.setFamily("Microsoft Tai Le")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.detailsWongLabel.setFont(font)
        self.detailsWongLabel.setStyleSheet("")
        self.detailsWongLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.detailsWongLabel.setObjectName("detailsWongLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        #Text Account Already Exists
        self.accountAlreadyExistsLabel = QtWidgets.QLabel(self.centralwidget)
        self.accountAlreadyExistsLabel.setGeometry(QtCore.QRect(380, 140, 251, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft Tai Le")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.accountAlreadyExistsLabel.setFont(font)
        self.accountAlreadyExistsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.accountAlreadyExistsLabel.setObjectName("accountAlreadyExistsLabel")
        self.accountCreatedLabel = QtWidgets.QLabel(self.centralwidget)
        self.accountCreatedLabel.setGeometry(QtCore.QRect(380, 140, 251, 31))
        #Text Create accound
        font = QtGui.QFont()
        font.setFamily("Microsoft Tai Le")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.accountCreatedLabel.setFont(font)
        self.accountCreatedLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.accountCreatedLabel.setObjectName("accountCreatedLabel")



        #Menu Bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.joinWinLabels = [self.joinButton, self.createAccountButton, self.dontHaveAccountLabal,
                              self.usernameTextEdit, self.usernameTitle, self.passwordTextEdit, self.passwordTitle,
                              self.detailsWongLabel]
        self.createWinLabels = [self.goToJoinButton, self.createFinalButton, self.alreadyHaveAccountLabel,
                                self.usernameTextEdit, self.usernameTitle, self.passwordTextEdit, self.passwordTitle,
                                self.accountAlreadyExistsLabel, self.accountCreatedLabel]
        self.welcomeWinLabels = [self.listFiles,self.video,self.pbplay,self.pbstop,self.pbpause]

        self.joinButton.clicked.connect(self.joinClicked)
        self.createAccountButton.clicked.connect(self.goToCreateClicked)
        self.createFinalButton.clicked.connect(self.createAccountClicked)

        for label in self.createWinLabels:
            label.setHidden(True)
        for label in self.welcomeWinLabels:
            label.setHidden(True)
        for label in self.joinWinLabels:
            label.setHidden(False)
        self.detailsWongLabel.setHidden(True)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.mainTitle.setText(_translate("MainWindow", "Login"))
        self.usernameTitle.setText(_translate("MainWindow", "Usuario: "))
        self.passwordTitle.setText(_translate("MainWindow", "Senha:"))
        self.joinButton.setText(_translate("MainWindow", "Acessar"))
        self.dontHaveAccountLabal.setText(_translate("MainWindow", "Criar conta"))
        self.createAccountButton.setText(_translate("MainWindow", "Criar"))
        self.createFinalButton.setText(_translate("MainWindow", "Criar"))
        self.goToJoinButton.setText(_translate("MainWindow", "Acessar"))
        self.alreadyHaveAccountLabel.setText(_translate("MainWindow", "Já tem conta?"))
        self.detailsWongLabel.setText(_translate("MainWindow", "Login ou Senha Incorreto Tente novamente"))
        self.accountAlreadyExistsLabel.setText(_translate("MainWindow", "Conta já Existe"))
        self.accountCreatedLabel.setText(_translate("MainWindow", "Conta Criada"))

    def videoplayer(self):
        selectfile = self.listFiles.selectedItems()
        if len(selectfile) != 0:
            namefile = selectfile[0].text()
            print(files.folder_files()+namefile)
            self.player=VideoPlayer(files.folder_files()+"\\"+namefile)
            self.player.l=self.video

    def play(self):
        self.close()
        self.t1=threading.Thread(target=self.videoplayer)
        self.t1.start()

    def pause(self):self.player.player.toggle_pause()

    def close(self):
        try:
            self.player.close=True
            time.sleep(1)
        except:pass

    def closeEvent(self, event):
        try:
            self.player.close=True
            time.sleep(1)
        except:pass

    def joinClicked(self):
        print("Click Join")
        global currentPassword, currentUsername
        username = self.usernameTextEdit.text()
        password = self.passwordTextEdit.text()
        if database.isAccountExists(username, password) == True:
            self.detailsWongLabel.setHidden(True)
            self.listFiles.addItems(files.listVideos())
            #self.welcomeLabel.setText("Bem vindo " + username)
            currentUsername = username
            currentPassword = password
            for label in self.joinWinLabels:
                label.setHidden(True)
            for label in self.welcomeWinLabels:
                label.setHidden(False)
            self.goToJoinButton.setGeometry(QtCore.QRect(460, 470, 111, 31))
        else:
            print("login False")
            self.detailsWongLabel.setHidden(False)
        self.usernameTextEdit.setText("")
        self.passwordTextEdit.setText("")

    def goToCreateClicked(self):
        self.usernameTextEdit.setText("")
        self.passwordTextEdit.setText("")
        for label in self.joinWinLabels:
            label.setHidden(True)
        for label in self.createWinLabels:
            if label == self.accountCreatedLabel or label == self.accountAlreadyExistsLabel:
                label.setHidden(True)
            else:
                label.setHidden(False)

    def goToJoinClicked(self):
        self.usernameTextEdit.setText("")
        self.passwordTextEdit.setText("")
        for label in self.createWinLabels:
            label.setHidden(True)
        for label in self.joinWinLabels:
            if label != self.detailsWongLabel:
                label.setHidden(False)
        for label in self.welcomeWinLabels:
            label.setHidden(True)
        self.goToJoinButton.setGeometry(QtCore.QRect(510, 470, 111, 31))

    def createAccountClicked(self):
        un = self.usernameTextEdit.text()
        pw = self.passwordTextEdit.text()
        isAccountCreated = database.createAccount(un, pw)
        if isAccountCreated == "Username Exists":
            self.accountAlreadyExistsLabel.setHidden(False)
        else:
            self.accountCreatedLabel.setHidden(False)
        self.usernameTextEdit.setText("")
        self.passwordTextEdit.setText("")

    def deleteAccount(self):
        msg = QMessageBox()
        msg.setWindowTitle("delete account")
        msg.setText("are you sure you want to delete the account?")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        msg.buttonClicked.connect(self.confirmDelete)
        x = msg.exec_()

    def confirmDelete(self, i):
        if i.text() == "&Yes":
            database.deleteAccount(currentUsername, currentPassword)
            self.goToJoinClicked()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
