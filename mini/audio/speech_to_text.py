from faster_whisper import WhisperModel
import numpy as np

SILENCE_FRAMES_TO_STOP = 6 
model = WhisperModel("tiny", compute_type="int8")

def convert_to_speech(silence_counter,buffer):

	if silence_counter>SILENCE_FRAMES_TO_STOP:
		print("processing to text")
		audio=np.concatenate(buffer,axis=0)
		audio=audio.flatten().astype(np.float32)/32768.0
		segments, _ = model.transcribe(audio)
		for segment in segments:
			print("➡️", segment.text)
			
		return True
	
	return False

