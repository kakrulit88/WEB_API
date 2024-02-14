import os
import sys

import requests
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Yandex_MAP(QWidget):
    def __init__(self):
        super().__init__()

        self.url = 'http://static-maps.yandex.ru/1.x/'
        self.lon, self.lat = 37.530887, 55.703118
        self.delta = 0.002

        self.params = {
            "ll": ",".join([str(self.lon), str(self.lat)]),
            "spn": ",".join([str(self.delta), str(self.delta)]),
            "l": "map"
        }

        self.get_Image()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Яндекс карта с алиэкспреса')

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)

        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def update_map(self):
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def get_Image(self):
        self.params = {
            "ll": ",".join([str(self.lon), str(self.lat)]),
            "spn": ",".join([str(self.delta), str(self.delta)]),
            "l": "map"
            }

        response = requests.get(self.url, self.params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(self.url, self.params)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def keyPressEvent(self, event):
        # if event.key() == QtCore.Qt.Key.Key_PageUp:
        if event.key() == QtCore.Qt.Key.Key_W:
            self.delta = self.delta + 0.002

        # if event.key() == QtCore.Qt.Key.Key_PageDown:
        if event.key() == QtCore.Qt.Key.Key_S:
            if self.delta - 0.002 > 0:
                self.delta = self.delta - 0.002

        if event.key() == QtCore.Qt.Key.Key_Right:
            self.lon += (self.lon / 12) * self.delta

        if event.key() == QtCore.Qt.Key.Key_Left:
            self.lon -= (self.lon / 12) * self.delta

        if event.key() == QtCore.Qt.Key.Key_Up:
            self.lat += (self.lon / 23) * self.delta

        if event.key() == QtCore.Qt.Key.Key_Down:
            self.lat -= (self.lon / 23) * self.delta

        self.get_Image()
        self.update_map()

    def closeEvent(self, event):
        os.remove(self.map_file)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Yandex_MAP()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
