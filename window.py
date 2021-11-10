import socket
import sys
import json

from PyQt5.QtWidgets import QFileDialog

import mainWindow
from PyQt5 import QtWidgets
import searcher
from Help import Help
from AddIP import AddIP


class SearchWindow(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_search.clicked.connect(self.btn_search_clicked)
        with open('./local_ips.json') as file:
            self.comboBox_ip.addItems(json.load(file).get('ips'))
        self.comboBox_ip.currentIndexChanged.connect(self.item_changed)
        self.folder_path = ''
        self.search_string = ''
        self.actionhelp.triggered.connect(self.help_clicked)
        # self.btn_add_ip.clicked.connect(self.add_clicked)
        self.btn_add_ip.clicked.connect(self.openFileNameDialog)
        self.host = 'localhost'
        # self.sock = socket.socket()
        # self.sock.connect((self.host, 9090))

    def item_changed(self, i):
        if self.comboBox_ip.currentText():
            self.host = self.comboBox_ip.currentText()
            try:
                self.sock.close()
                self.sock.connect((self.host, 9090))
                self.plainTextEdit_result.insertPlainText(f'connected to: {self.comboBox_ip.currentText()}\n*****\n')
            except Exception as e:
                self.plainTextEdit_result.insertPlainText(f'cant connect to: {self.comboBox_ip.currentText()}\n*****\n')
                print(e)

    def btn_search_clicked(self):
        try:
            # self.sock.connect((self.comboBox_ip.currentText(), 9090))
            search_str = self.textEdit_search.toPlainText()
            size = sys.getsizeof(search_str)
            print(size)
            size_bytes = size.to_bytes(2, byteorder='big')
            r1 = self.sock.send(size_bytes)
            print(r1)
            r2 = self.sock.send(bytes(search_str, 'utf-8'))
            print(r2)
            size = int.from_bytes(self.sock.recv(8), 'big')
            data = self.sock.recv(size)
            print(data.decode(encoding='utf-8'))
            # self.sock.close()
        except Exception as e:
            self.plainTextEdit_result.insertPlainText(f'cant connect to: {self.comboBox_ip.currentText()}\n*****\n')
            print(e)

    def help_clicked(self):
        dial = Help(self)
        dial.show()

    def add_clicked(self):
        add_dial = AddIP(self)
        add_dial.show()

    def openFileNameDialog(self):
        folder_path = QFileDialog.getExistingDirectory(self)
        if fileName:
            print(fileName)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = SearchWindow()
    window.show()
    app.exec()
