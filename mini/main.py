import threading
from mini.core.state import state_manager, MiniState
from mini.audio.wake_word_detection import run_wake_word_detection
from mini.ui.tray import tray_app
from mini.audio.listener import Audio_listener
from mini.audio.vad import VAD_processor
from mini.audio.speech_to_text import convert_to_speech

wake_thread = True
wake_running = False
# wake_detected = threading.Event()
wake_stop_event = threading.Event()
listener = Audio_listener(wake_stop_event)
vad_proc=VAD_processor()


def start_Mini():
    global wake_thread, wake_running
    buffer=[]
    silence_counter = 0
    recording = False

    print("start_wake_word_listener called, current state:", state_manager.get_state(), "running:", wake_running)
    if wake_running:
        print("start_wake_word_listener: already running")
        return
    wake_running = True
    wake_stop_event.clear()
    # wake_detected.clear()

    def audio_loop():
        listener.start()
        print("Wake word listening started")

        while not wake_stop_event.is_set():
            frame = listener.read()
            if state_manager.get_state() == MiniState.INACTIVE:
                if run_wake_word_detection(frame):
                    # wake_detected.set()
                    print("Wake word detected!")
                    vad_proc.reset()
                    state_manager.set_state(MiniState.ACTIVE)
            
            elif state_manager.get_state() == MiniState.ACTIVE:
                # wake_detected.wait()
                is_speech = vad_proc.vad_speech(frame)
                if is_speech==1:
                    # print("speech detecteds")
                    recording= True
                    silence_counter=0
                    buffer.append(frame)

                elif recording:
                    silence_counter+=1
                    if convert_to_speech(silence_counter,buffer):
                        buffer.clear()
                        recording=False
                        silence_counter=0
                elif is_speech==2:
                    print("No speech detected, returning to INACTIVE state")
                    state_manager.set_state(MiniState.INACTIVE)
                    
                    # continue
                # print(is_speech)
            if frame is None:
                    continue
 
        listener.stop()
        print("Wake word listener stopped")

    try:
        listen_thread = threading.Thread(target=audio_loop, daemon=True)
        listen_thread.start()
        # listen_thread.join()
    except Exception as e:
        print("Error in wake word listener thread:", e)
        wake_running = False



def stop_Mini():
    global wake_running

    print("stop_wake_word_listener called, running:", wake_running)

    if not wake_running:
        print("stop_wake_word_listener: not running, nothing to stop")
        return

    wake_stop_event.set()
    wake_running = False
    # porcupine.delete()
    print("wake listener stop requested")
    listener.stop()
    print("Wake word listener stopped")

# def vad_state_detection(frame):
#     while True:
#         vad_state=vad_speech(frame)
#         if vad_state:
#             print(vad_state)
#             return
#         else:
#             print("silence detected")
#             return 0


def main():
    try:
        tray_thread=threading.Thread(
            target=tray_app,
            args= (start_Mini,stop_Mini)
        )
        tray_thread.start()
        # Wait for tray thread to finish (keeps the program running)
        tray_thread.join()
        
    except KeyboardInterrupt:
        # Ensure wake listener is stopped on interrupt
        stop_Mini()

if __name__ == '__main__':
    main()