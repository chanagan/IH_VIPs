import cProfile
import sys
'''“We talked yesterday about using Qt.UserRole 
for LOS and auto-populating a QTableWidget from 
an API payload.”
'''
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QTableWidget, QApplication, QMainWindow, QGridLayout, \
    QVBoxLayout

from Main.UI.main import Ui_MainWindow
from FilterBlock.filter_proc import Filter
from VipList.vip_list import VipList

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(1200, 800)
        self.setWindowTitle("HA Header")
        self.setWindowTitle("HA List")

        pg_header = Filter()
        pg_list = VipList()

        # ha_header.status_changed.connect(ha_list.process_status_changed)
        # ha_header.acct_type_changed.connect(ha_list.account_type_changed)

        # ha_header.cb_status_closed.clicked.connect(self.close)
        # ha_header.cb_status_open.clicked.connect(ha_list.show)

        layout = QVBoxLayout(self.centralwidget)
        # group_box_layout = QVBoxLayout()
        layout.addWidget(pg_header)
        layout.addWidget(pg_list)
        # group_box_layout.addWidget(self.ha_list)
        # self.gb_acct_list.addWidget(self.ha_list)  perform_search

        pg_header.searchRequested.connect(pg_list.perform_search)
        pg_header.excelRequested.connect(pg_list.dump_to_excel)

def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # profiler = cProfile.Profile()
    # profiler.enable()
    run_app()
    # profiler.disable()
    # profiler.dump_stats("~/Downloads/profiler.prof")
