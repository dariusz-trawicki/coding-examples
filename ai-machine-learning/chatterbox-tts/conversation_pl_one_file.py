import torch
import numpy as np
import torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
import os

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Running on device: {DEVICE}")

# Load model
model = ChatterboxMultilingualTTS.from_pretrained(DEVICE)

# Paths to your samples
LUKE_VOICE = "example_samples/sample_02.wav"
VADER_VOICE = "example_samples/sample_03.wav"

# Output directory
OUTPUT_DIR = "output_samples"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Polish dialogue — 2 sentences each
dialogue = [
    ("Vader", "Luk, musimy porozmawiać. Znowu zostawiłeś miecz świetlny na kanapie."),
    ("Luke", "Wiem, przepraszam. Ale ty z kolei zostawiłeś hełm w lodówce!"),
    ("Vader", "Musiał się schłodzić. Synu, twoje bałaganiarstwo zaprowadzi cię prosto na ciemną stronę mocy."),
    ("Luke", "A ty lepiej wróć do ćwiczeń oddechowych, bo sąsiadka narzeka, że u nas ciągle ktoś trenuje z akwalungiem."),
    ("Vader", "I przestań używać mocy do robienia kanapek. Lodówka już drugi raz próbowała mnie udusić. To jest nienormalne."),
]

# Map speaker → reference audio
voice_map = {
    "Luke": LUKE_VOICE,
    "Vader": VADER_VOICE
}

sample_rate = model.sr
pause_seconds = 0.45
audio_segments = []

print("\nGenerating dialogue...\n")

for speaker, text in dialogue:
    print(f"{speaker}: {text}")

    wav = model.generate(
        text=text,
        language_id="pl",
        audio_prompt_path=voice_map[speaker],
        temperature=0.8,
        exaggeration=0.5,
        cfg_weight=0.5
    )

    if not isinstance(wav, torch.Tensor):
        wav = torch.tensor(wav)

    audio_segments.append(wav)

    # Add silence between lines
    pause_samples = int(pause_seconds * sample_rate)
    silence = torch.zeros((1, pause_samples))
    audio_segments.append(silence)

# Combine all audio
full_audio = torch.cat(audio_segments, dim=1)

# Save result
output_path = f"{OUTPUT_DIR}/full_conversation_pl.wav"
ta.save(output_path, full_audio, sample_rate)

print(f"\n✓ Conversation saved to: {output_path}")
print(f"Duration: {full_audio.shape[1] / sample_rate:.2f} seconds\n")
