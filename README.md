# AI Video Watching Buddy

This application listens to your computer's audio, transcribes it in real-time,
and uses a local Large Language Model (LLM) to generate reactions. It's like
having an AI buddy watching videos with you and sharing its thoughts.

## Features

- Real-time audio transcription using Whisper.cpp
- Reactions from a local Ollama LLM
- Terminal-based GUI to display reactions

## How it works

1.  **Audio Capture**: Captures system audio via a virtual audio device like
    BlackHole.
2.  **Transcription**: Transcribes the audio to text using `whisper-cpp`.
3.  **LLM Reactions**: Sends the transcribed text to an Ollama LLM to get
    reactions.
4.  **GUI**: Displays the LLM's reactions in a terminal interface.

## Prerequisites

1.  **Python 3.8+**
2.  **Ollama**: You need to have [Ollama](https://ollama.com/) installed and running.
3.  **Ollama Model**: Pull a model for Ollama to use. We recommend `gemma3`.
    ```bash
    ollama pull gemma3
    ```
4.  **Virtual Audio Device**: You need a way to route your system audio as a microphone input.
    -   **macOS**: [BlackHole](https://github.com/ExistentialAudio/BlackHole) is a great option. After installing, set BlackHole as your sound output device, and then you will use it as the input device for this application.
    -   **Windows**: You can use a tool like [VB-CABLE Virtual Audio Device](https://vb-audio.com/Cable/).
    -   **Linux**: You can use PulseAudio or PipeWire to create a virtual sink and source.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    The `pywhispercpp` library will also download the `tiny.en` model on its first run.

## Running the Application

1.  **Find your audio device name:**
    Run the following command to list all available audio devices on your system.
    ```bash
    python main.py --list-devices
    ```
    Look for the name of your virtual audio device in the output (e.g., `BlackHole 2ch`).

2.  **Run the application:**
    Use the device name you found in the previous step with the `--device` flag.
    ```bash
    python main.py --device "BlackHole 2ch"
    ```
    You can also specify a different Ollama model with the `--model` flag:
    ```bash
    python main.py --device "BlackHole 2ch" --model "llama3"
    ```

3.  **Enjoy!**
    Now, play any video or audio on your computer. You should see the AI buddy's reactions appear in your terminal. Press `Ctrl+C` to exit. You can also press `d` to toggle dark mode.
