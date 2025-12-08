import sounddevice as sd
from scipy.io.wavfile import write

def record_wav(
    filename="sample.wav",
    duration=10,
    fs=16000,
):
    """
    Records from the microphone and saves as 16 kHz, mono, WAV (int16).

    :param filename: name of the output .wav file
    :param duration: recording duration in seconds
    :param fs: sampling rate (here: 16000 Hz)
    """
    channels = 1            # MONO
    dtype = 'int16'         # standard WAV format

    print(f"Recording {duration} s at 16 kHz, mono...")
    recording = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=channels,
        dtype=dtype
    )
    sd.wait()  # wait until recording is finished
    write(filename, fs, recording)
    print(f"Saved to file: {filename}")

if __name__ == "__main__":
    for i in range(1, 11):
        filename = f"dataset/wavs/sample_{i:02d}.wav"
        print(f"\nGet ready to record {i}...")
        input("Press Enter when you’re ready.")
        record_wav(filename, duration=10, fs=16000)
