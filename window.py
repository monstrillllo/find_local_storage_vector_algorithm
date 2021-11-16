from PyQt5.QtWidgets import QFileDialog
import mainWindow
from PyQt5 import QtWidgets
import searcher
from Help import Help


class SearchWindow(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_search.clicked.connect(self.btn_search_clicked)
        self.btn_choose_folder.clicked.connect(self.open_file_name_dialog)
        self.folder_path = ''
        self.search_string = ''
        self.actionhelp.triggered.connect(self.help_clicked)

    def btn_search_clicked(self):
        self.search_string = self.textEdit_search.toPlainText()
        if not self.search_string or not self.folder_path:
            self.plainTextEdit_result.appendPlainText('First enter search string and choose folder!\n')
            return
        files = searcher.get_files_list(searcher.get_folders_content(self.folder_path))
        searcher.eq_rating(files, self.search_string)
        files.sort(key=searcher.sort_key, reverse=True)
        self.plainTextEdit_result.appendPlainText(f'Files suitable for the query "{self.search_string}":\n')
        for file in files:
            if file.eq_rate > 0:
                self.plainTextEdit_result.appendPlainText(f'{file.path} - equivalence rating {file.eq_rate}\n')

    def help_clicked(self):
        dial = Help(self)
        dial.show()

    def open_file_name_dialog(self):
        self.folder_path = QFileDialog.getExistingDirectory(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = SearchWindow()
    window.show()
    app.exec()
