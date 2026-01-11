import webrtcvad
from mini.core.state import state_manager,MiniState
vad = webrtcvad.Vad(3)

sample_rate=16000
frame_duration=20
frame_size= int(sample_rate * frame_duration/1000)* 2


def vad_speech(frame) -> bool:
	try:
		# frame = b'\x00' * 320 
		is_speech = False
		for i in range(0, 480, 160):
			vad_chunk = frame[i:i+160].astype('int16').tobytes()
			if vad.is_speech(vad_chunk, sample_rate):
				is_speech = True
				break
		return is_speech
	except Exception as e:
		print("Error in vad:", e)
		return False