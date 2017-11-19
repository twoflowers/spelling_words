from ws4py.client.threadedclient import WebSocketClient
import base64, json, ssl, subprocess, threading, time, pyaudio

class SpeechToTextClient(WebSocketClient):
    def __init__(self):
        ws_url = "wss://stream.watsonplatform.net/speech-to-text/api/v1/recognize"

        username = "3f6de098-3b12-445d-bf87-61a3343574c9"
        password = "IPdyxuPmkxdd"
        auth_string = "%s:%s" % (username, password)
        base64string = base64.encodestring(auth_string).replace("\n", "")

        self.listening = False

        try:
            WebSocketClient.__init__(self, ws_url,
                headers=[("Authorization", "Basic %s" % base64string)])
            self.connect()
        except: print "Failed to open WebSocket."

    def opened(self):
        self.send('{"action": "start", "content-type": "audio/l16;rate=16000"}')
        self.stream_audio_thread = threading.Thread(target=self.stream_audio)
        self.stream_audio_thread.start()

    def received_message(self, message):
        message = json.loads(str(message))
        if "state" in message:
            if message["state"] == "listening":
                self.listening = True
        print "Message received: " + str(message)

    # def stream_audio(self):
    #     while not self.listening:
    #         time.sleep(0.1)
    #
    #     # reccmd = ["afplay", "-f", "S16_LE", "-r", "16000", "-t", "raw"]
    #     reccmd = [
    #          "sox",
    #         #  "--no-show-progress",
    #          "--default-device",
    #          "--encoding", "signed-integer",
    #          "--bits", "16",
    #          "--endian", "little",
    #          "--rate", "44100",
    #          "--type", "raw",
    #          "-"
    #      ]
    #     p = subprocess.Popen(reccmd, stdout=subprocess.PIPE)
    #
    #     while self.listening:
    #         data = p.stdout.read(1024)
    #
    #         try: self.send(bytearray(data), binary=True)
    #         except ssl.SSLError: pass
    def stream_audio(self):
        while not self.listening:
            time.sleep(0.1)

        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paInt16,
                channels=2,
                rate=16000,
                input=True,
                frames_per_buffer=1024)

        # p = subprocess.Popen(stream, stdout=subprocess.PIPE)

        while self.listening:
            data = stream.read(1024)

            try:
                self.send(bytearray(data), binary=True)
            except ssl.SSLError:
                print "error"
                pass

        # p.kill()

    def close(self):
        self.listening = False
        self.stream_audio_thread.join()
        WebSocketClient.close(self)

try:
    stt_client = SpeechToTextClient()
    raw_input()
finally:
    stt_client.close()
