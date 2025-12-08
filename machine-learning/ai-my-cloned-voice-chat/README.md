# Local Voice Assistant with My Cloned Voice (Python + LLM + XTTS)

This project is a **local voice assistant** that:

1.  records my voice from the microphone,
2.  performs local speech recognition (ASR),
3.  sends the text to a local language model LLM (GPT4All),
4.  generates a response and **speaks it using my cloned voice** (TTS)
    with XTTS v2.

Everything runs fully locally.

Process: 
speech -> ASR (WhisperModel) -> text -> LLM (GPT) -> text -> TTS (xtts_v2) -> speech

------------------------------------------------------------------------

## 1. Project Structure

    ai-my-cloned-voice-chat/
    ├── asystent.py
    ├── audio_io.py
    ├── asr_local.py
    ├── llm_local.py
    ├── tts_local.py
    ├── requirements.txt
    ├── dataset/
    │   ├── metadata.csv
    │   └── wavs/
    │       ├── sample_01.wav
    │       ├── sample_02.wav
    │       ├── sample_03.wav
    │       ├── sample_04.wav
    │       ├── sample_05.wav
    │       ├── sample_06.wav
    │       ├── sample_07.wav
    │       ├── sample_08.wav
    │       ├── sample_09.wav
    │       └── sample_10.wav

------------------------------------------------------------------------

## 2. Requirements

Main packages:

    sounddevice
    soundfile
    scipy
    numpy
    faster-whisper
    gpt4all
    TTS
    torch==2.5.1
    torchaudio==2.5.1
    transformers==4.38.2

#### Creating the Python environment

``` bash
# use Python 3.11 because TLL library requires it
conda create -p ./venv python=3.11 -y
conda activate ./venv
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 3. Recording Voice Samples

1.  Audio files are stored in: `dataset/wavs/` Format:
    -   WAV, 16 kHz, mono, int16\
    -   10 clear sentences
2.  Helper script (not part of the main pipeline):
    `recorder_16khz_mono.py`\
    (loop — lets you record 10 sentences, each 10 seconds long, triggered by pressing Enter)

``` bash
python recorder_16khz_mono.py
```

NOTE: `metadata.csv` is not needed. When would `metadata.csv` be useful? - If you wanted to actually **train** fine‑tune a real TTS model on your voice (not just clone
it).

------------------------------------------------------------------------

## 4. ASR (Automatic Speech Recognition) - STT (Speech-To-Text)

File `asr_local.py`.

------------------------------------------------------------------------

## 5. Local LLM (Large Language Model) -- GPT4All (text in → text out)

File `llm_local.py`.

------------------------------------------------------------------------

## 6. XTTS -- Text‑to‑Speech "in my voice" (from recorded samples)

NOTE: `TTS` stands for `Text-To-Speech`.

File `tts_local.py`.

XTTS uses the provided audio samples (`speaker_wav=[...]`) to generate
speech with your timbre on the fly.

------------------------------------------------------------------------

## 7. Main application -- app.py

File `app.py`.


------------------------------------------------------------------------

## Final Result

After launching:

``` bash
python app.py
```

The application: - records your voice, - recognizes the text, -
generates a response with the local LLM, - **speaks the answer using
your cloned voice** (XTTS v2), - works entirely offline.

------------------------------------------------------------------------

## CLEAN UP

``` bash
conda deactivate
conda remove -p ./venv --all -y
```
