import threading
from mini.core.state import state_manager, MiniState
from mini.audio.wake_word_detection import run_wake_word_detection
from mini.ui.tray import tray_app
from mini.audio.listener import Audio_listener

wake_thread = True
wake_running = False
wake_stop_event = threading.Event()
listener = Audio_listener(wake_stop_event)


def start_wake_word_listener():
    global wake_thread, wake_running

    print("start_wake_word_listener called, current state:", state_manager.get_state(), "running:", wake_running)

    if state_manager.get_state() != MiniState.ACTIVE:
        print("start_wake_word_listener: not ACTIVE, not starting")
        return
    if wake_running:
        print("start_wake_word_listener: already running")
        return
    wake_running = True
    wake_stop_event.clear()

    def audio_loop():
        listener.start()
        print("Wake word listening started")

        while not wake_stop_event.is_set():
            frame = listener.read()
            if frame is None:
                continue

            if run_wake_word_detection(frame,wake_stop_event):
                print("Wake word detected!")

        listener.stop()
        print("Wake word listener stopped")

    try:
        listen_thread = threading.Thread(target=audio_loop, daemon=True)
        listen_thread.start()
        # listen_thread.join()
    except Exception as e:
        print("Error in wake word listener thread:", e)
        wake_running = False



def stop_wake_word_listener():
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



def main():
    try:
        tray_thread=threading.Thread(
            target=tray_app,
            args= (start_wake_word_listener,stop_wake_word_listener)
        )
        tray_thread.start()
        # Wait for tray thread to finish (keeps the program running)
        tray_thread.join()
        
    except KeyboardInterrupt:
        # Ensure wake listener is stopped on interrupt
        stop_wake_word_listener()

if __name__ == '__main__':
    main()