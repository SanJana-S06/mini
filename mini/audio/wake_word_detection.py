import pvporcupine
# from mini.audio.listener import audio_frame
# import mini.main
import sounddevice as sd
import numpy as np 
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY")
if not ACCESS_KEY:
  print("Warning: PICOVOICE_ACCESS_KEY not set; porcupine may fail to initialize")

SAMPLE_RATE = 16000
FRAME_LENGTH = 512

def run_wake_word_detection(stop_event):
  porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keyword_paths=["C:\\Users\\Sanjana.S\\OneDrive\\Desktop\\project mini\\hey-mini_en_windows_v4_0_0.ppn"]
  )

  try:
    with sd.InputStream(
      samplerate=SAMPLE_RATE,
      channels=1,
      dtype='int16',
      blocksize=FRAME_LENGTH
      ) as stream:
      print("listening to audio")
      while True:
        if stop_event.is_set():
          print("stop event detected, exiting wake-word loop")
          break
        try:
          audio_frame, _ = stream.read(FRAME_LENGTH)
        except Exception as e:
          print("Error reading audio frame:", e)
          break

        # Convert frame to 1-D int16 array expected by Porcupine
        audio_flat = audio_frame.flatten()
        # print(f"Read audio frame shape={audio_frame.shape} len={audio_flat.size} dtype={audio_flat.dtype}")
        if audio_flat.dtype != np.int16:
          try:
            audio_flat = audio_flat.astype(np.int16)
            print("Converted audio frame to int16")
          except Exception as e:
            print("Error converting audio frame to int16:", e)

        # process frame
        try:
          result = porcupine.process(audio_flat)
        except Exception as e:
          print("Error processing audio frame:", e)
          continue

        if result == 0:
          # detected `porcupine`
          print("wake word activated")
          break
  finally:
    try:
      porcupine.delete()
    except Exception:
      print("Error cleaning up porcupine")