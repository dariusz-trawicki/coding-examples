import torchaudio as ta
import torch
from chatterbox.tts import ChatterboxTTS
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

# Automatically detect the best available device
if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"

print(f"Using device: {device}")

model = ChatterboxTTS.from_pretrained(device=device)

## 1. Synthesize with a default voices:
text = "Hello there. How are you?"
wav = model.generate(text)
ta.save("output_samples/tts_en_default_voice.wav", wav, model.sr)

multilingual_model = ChatterboxMultilingualTTS.from_pretrained(device=device)
text = "Bonjour, comment ça va?"
wav = multilingual_model.generate(text, language_id="fr")
ta.save("output_samples/tts_fr_default_voice.wav", wav, multilingual_model.sr)


multilingual_model = ChatterboxMultilingualTTS.from_pretrained(device=device)
text = "Cześć, jak się masz?"
wav = multilingual_model.generate(text, language_id="pl")
ta.save("output_samples/tts_pl_default_voice.wav", wav, multilingual_model.sr)


## 2. Synthesize with a different voices:

text = "Hello. How are you?"
AUDIO_PROMPT_PATH = "example_samples/sample_02.flac"   # OR:
# AUDIO_PROMPT_PATH = "example_samples/sample_02.wav"
wav = model.generate(text, audio_prompt_path=AUDIO_PROMPT_PATH)
ta.save("output_samples/tts_en_diff_voice_.wav", wav, model.sr)

POLISH_PROMPT = "example_samples/sample_01.flac"   # OR:
# POLISH_PROMPT = "example_samples/sample_01.wav"
text = "Cześć, jak się masz?"
# Generate with Polish reference audio
wav = multilingual_model.generate(
    text,
    language_id="pl",
    audio_prompt_path=POLISH_PROMPT,
    temperature=0.8,
    exaggeration=0.5,
    cfg_weight=0.5,
)
ta.save("output_samples/tts_pl_diff_voice.wav", wav, multilingual_model.sr)




