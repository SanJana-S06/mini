import os
from PySide6.QtCore import Qt
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
from PySide6.QtWidgets import QApplication,QWidget
import sys
from PySide6.QtGui import QGuiApplication

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
app = QApplication(sys.argv)
screen = QGuiApplication.primaryScreen()
size = screen.size()

window_width=250
window_height=250
bottom_right_x = size.width()- window_width
bottom_right_y = size.height()- window_height

print(f"Bottom Right Coordinates: ({bottom_right_x}, {bottom_right_y})")




window=QWidget()

window.setGeometry(bottom_right_x,bottom_right_y,window_width,window_height)
window.SetTitle("Mini")
window.show()

app.exec()
