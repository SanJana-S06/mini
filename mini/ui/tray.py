import os
import sys
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from mini.core.state import state_manager,MiniState

_start_Mini= None
_stop_Mini= None

def tray_app(start_Mini,stop_Mini):
	global _start_Mini,_stop_Mini
	_start_Mini=start_Mini
	_stop_Mini=stop_Mini
	QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
	QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
	app=QApplication(sys.argv)
	app.setQuitOnLastWindowClosed(False)

	icon=QIcon("./mini/icon.png")

	tray=QSystemTrayIcon()
	tray.setIcon(icon)
	tray.setVisible(True)
	# tray.activated.connect(tray_clicked)

	menu=QMenu()

	voice_action=QAction("Start Voice",menu)
	voice_action.triggered.connect(set_voice_state)
	menu.addAction(voice_action)

	stop_action=QAction("Stop",menu)
	stop_action.triggered.connect(set_off_state)
	menu.addAction(stop_action)

	quit_action=QAction("Quit")
	quit_action.triggered.connect(app.exit)
	menu.addAction(quit_action)

	tray.setContextMenu(menu)

	sys.exit(app.exec())

# def tray_clicked(reason):
# 	print("tray icon clicked, reason:", reason)
# 	if reason==QSystemTrayIcon.ActivationReason.Trigger:
# 		state_manager.set_state(MiniState.ACTIVE)
# 		_start_wake_word_listener()
# 		print("Mini Activated! state: ",state_manager.get_state())

def set_voice_state():
	state_manager.set_state(MiniState.VOICE)
	# print("Voice State Set",state_manager.get_state())
	state_manager.set_state(MiniState.INACTIVE)
	_start_Mini()
	print("Mini state: ",state_manager.get_state())

def set_off_state():
	state_manager.set_state(MiniState.OFF)
	_stop_Mini()
	print("Off State Set",state_manager.get_state())


if __name__=='__main__':
	tray_app()
