import pyaudio
import wave
import whisper
from pynput import keyboard

class Transcriber:
    def __init__(self):
        self.model = whisper.load_model("base")
        self.p = pyaudio.PyAudio()
        self.device_index = self._select_device()
        self.recording = False
        self.frames = []
        self.stream = None

    def _select_device(self):
        print("\nAvailable input devices:")
        valid_devices = []
        for i in range(self.p.get_device_count()):
            try:
                dev = self.p.get_device_info_by_index(i)
                if dev['maxInputChannels'] > 0:
                    print(f"{len(valid_devices)}: {dev['name']}")
                    valid_devices.append(i)
            except IOError:
                pass
        if not valid_devices:
            raise IOError("No valid input devices found")
        selection = int(input("Enter the number of the input device you want to use: "))
        return valid_devices[selection]

    def _on_press(self, key):
        try:
            if key == keyboard.Key.space and not self.recording:
                print("Recording...")
                self.recording = True
                self.frames = []
                self._start_recording()
        except AttributeError:
            pass

    def _start_recording(self):
        try:
            self.stream = self.p.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=44100,
                                      frames_per_buffer=1024,
                                      input=True,
                                      input_device_index=self.device_index,
                                      stream_callback=self._audio_callback)
            self.stream.start_stream()
        except OSError as e:
            print(f"Error opening stream: {e}")
            self.recording = False

    def _on_release(self, key):
        if key == keyboard.Key.space and self.recording:
            print("Recording finished.")
            self.recording = False
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            return False

    def _audio_callback(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        return (None, pyaudio.paContinue)

    def _save_audio(self, filename):
        if self.frames:
            wf = wave.open(filename, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))
            wf.close()
        else:
            print("No audio recorded.")

    def listen(self, callback):
        def on_release_wrapper(key):
            if self._on_release(key) is False:
                audio_filename = "recorded_audio.wav"
                self._save_audio(audio_filename)
                transcribed_text = self.transcribe(audio_filename)
                callback(transcribed_text)
            return True

        with keyboard.Listener(on_press=self._on_press, on_release=on_release_wrapper) as listener:
            listener.join()

    def transcribe(self, filename):
        result = self.model.transcribe(filename)
        return result['text']
