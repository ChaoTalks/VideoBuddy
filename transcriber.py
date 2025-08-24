import numpy as np
from pywhispercpp.model import Model
import threading
import logging

class Transcriber:
    def __init__(self, model_name="tiny.en", transcription_callback=None, sample_rate=16000):
        self.model = Model(model_name,
                           print_realtime=False,
                           print_progress=False,
                           print_timestamps=False,
                           single_segment=True,
                           n_threads=4)
        self.transcription_callback = transcription_callback
        self.sample_rate = sample_rate
        self.audio_buffer = np.array([], dtype=np.float32)
        self.buffer_lock = threading.Lock()
        self.transcribing = False

    def process_audio_chunk(self, chunk):
        """Receives an audio chunk and adds it to the buffer."""
        with self.buffer_lock:
            self.audio_buffer = np.append(self.audio_buffer, chunk)

        # If buffer is long enough and not already transcribing, start transcription
        if len(self.audio_buffer) >= self.sample_rate * 5 and not self.transcribing:
            self.transcribing = True
            threading.Thread(target=self._transcribe).start()

    def _transcribe(self):
        """Transcribes the audio buffer."""
        with self.buffer_lock:
            audio_to_process = self.audio_buffer
            self.audio_buffer = np.array([], dtype=np.float32)

        logging.info("Transcribing audio chunk of size %d", len(audio_to_process))
        # The model expects a 16kHz mono float32 numpy array.
        # The sounddevice library should already provide this format.
        segments = self.model.transcribe(audio_to_process)
        text = "".join(segment.text for segment in segments)

        if self.transcription_callback and text.strip():
            self.transcription_callback(text)

        self.transcribing = False

if __name__ == '__main__':
    # Example Usage
    logging.basicConfig(level=logging.INFO)

    def my_callback(text):
        print(f"Transcription: {text}")

    transcriber = Transcriber(transcription_callback=my_callback)

    # Simulate receiving audio chunks
    # In the real application, this will come from the AudioCapturer
    sample_rate = 16000
    # Create 6 seconds of dummy audio data
    dummy_audio_chunk = np.random.rand(sample_rate * 6).astype(np.float32)

    transcriber.process_audio_chunk(dummy_audio_chunk)

    # Keep the main thread alive to see the transcription result
    import time
    time.sleep(5)
    print("Example finished.")
