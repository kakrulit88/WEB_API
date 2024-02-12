import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Yandex_MAP(QWidget):
    def __init__(self):
        super().__init__()

        self.url = 'http://static-maps.yandex.ru/1.x/'
        self.lon, self.lat = '37.530887', '55.703118'
        self.delta = '0.002'

        self.params = {
            "ll": ",".join([self.lon, self.lat]),
            "spn": ",".join([self.delta, self.delta]),
            "l": "map"
        }

        self.get_Image(self.url, params=self.params)
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Яндекс карта с алиэкспреса')

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)

        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def get_Image(self, url, params):
        response = requests.get(url, params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(url, params)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Yandex_MAP()
    ex.show()
    sys.exit(app.exec())
