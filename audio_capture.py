import sounddevice as sd
import numpy as np
import queue
import threading

def list_audio_devices():
    """Lists available audio devices."""
    return sd.query_devices()

class AudioCapturer:
    def __init__(self, device=None, samplerate=16000, channels=1):
        self.device = device
        self.samplerate = samplerate
        self.channels = channels
        self.q = queue.Queue()
        self.recording = False
        self.stream = None
        self.thread = None

    def _callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status)
        self.q.put(indata.copy())

    def start(self):
        """Starts the audio recording."""
        self.recording = True
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def _record(self):
        with sd.InputStream(samplerate=self.samplerate,
                             device=self.device,
                             channels=self.channels,
                             callback=self._callback):
            while self.recording:
                sd.sleep(100)

    def stop(self):
        """Stops the audio recording."""
        self.recording = False
        if self.thread:
            self.thread.join()

    def get_audio_chunk(self):
        """Gets an audio chunk from the queue."""
        return self.q.get()

if __name__ == '__main__':
    # Example usage:
    print("Available audio devices:")
    print(list_audio_devices())

    # To run this example, you would need to select a device.
    # For example, if 'BlackHole 2ch' is an input device.
    # capturer = AudioCapturer(device='BlackHole 2ch')
    # capturer.start()
    # print("Recording... Press Ctrl+C to stop.")
    # try:
    #     while True:
    #         chunk = capturer.get_audio_chunk()
    #         print(f"Got audio chunk of size: {len(chunk)}")
    # except KeyboardInterrupt:
    #     capturer.stop()
    #     print("Recording stopped.")
