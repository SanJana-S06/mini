from mini.actions.app_func import *
from mini.actions.operations import *
# from mini.core.state import state_manager, MiniState
def route(task,stop_mini):
	try:
		action=task["action"]
		arg=task["argument"]
		match action:
			case "OPEN_APP":
				open_app(arg)
			case "CLOSE_APP":
				close_app(arg)
			case "MINI_OFF":
				stop_mini()
			case "TEXT_TYPE":
				type_text(arg)
			# state_manager.set_state(MiniState.OFF)
	except:
		pass
