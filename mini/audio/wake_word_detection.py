import pvporcupine
# from mini.audio.listener import audio_frame
# import mini.main
# from mini.core.state import state_manager, MiniState
import sounddevice as sd
import numpy as np 
from dotenv import load_dotenv
# from mini.audio.vad import vad_speech
import os

load_dotenv()

ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY")
if not ACCESS_KEY:
  print("Warning: PICOVOICE_ACCESS_KEY not set; porcupine may fail to initialize")

SAMPLE_RATE = 16000
# FRAME_DURATION_MS=10
FRAME_LENGTH = 512

porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keyword_paths=["C:/Users/shrey/mini/hey-mini_en_windows_v4_0_0.ppn"]
  )


def run_wake_word_detection(frame)->bool:


  # print("wake word code running frame:", frame.shape)
  try:
    pcm = frame[:, 0].astype('int16').tolist()
    
    # print(len(pcm), porcupine.frame_length)
    return porcupine.process(pcm)>=0
  except Exception as e:
    print("Error during wake word detection:", e)
    return False
    