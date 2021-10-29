import socket
import sys
import json
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
        self.folder_path = ''
        self.search_string = ''
        self.actionhelp.triggered.connect(self.help_clicked)
        self.btn_add_ip.clicked.connect(self.add_clicked)

    def btn_search_clicked(self):
        try:
            sock = socket.socket()
            sock.connect((self.comboBox_ip.currentText(), 9099))
            search_str = self.textEdit_search.toPlainText()
            size = sys.getsizeof(search_str)
            print(size)
            size_bytes = bytes([size])
            sock.send(size_bytes)
            sock.send(bytes(search_str, 'utf-8'))
            size = int.from_bytes(sock.recv(8), 'little')
            data = sock.recv(size)
            print(data.decode(encoding='utf-8'))
            sock.close()
        except Exception as e:
            self.plainTextEdit_result.insertPlainText(f'cant connect to: {self.comboBox_ip.currentText()}\n*****\n')
            print(e)

    def help_clicked(self):
        dial = Help(self)
        dial.show()

    def add_clicked(self):
        add_dial = AddIP(self)
        add_dial.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = SearchWindow()
    window.show()
    app.exec()
