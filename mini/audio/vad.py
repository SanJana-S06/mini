import webrtcvad
from mini.core.state import state_manager,MiniState
vad = webrtcvad.Vad()

def vad_speech(audio_frame)->bool:
	sample_rate=16000
	frame_duration=10
	audio_bytes=audio_frame.tobytes()
	# audio_frame = b'\x00\x00' * int(sample_rate * frame_duration / 1000)
	return vad.is_speech(audio_bytes,sample_rate)
