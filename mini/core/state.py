from enum import Enum, auto

class MiniState(Enum):
	INACTIVE=auto()
	ACTIVE=auto()
	OFF=auto()
	VOICE=auto()
	GESTURE=auto()

class stateManager:
	def __init__(self):
		self._state=MiniState.INACTIVE

	def set_state(self, new_state=MiniState):
		self._state=new_state

	def get_state(self)->MiniState:
		return self._state

	def is_off(self) -> bool:
		return self._state==MiniState.OFF

	def is_active(self) -> bool:
		return self._state==MiniState.ACTIVE

	def is_voice(self) -> bool:
		return self._state==MiniState.VOICE

	def is_gesture(self) -> bool:
		return self._state==MiniState.GESTURE

state_manager = stateManager()