# Chatterbox TTS

**Chatterbox Multilingual** is a modern, open-source **TTS model** supporting **23 languages**.

GitHub repository: https://github.com/resemble-ai/chatterbox

### Key Details
- Multilingual, zero-shot TTS supporting 23 languages
- SoTA zeroshot English TTS
- 0.5B Llama backbone
- Unique exaggeration/intensity control
- Ultra-stable with alignment-informed inference
- Trained on 0.5M hours of cleaned data
- Watermarked outputs
- Easy voice conversion script
- [Outperforms ElevenLabs](https://podonos.com/resembleai/chatterbox)

### Supported Languages 
Arabic (ar) • Danish (da) • German (de) • Greek (el) • English (en) • Spanish (es) • Finnish (fi) • French (fr) • Hebrew (he) • Hindi (hi) • Italian (it) • Japanese (ja) • Korean (ko) • Malay (ms) • Dutch (nl) • Norwegian (no) • Polish (pl) • Portuguese (pt) • Russian (ru) • Swedish (sv) • Swahili (sw) • Turkish (tr) • Chinese (zh)

---

## Prerequisites

Before running the project, ensure you have installed:

### 1. **uv** — Fast Python package manager  
Installation guide: https://docs.astral.sh/uv/getting-started/installation/

```bash
# macOS
brew install uv
```

### Environment setup:

```bash
# Create environment
uv venv --python 3.11

# Install dependencies from project
uv pip install -e .

# Activate environment
source .venv/bin/activate
```

---

## Data (folder: `example_samples/`)

- `sample_01` — my own recorded voice  
- `sample_02` and `sample_03` — downloaded from: https://pixabay.com/

---

## Running Examples

### 1. **TTS — Text-to-Speech**

Generate speech audio using the timbre and style of a reference sample (`flac`, `wav`, etc.):

```bash
python example_tts.py
```

### 2. **Voice Cloning**

Clone or transform one speaker’s voice into another using two reference audio files:

```bash
python example_vc.py
```

### 3. **Create a Conversation**

Generate full back‑and‑forth speech interactions:

```bash
python conversation_en_all_files.py
python conversation_pl_one_file.py
```

---

## Results

All generated outputs (audio files) are stored in the `output_samples/` directory.

---

## License

This project uses components from the open‑source Chatterbox TTS system. See the upstream repository for license details.  
