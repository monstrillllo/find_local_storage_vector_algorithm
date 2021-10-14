from PyQt5 import QtWidgets
import HelpWindow


class Help(QtWidgets.QDialog, HelpWindow.Ui_Dialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.textBrowserHelp.setText("""
        Folder path - a string for selecting a folder with documents 
        Search string - search query string
        Work algorithm: 
        1. Enter relative path to folder with documents 
        2. Enter a search query 
        3. Press button
        4. A list of documents relevant to the query will be displayed. 
        """)
