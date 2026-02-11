import time
from threading import Timer

class TypingIndicator:
    def __init__(self, pause_time=2):
        self.is_typing = False
        self.pause_time = pause_time
        self.timer = None

    def start_typing(self):
        if not self.is_typing:
            self.is_typing = True
            print("composing → User started typing...")
        self.reset_timer()

    def stop_typing(self):
        if self.is_typing:
            self.is_typing = False
            print("paused → User stopped typing.")

    def reset_timer(self):
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(self.pause_time, self.stop_typing)
        self.timer.start()

# ====== Simulation ======
typing_indicator = TypingIndicator(pause_time=3)

# User starts typing
typing_indicator.start_typing()
time.sleep(1)

# User keeps typing (debounced, so no repeated "composing")
typing_indicator.start_typing()
time.sleep(1)

# User keeps typing again
typing_indicator.start_typing()
time.sleep(4)  # >3 sec → should trigger paused automatically

# User types again after pause
typing_indicator.start_typing()
time.sleep(3)
