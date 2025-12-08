# tts_local.py
from pathlib import Path

import torch
from TTS.api import TTS

MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Initialize XTTS v2
tts = TTS(MODEL_NAME).to(DEVICE)

# Path to your voice samples
SAMPLES_DIR = Path("dataset/wavs")

# List of WAV files that XTTS will use for voice cloning
SPEAKER_WAVS = sorted(SAMPLES_DIR.glob("*.wav"))


def tts_to_file(
    text: str,
    out_path: str = "reply.wav",
    language: str = "en",
) -> str:
    """
    Generate speech from text, cloning the voice based on WAV files from SAMPLES_DIR.
    """
    if not SPEAKER_WAVS:
        raise RuntimeError(
            f"No .wav files found in {SAMPLES_DIR.resolve()}. "
            "Make sure your recordings are there."
        )

    print(" > Text split into sentences.")
    print([s.strip() for s in text.split(".") if s.strip()])

    tts.tts_to_file(
        text=text,
        file_path=out_path,
        speaker_wav=[str(p) for p in SPEAKER_WAVS],
        language=language,
    )
    return out_path


if __name__ == "__main__":
    # Small test: generate a 'test_reply.wav' sample
    test_text = "This is a short test of my cloned voice using XTTS."
    print("Generating test file test_reply.wav...")
    tts_to_file(test_text, "test_reply.wav", language="en")
    print("Done: test_reply.wav")
