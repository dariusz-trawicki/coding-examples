from faster_whisper import WhisperModel


# Load the ASR (Automatic Speech Recognition) model 
# (e.g., "small", "medium" – the larger the model, the better the quality 
# but slower)
model = WhisperModel("small", device="cpu")  # if you have a GPU, you can use device="cuda"

def speech_to_text(audio_path: str) -> str:
    segments, info = model.transcribe(audio_path, beam_size=5)
    text = "".join(seg.text for seg in segments)
    return text.strip()
