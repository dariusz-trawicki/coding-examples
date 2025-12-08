import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf

def record_wav(filename="input.wav", duration=5, fs=16000):
    print(f"Recording ({duration} s)...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    write(filename, fs, audio)
    print("Saved:", filename)

def play_wav(filename: str):
    data, fs = sf.read(filename, dtype='float32')
    sd.play(data, fs)
    sd.wait()
