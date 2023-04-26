import string
from enum import Enum

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem
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
        self.matrix = []
        self.matrix_size = None
        self.data = None
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
                self.data = self.crypt_text(self.Action.ENCRYPT.value)
            elif self.ui.btn_dec.isChecked():
                self.data = self.crypt_text(self.Action.DECRYPT.value)
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
        self.fill_key_matrix()

    def fill_key_matrix(self):
        self.matrix_size = int(pow(len(self.matrix), 0.5))
        self.ui.abc_table.setColumnCount(self.matrix_size)
        self.ui.abc_table.setRowCount(self.matrix_size)
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                self.ui.abc_table.setItem(i, j, QTableWidgetItem(self.matrix[i * self.matrix_size + j].upper()))
        self.ui.abc_table.resizeRowsToContents()
        self.ui.abc_table.resizeColumnsToContents()

    def get_plaintext(self):
        result = []
        plaintext = self.ui.plain_text.toPlainText().lower().replace(" ", "")
        if not set(plaintext).issubset(self.matrix):
            return QMessageBox.information(self, "Ошибка", "Введите корректный ключ", QMessageBox.Ok)
        for i in range(0, len(plaintext) - 1, 2):
            if plaintext[i] == plaintext[i + 1]:
                if plaintext[i] == "x" and plaintext[i + 1] == "x":
                    plaintext = plaintext[:i + 1] + "o" + plaintext[i + 1:]
                else:
                    plaintext = plaintext[:i + 1] + "x" + plaintext[i + 1:]
        if len(plaintext) % 2:
            if plaintext[-1] == "x":
                plaintext += "o"
            else:
                plaintext += "x"
        for i in range(0, len(plaintext) - 1, 2):
            result.append(plaintext[i:i + 2])
        return result

    def calculate_indexes(self, indexes, choice):
        index_x, index_y = indexes
        if index_x[0] == index_y[0]:
            new_index_x = (index_x[0], ((index_x[1] + 1 * choice) + self.matrix_size) % self.matrix_size)
            new_index_y = (index_y[0], ((index_y[1] + 1 * choice) + self.matrix_size) % self.matrix_size)
        elif index_x[1] == index_y[1]:
            new_index_x = (((index_x[0] + 1 * choice) + self.matrix_size) % self.matrix_size, index_x[1])
            new_index_y = (((index_y[0] + 1 * choice) + self.matrix_size) % self.matrix_size, index_y[1])
        else:
            new_index_x = (index_x[0], index_y[1])
            new_index_y = (index_y[0], index_x[1])
        return new_index_x, new_index_y

    def crypt_text(self, choice):
        bigrams = self.get_plaintext()
        size = int(pow(len(self.matrix), 0.5))
        text = ''
        for item in bigrams:
            x, y = item[0], item[1]
            index_x = (self.matrix.index(x) // self.matrix_size, self.matrix.index(x) % self.matrix_size)
            index_y = (self.matrix.index(y) // self.matrix_size, self.matrix.index(y) % self.matrix_size)
            new_index_x, new_index_y = self.calculate_indexes((index_x, index_y), choice)
            text += self.matrix[new_index_x[0] * self.matrix_size + new_index_x[1]]
            text += self.matrix[new_index_y[0] * self.matrix_size + new_index_y[1]]
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
