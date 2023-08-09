import socket
import threading
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot

def received_text(server_ip, server_port, signal):
    while True:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_ip, server_port))
        server_socket.listen(1)
        client_socket, client_address = server_socket.accept()
        text = client_socket.recv(70).decode('utf-8')
        signal.emit(text)
    client_socket.close()
    server_socket.close()

ip_second_computer = ""
port = 1234
uni = '0.0.0.0'
text1 = ""

class MyGui(QMainWindow):
    message_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        uic.loadUi("mess.ui", self)
        self.show()
        self.setWindowTitle("Messenger")

        self.textEdit.setText("")  # Wyczyszczenie początkowej wartości
        self.message_received.connect(self.update_text_edit)
        self.pushButton.clicked.connect(self.change_data)

        self.thread = threading.Thread(target=received_text, args=(uni, port, self.message_received))
        self.thread.start()

    def update_text_edit(self, text):
        self.textEdit.append(text)  # Dodanie nowego tekstu do końca

    def change_data(self):
        global ip_second_computer
        ip_second_computer = self.textEdit_3.toPlainText()

        if self.textEdit_2.toPlainText() != "" and ip_second_computer != "":
            text1 = self.textEdit_2.toPlainText()
            self.textEdit.append(text1)
            self.textEdit_2.setText("")
            self.send_text(ip_second_computer, port, text1)

    def send_text(self, server_ip, server_port, n):
        text = n
        data = text.encode('utf-8')
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server_ip, server_port))
        client.sendall(data)
        client.close()


if __name__ == '__main__':
    app = QApplication([])
    window = MyGui()
    app.exec_()
