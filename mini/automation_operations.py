import pyautogui
from time import *
from files_list import search_application

pyautogui.PAUSE = 2 
pyautogui.FAILSAFE = True
sstring=search_application()
print(sstring)
def automation():
	# pyautogui.hotkey('win','d')
	pyautogui.hotkey('win')
	pyautogui.typewrite(f"{sstring}")
	# pyautogui.press("enter")
	test()

# pyautogui.typewrite(" Hello there! Am mini\n How may i help you ", interval= .05)

def test():
	print("this is test func call from imported file")

