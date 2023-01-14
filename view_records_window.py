from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit
from database import fetch_all_records, update_data, delete_data

class ViewRecordsWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create a table widget to display the records
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Gender", "Alleged Offense"])
        #Button Layout for Update and Delete
        self.main_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()
        self.update_button = QPushButton('Update')
        self.update_button.clicked.connect(self.update_data)
        self.delete_button = QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete_data)
        self.button_layout.addWidget(self.update_button)
        self.button_layout.addWidget(self.delete_button)
        
        # Create a vertical layout for the window
        self.layout = QVBoxLayout()

        # Add the table to the layout
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        # Populate the table with the records
        records = fetch_all_records()
        self.populate_table(records)

    def delete_data(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            name = self.table.item(selected_row,0).text()
            delete_data(name)
            self.table.removeRow(selected_row)

    def update_data(self):
        selected_row = self.table.currentRow()
        name = self.table.item(selected_row, 0).text()
        gender = self.table.item(selected_row, 1).text()
        alleged_offense = self.table.item(selected_row, 2).text()
        update_data(name, gender, alleged_offense)

    def populate_table(self, records):
        # Clear any existing rows
        self.table.setRowCount(0)

        # Add the records to the table
        for i, record in enumerate(records):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(record[0]))
            self.table.setItem(i, 1, QTableWidgetItem(record[1]))
            self.table.setItem(i, 2, QTableWidgetItem(record[2]))
        self.layout.addLayout(self.button_layout) # add the button layout to the main layout

        
