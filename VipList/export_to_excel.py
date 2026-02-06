from pathlib import Path
from PySide6.QtWidgets import QTableWidget
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter
from PySide6.QtCore import Qt

def qtablewidget_to_xlsx(
    table: QTableWidget,
    filepath: str | Path,
    sheet_name: str = "Sheet1"
) -> None:
    filepath = str(filepath)

    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name

    rows = table.rowCount()
    cols = table.columnCount()

    # ---- headers ----
    for c in range(cols):
        header_item = table.horizontalHeaderItem(c)
        ws.cell(row=1, column=c + 1).value = (
            header_item.text() if header_item else ""
        )
        ws.cell(row=1, column=c +1).font = Font(bold=True)
    # row = ws.row_dimensions[rows]
    # col = ws.column_dimensions[cols]
    # for r in range(1, rows + 1):
    #     for c in range(1, cols + 1):
    #         ws[r,c].alignment = Alignment(horizontal="center", vertical="center")
    #         ws[r,c].font = Font(bold=True)


    # ---- data ----
    for r in range(rows):
        for c in range(cols):
            item = table.item(r, c)
            ws.cell(row=r + 2, column=c + 1).value = cell_value(item)

    # ---- autosize columns (approx) ----
    for c in range(1, cols + 1):
        max_len = 0
        for r in range(1, rows + 2):
            v = ws.cell(row=r, column=c).value
            if v is not None:
                max_len = max(max_len, len(str(v)))
        ws.column_dimensions[get_column_letter(c)].width = min(max_len + 2, 60)

    # Optional Excel niceties
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions

    wb.save(filepath)


def cell_value(item):
    if item is None:
        return ""
    # Prefer raw value if you stored one
    raw = item.data(Qt.UserRole)
    return raw if raw is not None else item.text()