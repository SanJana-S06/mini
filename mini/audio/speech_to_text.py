import numpy as np
# import time
import queue
import threading

model = None
audio_queue = queue.Queue()
_audio_buffer = []
model_lock = threading.Lock()

# BUFFER_SECONDS = 1.2
# SAMPLE_RATE = 16000
# BUFFER_SAMPLES = int(SAMPLE_RATE * BUFFER_SECONDS)
# _audio_buffer = np.empty((0,), dtype=np.int16)
# last_speech_time=time.time()


def _load_model():
	from faster_whisper import WhisperModel
	print("Loading Whisper model...")
	return WhisperModel("small", device="cpu", compute_type="int8")


def get_model():
	global model
	if model is None:
		with model_lock:
			if model is None:
				model = _load_model()
	return model


def preload_model():
	threading.Thread(target=get_model, daemon=True, name="whisper-preload").start()


def reset_buffer():
	global _audio_buffer
	_audio_buffer=[]


def push_audio(frame):
	_audio_buffer.append(frame[:,0])

def convert_to_speech():
	global _audio_buffer
	# if silence_counter>SILENCE_FRAMES_TO_STOP:
	# print("processing to text")
	if not _audio_buffer:
		return ""
	_audio_buffer=np.concatenate(_audio_buffer)
	audio=_audio_buffer.astype(np.float32)/32768.0
	_audio_buffer=[]
	# print("audio energy:", np.abs(audio).mean())
	model = get_model()
	segments, _ = model.transcribe(
		audio,
		language="en",
		beam_size=1,
		vad_filter=True,
		condition_on_previous_text=False,
		without_timestamps=True
		)
	return " ".join(seg.text.strip() for seg in segments).strip()

def sst(stop_event,state_manager):
	print("sst thread ready")
	while not stop_event.is_set():
		if state_manager.get_state().name != 'ACTIVE':
			# time.sleep(0.05)
			continue

		try:
			frame = audio_queue.get(timeout=0.1)
		except queue.Empty:
			continue
		push_audio(frame)
		# print("frame shape:", frame.shape, "dtype:", frame.dtype)
		# convert_to_speech(frame)