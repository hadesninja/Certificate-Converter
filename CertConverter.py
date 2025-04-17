import sys
import os
import hashlib

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QTextEdit, QLabel, QLineEdit,
    QMessageBox, QMainWindow, QAction, QMenuBar
)
from OpenSSL import crypto

class CertConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Certificate Converter (.der to .0)")
        self.setGeometry(300, 200, 650, 420)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # File path entry
        self.label = QLabel("DER Certificate File:")
        self.layout.addWidget(self.label)

        self.file_path_entry = QLineEdit()
        self.file_path_entry.setReadOnly(True)
        self.layout.addWidget(self.file_path_entry)

        self.browse_button = QPushButton("Browse .der File")
        self.browse_button.clicked.connect(self.browse_file)
        self.layout.addWidget(self.browse_button)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.layout.addWidget(self.log_output)

        # Menu Bar
        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help Menu
        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_about(self):
        QMessageBox.information(self, "About", "Version: 1.0\nDeveloper: Vaibhav Pail")

    def log(self, message):
        self.log_output.append(message)
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    def show_popup(self, message):
        msg = QMessageBox()
        msg.setWindowTitle("Conversion Complete")
        msg.setText(message)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select DER Certificate", "", "DER Files (*.der)")
        if file_path:
            self.file_path_entry.setText(file_path)
            self.convert_cert(file_path)

    def convert_cert(self, der_path):
        self.log_output.clear()
        self.log(f"Loading .der file: {der_path}")
        try:
            with open(der_path, "rb") as f:
                der_data = f.read()
            cert = crypto.load_certificate(crypto.FILETYPE_ASN1, der_data)
        except Exception as e:
            self.log(f"Error loading DER certificate: {e}")
            return

        # Convert to PEM
        try:
            pem_data = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
            pem_path = der_path.replace(".der", ".pem")
            with open(pem_path, "wb") as f:
                f.write(pem_data)
            self.log(f"Converted to PEM: {pem_path}")
        except Exception as e:
            self.log(f"Error writing PEM file: {e}")
            return

        # Generate subject_hash_old
        try:
            subject_der = cert.get_subject().der()
            md5_hash = hashlib.md5(subject_der).digest()
            hash_int = int.from_bytes(md5_hash[:4], byteorder='little')
            subject_hash_old = "{:08x}".format(hash_int)
            self.log(f"Subject Hash (old): {subject_hash_old}")
        except Exception as e:
            self.log(f"Error generating subject_hash_old: {e}")
            return

        # Rename PEM to .0 file
        try:
            final_path = os.path.join(os.path.dirname(pem_path), subject_hash_old + ".0")
            os.rename(pem_path, final_path)
            self.log(f"Renamed {pem_path} to {final_path}")
            self.log("Certificate converted and saved successfully.")
            self.show_popup(f"Certificate successfully converted!\nSaved as:\n{final_path}")
        except Exception as e:
            self.log(f"Error renaming file: {e}")
            return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('images.ico'))
    window = CertConverter()
    window.show()
    sys.exit(app.exec_())
