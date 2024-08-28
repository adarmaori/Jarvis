import ollama
import time
import pyaudio
import wave
import whisper
from pynput import keyboard
import tempfile
import os
import threading
import json

# from cli.index import index
# Parameters for audio recording

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Initialize PyAudio and Whisper model
audio = pyaudio.PyAudio()
model = whisper.load_model("base")

frames = []
recording = False
temp_wave_file = None

messages = [
    {
        'role': 'system',
        'content': 'You are an AI assistant, and your name is Jarvis. You will be given instructions, questions and generally messages from the user, and your responsibility is to react appropriately, and call the tools you need in the order you need to make sure what they need is done. When no tool is necessary, just respond to the user with your own thoughts'
    }
]



with open("cli/index/functions.json", "r") as file:
    tools = json.load(file)


print(tools)
def record_audio(temp_wave_file):
    global recording, frames
    frames = []
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording started. Press Spacebar to stop...")
    while recording:
        data = stream.read(CHUNK)
        frames.append(data)

    # Stop the stream and close it properly
    stream.stop_stream()
    stream.close()

    try:
        with wave.open(temp_wave_file.name, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
    except Exception as e:
        print(f"Error writing WAV file: {e}")

    print("Recording stopped...")


def start_recording():
    global recording, temp_wave_file
    if not recording:
        recording = True
        # Create a temporary file to store the audio
        temp_wave_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        # Start the recording in a new thread
        threading.Thread(target=record_audio, args=(temp_wave_file,)).start()

def stop_recording():
    global recording, temp_wave_file
    if recording:
        recording = False
        print("Processing audio...")
        time.sleep(1)

        # Load audio and run transcription
        try:
            print("The file name is: " + temp_wave_file.name)
            result = model.transcribe(temp_wave_file.name)
            print("Transcription:\n", result['text'])
            messages.append({'role': 'user', 'content': result['text']})
            response = ollama.chat(
                model="llama3.1",
                messages=messages,
                # tools=tools
            )
            print(response['message']['content'])
            print(response['message']['tool_calls'])
        except Exception as e:
            print(f"Error transcribing audio: {e}")

        # Clean up temporary file
        os.remove(temp_wave_file.name)
        temp_wave_file = None



recording_in_progress = False
def on_press(key):
    global recording_in_progress
    current_time = time.time()
    if key == keyboard.Key.space and not recording_in_progress:
        recording_in_progress = True
        start_recording()

def on_release(key):
    global recording_in_progress
    if key == keyboard.Key.space and recording_in_progress:
        recording_in_progress = False
        stop_recording()

    if key == keyboard.Key.esc:
        print("Listener stopped. Exiting...")
        return False

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

audio.terminate()
