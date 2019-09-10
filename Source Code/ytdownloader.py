# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from requests import get
from pytube import YouTube

class mythread(QThread):
    progressvalue = pyqtSignal(int)
    labeltext = pyqtSignal(str)
    def checker(self):
        try:
            re = get(ui.geturl(), stream=True)
            if re.ok == True and ui.getfilename() != "":
                return True
            else:
                return False
        except:
            return False

    def run(self):
        if self.checker() == True:
            self.downloader()
        else:
            self.labeltext.emit("Enter a valid url\n and filename")


    def downloader(self):
        self.labeltext.emit("Starting")
        yt = YouTube(ui.geturl())
        url = yt.streams.first().url
        r = get(url, stream=True)
        total_length = int(r.headers.get('content-length'))
        if total_length != 0:
            with open(ui.getfilename() + ".mp4", 'wb') as f:
                self.labeltext.emit(str(total_length/1000000) + "mb")
                chunksize = round(total_length/100)
                x = 0
                for chunk in r.iter_content(chunksize):
                    f.write(chunk)
                    x += 1
                    self.progressvalue.emit(x)
                self.labeltext.emit("Done!")
        else:
            self.labeltext.emit("Cannot download\nthis video. Sorry!")



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("YouTube Downloader")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.urlinput = QtWidgets.QLineEdit(self.centralwidget)        #LineEdit input box for URL
        self.urlinput.setGeometry(QtCore.QRect(145, 200, 471, 31))
        self.urlinput.setObjectName("urlinput")


        self.filename = QtWidgets.QLineEdit(self.centralwidget)        #LineEdit input box for filename
        self.filename.setGeometry(QtCore.QRect(145, 250, 471, 31))
        self.filename.setObjectName("filename")


        self.urllabel = QtWidgets.QLabel(self.centralwidget)
        self.urllabel.setGeometry(QtCore.QRect(80, 210, 47, 13))      #Label for URL input
        font = QtGui.QFont()
        font.setPointSize(12)
        self.urllabel.setFont(font)
        self.urllabel.setObjectName("urllabel")

        self.filenamelabel = QtWidgets.QLabel(self.centralwidget)
        self.filenamelabel.setGeometry(QtCore.QRect(50, 260, 90, 13))      #Label for filename input
        font = QtGui.QFont()
        font.setPointSize(12)
        self.filenamelabel.setFont(font)
        self.filenamelabel.setObjectName("filenamelabel")




        self.progress = QtWidgets.QLabel(self.centralwidget)
        self.progress.setGeometry(QtCore.QRect(340, 450, 118, 23))      #Label for text
        self.progress.setText("")
        self.progress.setObjectName("progress")

        self.size = QtWidgets.QLabel(self.centralwidget)
        self.size.setGeometry(QtCore.QRect(350, 400, 118, 23))      #Label for size
        self.size.setText("")
        self.size.setObjectName("progress")


        self.submit = QtWidgets.QPushButton(self.centralwidget)    #submit button
        self.submit.setGeometry(QtCore.QRect(650, 200, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.submit.setFont(font)
        self.submit.setObjectName("submit")


        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)   #progress bar
        self.progressBar.setGeometry(QtCore.QRect(330, 350, 118, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.msg = QtWidgets.QMessageBox()
        self.msg.setWindowTitle("Info")


        self.submit.clicked.connect(self.startthread)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.urllabel.setText(_translate("MainWindow", "URL"))
        self.filenamelabel.setText(_translate("MainWindow", "Filename"))
        self.submit.setText(_translate("MainWindow", "go"))


    def geturl(self):

        return self.urlinput.text()

    def getfilename(self):
        self.filenametext = self.filename.text()
        return self.filenametext


    def checker(self):
        try:
            self.re = get(self.geturl(), stream=True)
            if self.re.ok == True and self.getfilename() != "":
                return True
            else:
                return False
        except:
            return False

    def startthread(self):
        self.thread = mythread()
        self.thread.progressvalue.connect(self.progresser)
        self.thread.labeltext.connect(self.labeltextsetter)
        self.thread.start()

    def progresser(self, val):
        self.progressBar.setValue(val)


    def labeltextsetter(self, infotext):
        self.progress.setText(infotext)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()



