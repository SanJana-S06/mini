import time
from mini.core.state import state_manager,MiniState

try:
    import webrtcvad
    vad = webrtcvad.Vad(3)
    VAD_AVAILABLE = True
except ModuleNotFoundError:
    print("Warning: webrtcvad is not installed. VAD will be disabled.")
    vad = None
    VAD_AVAILABLE = False

sample_rate=16000
frame_duration=20
frame_size= int(sample_rate * frame_duration/1000)* 2
# SILENCE_TIMEOUT=15

class VAD_processor:

	def __init__(self,SILENCE_TIMEOUT):
		self.timeout=SILENCE_TIMEOUT
		self.last_speech_time= None
	
	def reset(self):
		self.last_speech_time=None

	def vad_speech(self, frame)-> int:
		if not VAD_AVAILABLE:
			now = time.time()
			if self.last_speech_time is None:
				self.last_speech_time = now
				return 1
			if frame is None:
				if (now - self.last_speech_time) >= self.timeout:
					return 2
				return 0
			if (now - self.last_speech_time) >= self.timeout:
				return 2
			return 1
		try:
			now = time.time()
			# frame = b'\x00' * 320 
			speech_detected = False
			for i in range(0, 480, 160):
				vad_chunk = frame[i:i+160].astype('int16').tobytes()
				if vad.is_speech(vad_chunk, sample_rate):
					speech_detected= True
					break
			
			if speech_detected:
				self.last_speech_time= now
				return 1
			if self.last_speech_time is None:
				return 1
			
			if (now - self.last_speech_time) >= self.timeout:
				return 2
					# print("No speech detected for 5 seconds. Stopping Mini.")
					# state_manager.set_state(MiniState.INACTIVE)
			return 0
		except Exception as e:
			print("Error in vad:", e)
			return False