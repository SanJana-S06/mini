import threading
from mini.core.state import state_manager, MiniState
from mini.audio.wake_word_detection import run_wake_word_detection
from mini.ui.tray import tray_app

wake_thread = True
wake_running = False
wake_stop_event = threading.Event()

def start_wake_word_listener():
    global wake_thread, wake_running

    print("start_wake_word_listener called, current state:", state_manager.get_state(), "running:", wake_running)

    if state_manager.get_state() != MiniState.ACTIVE:
        print("start_wake_word_listener: not ACTIVE, not starting")
        return
    if wake_running:
        print("start_wake_word_listener: already running")
        return

    wake_stop_event.clear()
    wake_thread = threading.Thread(
        target=run_wake_word_detection,
        args=(wake_stop_event,),
        daemon=True
    )
    wake_thread.start()
    print("wake listener thread started")

    wake_running = True

def stop_wake_word_listener():
    global wake_running

    print("stop_wake_word_listener called, running:", wake_running)

    if not wake_running:
        print("stop_wake_word_listener: not running, nothing to stop")
        return

    wake_stop_event.set()
    wake_running = False
    print("wake listener stop requested")



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