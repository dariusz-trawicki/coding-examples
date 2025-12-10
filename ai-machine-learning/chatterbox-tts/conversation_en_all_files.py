import torchaudio as ta
import torch
from chatterbox.tts import ChatterboxTTS
import os

# Automatically detect the best available device
if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"

print(f"Using device: {device}")

# Load the TTS model
model = ChatterboxTTS.from_pretrained(device=device)

# Voice prompt paths
VADER_VOICE = "example_samples/sample_03.flac"
LUKE_VOICE = "example_samples/sample_02.flac"

# Output directory for generated audio
output_dir = "output_samples"
os.makedirs(output_dir, exist_ok=True)

# Check if voice files exist
if not os.path.exists(VADER_VOICE):
    raise FileNotFoundError(f"Vader voice file not found at {VADER_VOICE}")
if not os.path.exists(LUKE_VOICE):
    raise FileNotFoundError(f"Luke voice file not found at {LUKE_VOICE}")

# Conversation script
conversation = [
    (
        "Vader",
        "Luke, I am your father.",
    ),
    (
        "Luke",
        "No! That’s impossible! Search your history! I am actually your father! You know it to be true!",
    ),
    (
        "Vader",
        "The Force is strong with you, my father. "
        "But your cooking skills are a path to the Dark Side.",
    ),
    (
        "Luke",
        "Better than your breathing skills.",
    ),
    (
        "Vader",
        "That was uncalled for. This is why we can’t have nice things in the galaxy.",
    ),
]

print("Generating conversation...")
print("=" * 50)

# Generate each line of the conversation and collect audio
audio_segments = []
pause_duration = 0.5  # seconds of silence between lines

for i, (speaker, text) in enumerate(conversation):
    print(f"\n{speaker}: {text}")

    # Choose the appropriate voice prompt
    if speaker == "Vader":
        voice_prompt = VADER_VOICE
    elif speaker == "Luke":
        voice_prompt = LUKE_VOICE
    else:
        raise ValueError(f"Unknown speaker: {speaker}")

    # Generate audio for this line
    try:
        wav = model.generate(text, audio_prompt_path=voice_prompt)

        # Ensure tensor format (1, num_samples)
        if not isinstance(wav, torch.Tensor):
            wav = torch.tensor(wav)

        audio_segments.append(wav)

        # Save the individual line
        filename = f"{output_dir}/{i + 1:02d}_{speaker.lower()}.wav"
        ta.save(filename, wav, model.sr)

        # Add silence after each line except the last one
        if i < len(conversation) - 1:
            pause_samples = int(pause_duration * model.sr)
            silence = torch.zeros((wav.shape[0], pause_samples))
            audio_segments.append(silence)

    except Exception as e:
        print(f"Error generating audio for {speaker}: {e}")

# Ensure something was generated
if not audio_segments:
    raise RuntimeError("No audio segments were generated.")

# Combine all generated segments
combined_audio = torch.cat(audio_segments, dim=1)

# Save the full combined conversation
combined_filename = f"{output_dir}/full_conversation_en.wav"
ta.save(combined_filename, combined_audio, model.sr)

# Compute duration
duration_minutes = combined_audio.shape[1] / model.sr / 60
print(f"✓ Combined conversation saved: {combined_filename}")
print(f"  Total duration: {duration_minutes:.1f} minutes")

print("\n" + "=" * 50)
print("Conversation generation complete!")
print(f"Audio files saved in: {output_dir}/")
print("Files generated:")

for i, (speaker, _) in enumerate(conversation):
    filename = f"{i + 1:02d}_{speaker.lower()}.wav"
    print(f"  - {filename}")

print("  - full_conversation_en.wav (combined)")
