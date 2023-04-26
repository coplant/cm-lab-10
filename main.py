import string
from enum import Enum

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from ui_mainwindow import Ui_MainWindow


class Application(QMainWindow):
    class Action(Enum):
        ENCRYPT = -1
        DECRYPT = 1

    class Language(Enum):
        RUSSIAN = 0
        ENGLISH = 1

    def __init__(self):
        super(Application, self).__init__()
        self.data = None
        self.matrix = []
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        self.ui.btn_enc.setChecked(True)

        self.ru_abc = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        self.en_abc = "abcdefghijklmnopqrstuvwxyz"
        self.abc = [self.ru_abc, self.en_abc]

        self.ui.proc_button.clicked.connect(self.process_data)
        self.ui.open_file.triggered.connect(self.open)
        self.ui.save_file.triggered.connect(self.save)

    def process_data(self):
        self.data = self.ui.plain_text.toPlainText()
        try:
            self.get_key_matrix(self.ui.line_key.text())
            if self.ui.btn_enc.isChecked():
                self.data = self.crypt_text(self.data, self.Action.ENCRYPT.value)
            elif self.ui.btn_dec.isChecked():
                self.data = self.crypt_text(self.data, self.Action.DECRYPT.value)
        except ValueError as e:
            ...
        self.ui.cipher_text.setText(str(self.data))

    def get_key_matrix(self, key_string):
        self.matrix.clear()
        option = self.ui.combo.currentIndex()
        key = key_string.lower()
        for char in key:
            if char == "j":
                char = "i"
            if char in self.abc[option] and char not in self.matrix and char.isalpha():
                self.matrix.append(char)
        for char in self.abc[option]:
            if char == "j":
                char = "i"
            if char not in self.matrix:
                self.matrix.append(char)
        if option == self.Language.RUSSIAN.value:
            self.matrix.append(".")
            self.matrix.append(",")
            self.matrix.append(" ")

    def crypt_text(self, data, choice):
        # extended_key = self.get_extended_key(data)
        text = ''
        for i, char in enumerate(data):
            is_found = False
            for abc in self.abc:
                if char.lower() in abc:
                    to_add = abc[(len(abc) + abc.index(char.lower()) - choice * extended_key[i]) % len(abc)]
                    text += to_add.upper() if char.isupper() else to_add.lower()
                    is_found = True
            if not is_found:
                text += char
        return text

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
