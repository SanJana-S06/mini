import sounddevice as sd
import numpy as np 

SAMPLE_RATE = 16000
FRAME_LENGTH = 512

def audio_frame():
	with sd.InputStream(
		samplerate=SAMPLE_RATE,
		channels=1,
		dtype='int16',
		blocksize=FRAME_LENGTH
	) as stream:
		print("listening....")
		while True:
			audio_frame, _ = stream.read(FRAME_LENGTH)
            yield audio_frame.flatten()


