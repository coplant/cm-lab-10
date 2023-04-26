import string
from enum import Enum

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from ui_mainwindow import Ui_MainWindow


class Application(QMainWindow):
    class Action(Enum):
        ENCRYPT = -1
        DECRYPT = 1

    def __init__(self):
        super(Application, self).__init__()
        self.data = None
        self.matrix = []
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        self.ui.btn_enc.setChecked(True)

        ru_abc = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        en_abc = "abcdefghijklmnopqrstuvwxyz"
        self.abc = [ru_abc, en_abc]

        self.ui.proc_button.clicked.connect(self.process_data)
        self.ui.open_file.triggered.connect(self.open)
        self.ui.save_file.triggered.connect(self.save)

    def process_data(self):
        self.data = self.ui.plain_text.toPlainText()
        try:
            if self.ui.btn_enc.isChecked():
                self.data = self.crypt_text(self.data, self.Action.ENCRYPT.value)
            elif self.ui.btn_dec.isChecked():
                self.data = self.crypt_text(self.data, self.Action.DECRYPT.value)
        except ValueError as e:
            ...
        self.ui.cipher_text.setText(str(self.data))

    def open(self):
        file_name = QFileDialog.getOpenFileName(self, "Открыть файл", ".", "All Files (*)")
        if file_name[0]:
            with open(file_name[0], "r") as file:
                self.data = file.read()
                self.ui.plain_text.setText(self.data)
        else:
            QMessageBox.information(self, "Ошибка", "Файл не выбран", QMessageBox.Ok)

    def save(self):
        file_name = QFileDialog.getSaveFileName(self, "Сохранить файл", ".", "All Files (*)")
        if file_name[0]:
            with open(file_name[0], "w") as file:
                file.write(self.ui.cipher_text.toPlainText())
        else:
            QMessageBox.information(self, "Ошибка", "Файл не выбран", QMessageBox.Ok)


if __name__ == "__main__":
    app = QApplication()
    window = Application()
    app.exec()
