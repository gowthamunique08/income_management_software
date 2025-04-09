from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit, QComboBox,
    QDateEdit, QTableWidget, QVBoxLayout, QMessageBox,
    QTableWidgetItem, QHeaderView, QHBoxLayout, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QIcon, QColor
from database import fetch_expenses, add_expenses, delete_expenses


class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.load_table_data()
        self.apply_styles()

    def settings(self):
        self.setGeometry(750, 300, 550, 500)
        self.setWindowTitle("ZOHO INCOME MANAGEMENT")

    def initUI(self):
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()

        self.btn_add = QPushButton("Add Expense")
        self.btn_add.setObjectName("btn_add")
        self.btn_add.setIcon(QIcon("icons/add.png"))
        self.apply_shadow(self.btn_add, "#27ae60")

        self.btn_delete = QPushButton("Delete Expense")
        self.btn_delete.setObjectName("btn_delete")
        self.btn_delete.setIcon(QIcon("icons/delete.png"))
        self.apply_shadow(self.btn_delete, "#c0392b")

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Category", "Amount", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.populate_dropdown()
        self.btn_add.clicked.connect(self.add_expense)
        self.btn_delete.clicked.connect(self.delete_expense)
        self.setup_layout()

    def setup_layout(self):
        master = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()

        row1.addWidget(QLabel("Date"))
        row1.addWidget(self.date_box)
        row1.addWidget(QLabel("Category"))
        row1.addWidget(self.dropdown)

        row2.addWidget(QLabel("Amount"))
        row2.addWidget(self.amount)
        row2.addWidget(QLabel("Description"))
        row2.addWidget(self.description)
        row2.addWidget(self.btn_add)
        row2.addWidget(self.btn_delete)

        master.addLayout(row1)
        master.addLayout(row2)
        master.addWidget(self.table)

        self.setLayout(master)

    def populate_dropdown(self):
        categories = ["GST", "other Taxes", "Food", "Rent", "Bills", "Entertainment", "Shopping", "Other"]
        self.dropdown.addItems(categories)

    def load_table_data(self):
        expenses = fetch_expenses()
        self.table.setRowCount(0)
        for row_idx, expense in enumerate(expenses):
            self.table.insertRow(row_idx)
            for col_idx, data in enumerate(expense):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    def clear_inputs(self):
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

    def add_expense(self):
        date = self.date_box.date().toString("yyyy-MM-dd")  # Correct usage for QDateEdit
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()

        if not amount or not description:
            QMessageBox.warning(self, "Input Error", "Amount and Description cannot be empty")
            return

        if add_expenses(date, category, amount, description):
            self.load_table_data()
            self.clear_inputs()
        else:
            QMessageBox.critical(self, "Error", "Failed to add expense")

    def delete_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Uh oh", "You need to choose a row to delete.")
            return

        expense_id = int(self.table.item(selected_row, 0).text())
        confirm = QMessageBox.question(
            self, "Confirm", "Are you sure you want to delete?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes and delete_expenses(expense_id):
            self.load_table_data()

    def apply_shadow(self, widget, color="#000000", blur=20):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blur)
        shadow.setOffset(0)
        shadow.setColor(QColor(color))
        widget.setGraphicsEffect(shadow)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #e3e9f2;
                font-family: Arial, sans-serif;
                font-size: 14px;
                color: #333;
            }

            QLabel {
                font-size: 16px;
                color: #2c3e50;
                font-weight: bold;
                padding: 5px;
            }

            QLineEdit, QComboBox, QDateEdit {
                background-color: #fff;
                font-size: 14px;
                color: #333;
                border: 1px solid #b0bfc6;
                border-radius: 15px;
                padding: 5px;
            }

            QLineEdit:hover, QComboBox:hover, QDateEdit:hover {
                border: 1px solid #4caf50;
                background-color: #f5f9fc;
            }

            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 1px solid #2a9d8f;
                background-color: #f5f9fc;
            }

            QTableWidget {
                background-color: #fff;
                alternate-background-color: #f2f7fb;
                gridline-color: #c0c9d0;
                selection-background-color: #4caf50;
                selection-color: white;
                font-size: 14px;
                border: 1px solid #cfd9e1;
            }

            QPushButton {
                background-color: #2a9d8f;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 6px 12px;
                font-weight: bold;
            }

            QPushButton#btn_add {
                background-color: #27ae60;
            }

            QPushButton#btn_add:hover {
                background-color: #2ecc71;
                padding: 7px 13px;
            }

            QPushButton#btn_delete {
                background-color: #c0392b;
            }

            QPushButton#btn_delete:hover {
                background-color: #e74c3c;
                padding: 7px 13px;
            }
        """)
