import webrtcvad
import time
# from mini.core.state import state_manager,MiniState
vad = webrtcvad.Vad(3)

sample_rate=16000
frame_duration=20
frame_size= int(sample_rate * frame_duration/1000)* 2
SILENCE_TIMEOUT=10

class VAD_processor:

	def __init__(self):
		self.timeout=SILENCE_TIMEOUT
		self.last_speech_time= None
	
	def reset(self):
		self.last_speech_time=None

	def vad_speech(self, frame) -> bool:
		try:
			now = time.time()
			# frame = b'\x00' * 320 
			# is_speech = False
			for i in range(0, 480, 160):
				vad_chunk = frame[i:i+160].astype('int16').tobytes()
				if vad.is_speech(vad_chunk, sample_rate):
					self.last_speech_time= now
					return True
			if self.last_speech_time is None:
				return True
			
			return (now - self.last_speech_time) < self.timeout
					# print("No speech detected for 5 seconds. Stopping Mini.")
					# state_manager.set_state(MiniState.INACTIVE)
			# return now - last_speech_time >= SILENCE_TIMEOUT
		except Exception as e:
			print("Error in vad:", e)
			return False