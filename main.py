import cv2
import sys
import os
import csv
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QApplication, QMessageBox, QHBoxLayout, QComboBox, QTextEdit, QMainWindow, QFileDialog
from PyQt5.QtGui import QImage, QPixmap, QIcon, QDesktopServices
from PyQt5.QtCore import QUrl, Qt 
from simple_facerec import SimpleFacerec
from view_records_window import ViewRecordsWindow
from database import create_database, insert_data_to_database

# e encode ang mga nawong sa folders
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

class FormWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create form fields
        self.name_label = QLabel("Name:", self)
        self.name_field = QLineEdit(self)

        self.gender_label = QLabel("Gender:", self)
        self.gender_field = QComboBox(self)
        self.gender_field.addItems(["", "Male", "Female"])

        self.alleged_offense_label = QLabel("Alleged Offense:", self)
        self.alleged_offense_field = QTextEdit(self)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit_form)

        # Create a vertical layout for the form
        self.form_layout = QVBoxLayout()

        # Add form fields to the layout
        self.form_layout.addWidget(self.name_label)
        self.form_layout.addWidget(self.name_field)
        self.form_layout.addWidget(self.gender_label)
        self.form_layout.addWidget(self.gender_field)
        self.form_layout.addWidget(self.alleged_offense_label)
        self.form_layout.addWidget(self.alleged_offense_field)
        self.form_layout.addWidget(self.submit_button)

        # Set the form layout as the main layout of the form window
        self.setLayout(self.form_layout)

    def submit_form(self):
        # Get the values of the form fields
        name = self.name_field.text()
        gender = self.gender_field.currentText()
        alleged_offense = self.alleged_offense_field.toPlainText()

        # Insert the data into the database
        insert_data_to_database(name, gender, alleged_offense)

        # Confirm the data was saved
        QMessageBox.information(self, "Data Saved", "Data was saved to the database")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Create database
        create_database()

        # Create form window
        self.form_window = FormWindow()

        # Create view records window
        self.view_records_window = ViewRecordsWindow()

        # Create a button to open the view records window
        self.view_records_button = QPushButton("View Criminal Records", self)
        self.view_records_button.move(20, 80)
        self.view_records_button.clicked.connect(self.open_view_records)
        # Create a label to display the video feed
        self.label = QLabel(self)
        self.label.setGeometry(QtCore.QRect(10, 10, 480, 360))

        # Create a horizontal layout for the buttons
        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignCenter)

        # Submit Image button
        self.open_folder_button = QPushButton('Submit Image', self)
        self.open_folder_button.clicked.connect(self.open_folder)
        self.button_layout.addWidget(self.open_folder_button)

        # Submit Criminal Records button
        self.open_form_button = QPushButton('Submit Criminal Records', self)
        self.open_form_button.clicked.connect(self.open_form)
        self.button_layout.addWidget(self.open_form_button)

        # View Criminal Records Button
        self.view_records_button = QPushButton('View Criminal Records', self)
        self.view_records_button.clicked.connect(self.open_view_records)
        self.button_layout.addWidget(self.view_records_button)

        # Create a vertical layout for the main window
        self.main_layout = QVBoxLayout()

        # Add the video feed label and the horizontal layout to the main layout
        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(self.button_layout)

        # Set the main layout as the central layout of the main window
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # Load Camera
        self.cap = cv2.VideoCapture(0)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

        # Create a label to display the logo
        self.logo_label = QLabel(self)
        self.logo_label.setGeometry(QtCore.QRect(self.width() - 110, 10, 100, 100))
        self.logo_label.setAlignment(QtCore.Qt.AlignRight)

        # Load the logo image
        logo_image = QPixmap("logo/logo.png")
        self.logo_label.setPixmap(logo_image)

        # Make the logo label transparent
        self.logo_label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    def open_view_records(self):
        self.view_records_window.show()

    def open_view_records(self):
        self.view_records_window = ViewRecordsWindow()
        self.view_records_window.show()
    #open submit criminal records button
    def open_form(self):
        # Function to be called when submit criminal records button is clicked
        self.form_window.show()
    #Submit Images Button
    def open_folder(self):
        # Function to be called when open folder button is clicked
        folder_path = QUrl.fromLocalFile('C://Users//user//Desktop//face_recog//images')
        QDesktopServices.openUrl(folder_path)

    def update_frame(self):
        ret, frame = self.cap.read()
        self.setWindowTitle("Image Processing for Wanted Criminals")
        icon = QIcon("icon/icon.png")  # Load the icon image
        self.setWindowIcon(icon)

        # Create a label to display the video feed
        self.label = QLabel(self)
        self.label.setGeometry(QtCore.QRect(10, 10, 480, 360))

        # Load Camera
        self.cap = cv2.VideoCapture(0)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)
        #Submit Image button
        self.open_folder_button = QPushButton('Submit Image', self)
        self.open_folder_button.setGeometry(QtCore.QRect(10, 380, 100, 30))
        self.open_folder_button.clicked.connect(self.open_folder)
        # Create a label to display the logo
        self.logo_label = QLabel(self)
        self.logo_label.setGeometry(QtCore.QRect(self.width() - 110, 10, 100, 100))
        self.logo_label.setAlignment(QtCore.Qt.AlignRight)
        # Load the logo image
        logo_image = QPixmap("logo/logo.png")
        self.logo_label.setPixmap(logo_image)

        # Make the logo label transparent
        self.logo_label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    #SUBMIT IMAGES BUTTON CONNECT
    def open_folder(self):
        # Function to be called when open folder button is clicked
        folder_path = QUrl.fromLocalFile('C://Users//user//Desktop//face_recog//images')
        QDesktopServices.openUrl(folder_path)

    def update_frame(self):
        ret, frame = self.cap.read()
        self.setWindowTitle("Image Processing for Wanted Criminals")
        icon = QIcon("icon/icon.png")  # Load the icon image
        self.setWindowIcon(icon)

        # Detect Faces
        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        # Convert the frame to a QImage and set it to the label
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        qImg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        self.label.setPixmap(QPixmap.fromImage(qImg))

    def closeEvent(self, event):
        self.cap.release()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create widgets
        self.username_label = QLabel("Username:")
        self.username_edit = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.login_button)
        layout.addWidget(self.cancel_button)
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon("icon/icon.png"))

    def login(self):
        # Check if the username and password are correct
        if self.username_edit.text() == "admin" and self.password_edit.text() == "123":
            # If correct, show the main window
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            # If incorrect, show an error message
            QMessageBox.warning(self, "Error", "Incorrect username or password.")

    def cancel(self):
        # Close the login window
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
