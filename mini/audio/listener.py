import sounddevice as sd
import queue
import numpy as np

SAMPLE_RATE=16000
FRAME_LENGTH=512

class Audio_listener:
	def __init__(self,stop_event):
		self.stop_event=stop_event
		self.q=queue.Queue(maxsize=5)

	def _callback(self,indata,frames,time,status):
		if status:
			print("Audio Listener Status:",status)
		if self.stop_event.is_set():
			return
		try:
			self.q.put_nowait(indata.copy())
		except queue.Full:
			pass

	def start(self):
		self.stream=sd.InputStream(
			samplerate=SAMPLE_RATE,
			channels=1,
			dtype='int16',
			blocksize=FRAME_LENGTH,
			callback=self._callback
		)
		self.stream.start()
		print("listening....")

	def read(self):
		return self.q.get()

	def stop(self):
		self.stop_event.set()
		self.stream.stop()
		self.stream.close()