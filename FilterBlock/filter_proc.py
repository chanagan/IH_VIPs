import datetime
import sys

import qtawesome as qa

from PySide6.QtCore import Qt, Signal, QDate, Slot
from PySide6.QtGui import QIcon
# from PySide6.QtGui import QColor, QFont, QIcon
from PySide6.QtWidgets import QWidget, QApplication, QGridLayout, QButtonGroup

from FilterBlock.UI.filter import Ui_Filter


class Filter(QWidget, Ui_Filter):
    # status_changed = Signal(bool, bool)
    # acct_type_changed = Signal(str)
    searchRequested = Signal(str, str)
    excelRequested = Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.de_fromDate.setDate(QDate.currentDate())
        self.de_toDate.setDate(QDate.currentDate())
        searchIcon = qa.icon('mdi.database-search')
        excelIcon = qa.icon('fa5.file-excel')
        self.pb_findVips.setIcon(searchIcon)
        self.pb_toExcel.setIcon(excelIcon)

        self.pb_findVips.clicked.connect(self.search_button_clicked)
        self.pb_toExcel.clicked.connect(self.excel_button_clicked)
    @Slot()
    def search_button_clicked(self):
        fromDate = self.de_fromDate.dateTime().toString("yyyy-MM-dd")
        toDate = self.de_toDate.dateTime().toString("yyyy-MM-dd")
        print ('filter: fromDate: ', fromDate, 'toDate: ', toDate)
        self.searchRequested.emit(fromDate, toDate)

    @Slot()
    def excel_button_clicked(self):
        self.excelRequested.emit()

    # def account_type_changed(self):
    #     new_account_type =


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Filter()
    form.setWindowTitle(f"Giant Horse Cock - closed")
    form.show()
    sys.exit(app.exec())
