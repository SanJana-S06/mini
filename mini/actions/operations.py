import pyautogui
pyautogui.PAUSE = 2 
pyautogui.FAILSAFE = True


def type_text(text):
	pyautogui.typewrite(text)