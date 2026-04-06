import threading
from mini.core.state import state_manager, MiniState
from mini.audio.wake_word_detection import run_wake_word_detection, porcupine
from mini.ui.tray import tray_app
from mini.audio.listener import Audio_listener
from mini.audio.vad import VAD_processor
from mini.audio.speech_to_text import sst,audio_queue,convert_to_speech,preload_model
from mini.commands.normalizer import normalize
from mini.commands.parser import parse
from mini.core.router import route

wake_thread = True
wake_running = False
# wake_detected = threading.Event()
wake_stop_event = threading.Event()
listener = Audio_listener(wake_stop_event)
vad_active_or_inactive=VAD_processor(15)
vad_speech=VAD_processor(1)


def start_Mini():
    global wake_thread, wake_running
    # buffer=[]
    # silence_counter = 0
    # recording = False

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
            if frame is None:
                continue
            if state_manager.get_state() == MiniState.INACTIVE:
                if run_wake_word_detection(frame):
                    # wake_detected.set()
                    print("Wake word detected!")
                    vad_active_or_inactive.reset()
                    # vad_speech.reset()
                    state_manager.set_state(MiniState.ACTIVE)
            
            elif state_manager.get_state() == MiniState.ACTIVE:
                # wake_detected.wait()
                is_speech_active_inactive = vad_active_or_inactive.vad_speech(frame)
                is_speech = vad_speech.vad_speech(frame)
                if is_speech==1:
                    audio_queue.put(frame)
                if is_speech==2:
                    cmd=convert_to_speech()
                    if cmd:
                        print(cmd)
                        cmds=normalize(cmd)
                        for part in cmds:
                            print(part.strip())
                            parser_data=parse(part)
                            route(parser_data,stop_Mini)
                    # print("speech detecteds")
                    # recording= True
                    # silence_counter=0
                    # buffer.append(frame)

                # elif recording:
                #     silence_counter+=1

                    # if convert_to_speech(silence_counter,buffer):
                    #     buffer.clear()
                    #     recording=False
                    #     silence_counter=0
                if is_speech_active_inactive==2:
                    print("No speech detected, returning to INACTIVE state")
                    state_manager.set_state(MiniState.INACTIVE)
                    
                    # continue
                # print(is_speech)
            if frame is None:
                    continue
 
        listener.stop()
        print("Wake word listener stopped")

    try:
        preload_model()
        listen_thread = threading.Thread(target=audio_loop, daemon=True)
        listen_thread.start()
        speech_thread = threading.Thread(target=sst,args=(wake_stop_event,state_manager), daemon=True)
        speech_thread.start()
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
    try:
        porcupine.delete()
    except Exception as e:
        print("Error deleting porcupine instance:", e)
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
# def shutdown():
#     print("Shutting down Mini...")

#     wake_stop_event.set()

#     try:
#         listener.stop()
#     except:
#         pass

#     try:
#         if porcupine:
#             porcupine.delete()
#     except:
#         pass

#     try:
#         with audio_queue.mutex:
#             audio_queue.queue.clear()
#     except:
#         pass
#     app.exec()


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