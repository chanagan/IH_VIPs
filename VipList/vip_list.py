import sys
import time
from dataclasses import dataclass
from datetime import date
from itertools import chain
from typing import Callable, Any

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QTableWidgetItem, QTableWidget, QApplication, QFileDialog


from VipList.get_reservations import get_reservations
from VipList.get_rooms import get_rooms
from VipList.UI.vip_list import Ui_wgt_vip_list
from VipList.export_to_excel import qtablewidget_to_xlsx


def parse_iso_date(s: str) -> date:
    return date.fromisoformat(s)


def make_item(text: str, user_value: Any, alignment=None) -> QTableWidgetItem:
    it = QTableWidgetItem(text)
    if user_value is not None:
        it.setData(Qt.UserRole, user_value)
    if alignment is not None:
        it.setTextAlignment(int(alignment))
    return it


@dataclass(frozen=True)
class ColSpec:
    element: str
    header: str
    width: int
    display: Callable[[dict], str]
    userrole: Callable[[dict], Any]
    align: Qt.AlignmentFlag | None = None


resColumns = [
    ColSpec(
        element="reservationID",
        header="Res ID",
        width=130,
        display=lambda x: str(x["reservationID"]),
        userrole=lambda x: str(x["reservationID"]),
    ),
    ColSpec(
        element="guestName",
        header="Guest Name",
        width=150,
        display=lambda x: x["guestName"],
        userrole=lambda x: x["guestName"],
    ),
    ColSpec(
        element="nights",
        header="Days",
        width=40,
        display=lambda x: str(x["nights"]),
        userrole=lambda x: x["nights"],
        align=Qt.AlignmentFlag.AlignCenter,
    ),
    ColSpec(
        element="startDate",
        header="Check In",
        width=100,
        display=lambda x: str(x["startDate"]),
        userrole=lambda x: parse_iso_date(x["startDate"]),
        align=Qt.AlignmentFlag.AlignCenter,
    ),
    ColSpec(
        element="dow",
        header="DoW",
        width=50,
        display=lambda x: x["dow"],
        userrole=lambda x: x["dow"],
        align=Qt.AlignmentFlag.AlignCenter,
    ),
    ColSpec(
        element="adults",
        header="#",
        width=30,
        display=lambda x: x["adults"],
        userrole=lambda x: int(x["adults"]),
        align=Qt.AlignmentFlag.AlignCenter,
    ),
]

gstColumns = [
    ColSpec(
        element="guestID",
        header="Guest ID",
        width=90,
        display=lambda x: str(x["guestID"]),
        userrole=lambda x: x["guestID"],
    ),
    ColSpec(
        element="guestLastName",
        header="Last",
        width=100,
        display=lambda x: x["guestLastName"],
        userrole=lambda x: x["guestLastName"],
    ),
    ColSpec(
        element="guestFirstName",
        header="First",
        width=100,
        display=lambda x: str(x["guestFirstName"]),
        userrole=lambda x: x["guestFirstName"],
    ),
    # ColSpec(
    #     element="isMainGuest",
    #     header="Main",
    #     width=40,
    #     display=lambda x: str(x["isMainGuest"]),
    #     userrole=lambda x: str(x["isMainGuest"]),
    # ),
]

roomColumns = [
    ColSpec(
        element="roomName",
        header="Room",
        width=80,
        display=lambda x: x["roomName"],
        userrole=lambda x: x["roomName"],
        align=Qt.AlignmentFlag.AlignCenter,
    ),
    ColSpec(
        element="startDate",
        header="Date",
        width=100,
        display=lambda x: x["startDate"],
        userrole=lambda x: parse_iso_date(x["startDate"]),
        align=Qt.AlignmentFlag.AlignCenter,
    ),
]


class VipList(QTableWidget, Ui_wgt_vip_list):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # this the default list
        self.reservations = []
        # print (self.reservations)
        self.guestRooms = []
        # print (self.guestRooms)

        # Create font object
        font = QFont("Trebuchet MS", 14)
        font.setFixedPitch(True)  # Ensure it is recognized as fixed pitch
        self.setFont(font)

        totalWidth = 0

        allColumns = chain(resColumns, gstColumns, roomColumns)
        colCount = 0
        for colIdx, c in enumerate(allColumns):
            self.tbl_vip_list.setColumnWidth(colIdx, c.width)
            totalWidth += c.width
            colCount += 1

        self.tbl_vip_list.setColumnCount(colCount)

        print("total pixels: ", totalWidth)

        self.tbl_vip_list.horizontalHeader().setFont(font)
        self.tbl_vip_list.setHorizontalHeaderLabels(
            [r.header for r in chain(resColumns, gstColumns, roomColumns)]
        )

    @Slot(str, str)
    def perform_search(self, from_date, to_date):
        print('from: ', from_date, ' to: ', to_date)
        self.get_reserveGuests(from_date, to_date)
        self.show_reservations()

    @Slot()
    def dump_to_excel(self):
        print('dump to excel')

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export to Excel",
            "reservations.xlsx",
            "Excel files (*.xlsx)"
        )
        if path:
            qtablewidget_to_xlsx(self.tbl_vip_list, path, sheet_name="Reservations")

    def get_reserveGuests(self, from_date, to_date):
        # this the default list
        start = time.perf_counter()
        self.reservations = get_reservations(from_date, to_date)
        # print (self.reservations)
        end = time.perf_counter()
        print(f"self.reservations: {end - start:.3f} seconds")

        start = time.perf_counter()
        self.guestRooms = get_rooms(self.reservations)
        end = time.perf_counter()
        print(f"self.guestRooms: {end - start:.3f} seconds")

        # print (self.guestRooms)

    def show_reservations(self):
        # start with an empty table
        print(len(self.reservations))

        self.tbl_vip_list.clearContents()

        tableLength = len(self.reservations) * 2
        self.tbl_vip_list.setRowCount(tableLength)

        rowIdx = 1
        table = self.tbl_vip_list
        for row in self.reservations:
            offsetColumn = 0
            for col_idx, spec in enumerate(resColumns):
                text = spec.display(row)
                user_val = spec.userrole(row)
                item = make_item(text, user_val, alignment=spec.align)
                table.setItem(rowIdx, col_idx, item)

            thisRow = rowIdx
            offsetColumn += len(resColumns)
            for guest in row['guests']:
                for col_idx, spec in enumerate(gstColumns):
                    gCol = offsetColumn + col_idx
                    text = spec.display(guest)
                    user_val = spec.userrole(guest)
                    item = make_item(text, user_val, alignment=spec.align)
                    table.setItem(thisRow, gCol, item)
                thisRow += 1
                # print(guest)
            guestCount = thisRow

            thisRow = rowIdx
            offsetColumn += len(gstColumns)
            for room in row['rooms']:
                for col_idx, spec in enumerate(roomColumns):
                    pCol = offsetColumn + col_idx
                    text = spec.display(room)
                    user_val = spec.userrole(room)
                    item = make_item(text, user_val, alignment=spec.align)
                    table.setItem(thisRow, pCol, item)
                thisRow += 1
                # print(room)
            roomCount = thisRow

            rowIdx = max(guestCount, roomCount)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = VipList()
    form.setWindowTitle(f"Giant Horse Cock - closed")
    form.show()
    sys.exit(app.exec())
