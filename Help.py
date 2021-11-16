from PyQt5 import QtWidgets
import HelpWindow


class Help(QtWidgets.QDialog, HelpWindow.Ui_Dialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.textBrowserHelp.setText("""
        Search string - search query string
        Work algorithm: 
        1. Enter a search query 
        2. Press folder button and choose folder to search 
        3. Press search button
        4. A list of documents relevant to the query will be displayed. 
        """)
