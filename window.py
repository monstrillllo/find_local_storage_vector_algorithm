import mainWindow
from PyQt5 import QtWidgets
import searcher
from Help import Help


class SearchWindow(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_search.clicked.connect(self.btn_search_clicked)
        self.folder_path = ''
        self.search_string = ''
        self.actionhelp.triggered.connect(self.help_clicked)

    def btn_search_clicked(self):
        if not self.textEdit_search.toPlainText():
            return
        self.folder_path = self.textEdit_folder.toPlainText().strip().lower()
        self.search_string = self.textEdit_search.toPlainText().strip().lower()
        result = searcher.main(self.folder_path, self.search_string)
        for file in result:
            if file.eq_rate == 0:
                break
            self.plainTextEdit_result.insertPlainText(f'file path: {file.path}\nrating: {file.eq_rate}\n'
                                                      f'words from search string: {file.words_from_search}\n*****\n')

    def help_clicked(self):
        dial = Help(self)
        # dial.setupUi(dial)
        dial.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = SearchWindow()
    window.show()
    app.exec()
