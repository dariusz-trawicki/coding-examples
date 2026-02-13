import torch
import torchaudio as ta

from chatterbox.vc import ChatterboxVC

# Automatically detect the best available device
if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"

print(f"Using device: {device}")

AUDIO_PATH = "example_samples/sample_01.flac"
TARGET_VOICE_PATH = "example_samples/sample_02.flac"

model = ChatterboxVC.from_pretrained(device)
wav = model.generate(
    audio=AUDIO_PATH,
    target_voice_path=TARGET_VOICE_PATH,
)
ta.save("output_samples/test_vc_kid.wav", wav, model.sr)

AUDIO_PATH = "example_samples/sample_01.flac"
TARGET_VOICE_PATH = "example_samples/sample_03.flac"

model = ChatterboxVC.from_pretrained(device)
wav = model.generate(
    audio=AUDIO_PATH,
    target_voice_path=TARGET_VOICE_PATH,
)
ta.save("output_samples/test_vc_vader.wav", wav, model.sr)
