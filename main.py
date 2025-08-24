import argparse
import threading
import time
from audio_capture import AudioCapturer, list_audio_devices
from transcriber import Transcriber
from llm_client import LLMClient
from gui import TUI

def main():
    parser = argparse.ArgumentParser(description="AI Video Watching Buddy")
    parser.add_argument("--device", type=str, help="The name of the audio input device to use.")
    parser.add_argument("--list-devices", action="store_true", help="List available audio devices and exit.")
    parser.add_argument("--model", type=str, default="gemma3", help="The Ollama model to use.")
    args = parser.parse_args()

    if args.list_devices:
        print("Available audio devices:")
        print(list_audio_devices())
        return

    if not args.device:
        print("Please specify an audio device using --device.")
        print("Available audio devices:")
        print(list_audio_devices())
        return

    # 1. Instantiate the TUI
    tui = TUI()

    # 2. Instantiate the LLMClient with callbacks to the TUI
    def reaction_callback(chunk):
        tui.write_to_log(chunk)

    def new_reaction_callback():
        tui.new_reaction()

    llm_client = LLMClient(model=args.model, reaction_callback=reaction_callback)
    llm_client.new_reaction = new_reaction_callback


    # 3. Instantiate the Transcriber with a callback to the LLMClient
    def transcription_callback(text):
        llm_client.get_reaction(text)

    transcriber = Transcriber(transcription_callback=transcription_callback)

    # 4. Instantiate and start the AudioCapturer
    capturer = AudioCapturer(device=args.device)
    capturer.start()

    # 5. Create a thread to process audio
    def audio_processing_thread():
        while capturer.recording:
            try:
                chunk = capturer.get_audio_chunk()
                transcriber.process_audio_chunk(chunk)
            except Exception as e:
                print(f"Error in audio processing thread: {e}")
                break

    audio_thread = threading.Thread(target=audio_processing_thread)
    audio_thread.start()

    # 6. Run the TUI
    # This will block until the TUI exits
    tui.run()

    # 7. Cleanup
    print("Shutting down...")
    capturer.stop()
    audio_thread.join()
    print("Cleanup complete.")


if __name__ == "__main__":
    main()
