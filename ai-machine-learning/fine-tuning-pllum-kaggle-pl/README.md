# Fine-tuning Llama-PLLuM-8B-chat — QLoRA na darmowym GPU

Minimalny pipeline fine-tuningu QLoRA dla **PLLuM** — polskiego otwartego modelu językowego — uruchamiany na GPU T4 (Kaggle).

## Co robi

Dostosowuje `Llama-PLLuM-8B-chat` do własnego datasetu instrukcji przy użyciu **QLoRA** (kwantyzacja 4-bit + adaptery LoRA), trenując jedynie ~42M z 8B parametrów. Wynikiem jest lekki adapter LoRA (~100 MB), który można scalić z modelem bazowym lub używać samodzielnie.

---

## Stos technologiczny

| Komponent | Biblioteka / Model |
|---|---|
| Model bazowy | `CYFRAGOVPL/Llama-PLLuM-8B-chat` |
| Kwantyzacja | 4-bitowe QLoRA via [Unsloth](https://github.com/unslothai/unsloth) |
| Trening | `trl` `SFTTrainer` + `SFTConfig` |
| Rank LoRA | r=16, alpha=16, dropout=0.0 |
| Trenowalne parametry | ~42M / 8B (0.52%) |
| Środowisko | T4 15 GB (Kaggle free / Google Colab free) |
| Czas treningu | ~5 min (1 epoka, mały dataset) |

---

## O PLLuM

PLLuM to rodzina dużych modeli językowych wyspecjalizowanych w języku polskim i innych językach słowiańskich/bałtyckich, opracowana przez [konsorcjum HIVE AI](https://pllum.org.pl) oraz Ministerstwo Cyfryzacji.

`Llama-PLLuM-8B-chat` bazuje na **Llama 3.1-8B**, opublikowanym na licencji **Llama 3.1** (otwarta, dozwolony użytek komercyjny), i był dalej pretrenowany na ~30 miliardach tokenów polskiego tekstu.

### Kluczowa różnica od innych modeli Llama 3.1

PLLuM używa **szablonu czatu Llama 3** — nie ChatML. To kluczowe przy fine-tuningu:

```
# PLLuM / Llama 3 (poprawnie):
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{system}<|eot_id|><|start_header_id|>user<|end_header_id|>

{user}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

{assistant}<|eot_id|>

# ChatML (błędnie dla PLLuM):
<|im_start|>system
{system}<|im_end|>
```

Użycie błędnego szablonu spowoduje ciche trenowanie na niepoprawnych danych.

---

## Szybki start

### Kaggle

1. Przejdź na [kaggle.com](https://www.kaggle.com) → **New Notebook**
2. Settings → Accelerator → **GPU T4 x2**
3. Wgraj `pllum-8b-finetuning.ipynb`
4. **Run All**


---

## Struktura notebooka

| Komórka | Opis |
|---|---|
| 1 | Instalacja zależności |
| 2 | Sprawdzenie GPU (`nvidia-smi`) |
| 3 | Ładowanie modelu + zastosowanie adapterów LoRA |
| 4 | Przygotowanie datasetu (format Llama 3) |
| 5 | Trening z `SFTTrainer` |
| 6 | Test fine-tunowanego modelu |
| 7 | Zapis adaptera LoRA lub eksport do GGUF |
| 8 | Wgranie na HuggingFace Hub |

---

## Używanie własnych danych

Zastąp listę `data` w komórce 4 własnymi przykładami w formacie `{instruction, input, output}`:

```python
data = [
    {
        "instruction": "Odpowiedz krótko po polsku.",
        "input": "Twoje pytanie tutaj",
        "output": "Oczekiwana odpowiedź tutaj"
    },
    ...
]
```

Funkcja `format_prompt` automatycznie opakuje każdy przykład w poprawny szablon czatu Llama 3.

---

## Wymagania pamięci GPU

| Etap | VRAM |
|---|---|
| Model (4-bit) | ~5.5 GB |
| Adaptery LoRA | ~0.2 GB |
| Narzut treningu | ~1–2 GB |
| **Łącznie** | **~7 GB** |

Mieści się komfortowo w 15 GB karty T4. Pozostałe ~8 GB stanowi bezpieczny margines dla dłuższych sekwencji.

---

## Konfiguracja LoRA — wyjaśnienie

```python
r=16,           # rank — wyższy = więcej trenowanych parametrów, wolniejszy trening
lora_alpha=16,  # współczynnik skalowania (alpha/r = 1.0 to bezpieczna wartość domyślna)
lora_dropout=0.0,  # 0.0 wymagane dla szybkich kerneli Unsloth
target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                "gate_proj", "up_proj", "down_proj"],
```

Ustawienie `lora_dropout > 0` wyłącza szybkie patchowanie QKV/MLP przez Unsloth i powoduje ~2x spowolnienie. Trzymaj wartość `0.0`, chyba że masz konkretny powód, by ją zmienić.

---

## Zapis adaptera

```python
# Opcja A: zapisz tylko adapter LoRA (~100 MB)
model.save_pretrained("pllum-8b-finetuned-lora")
tokenizer.save_pretrained("pllum-8b-finetuned-lora")

# Opcja B: scal LoRA + eksportuj do GGUF (dla Ollama / llama.cpp)
model.save_pretrained_gguf("pllum-8b-finetuned", tokenizer,
                           quantization_method="q4_k_m")
```

---

## Wgranie na HuggingFace Hub

```python
from huggingface_hub import login
login(token="hf_TWOJ_TOKEN")

model.push_to_hub("twoja-nazwa/pllum-8b-finetuned")
tokenizer.push_to_hub("twoja-nazwa/pllum-8b-finetuned")
```

---

## Licencja

- **Model:** [Licencja społecznościowa Llama 3.1](https://huggingface.co/meta-llama/Llama-3.1-8B/blob/main/LICENSE) — otwarta, dozwolony użytek komercyjny
- **Notebook:** MIT

---

## Źródła

- [PLLuM na HuggingFace](https://huggingface.co/CYFRAGOVPL)
- [Artykuł PLLuM (arXiv:2511.03823)](https://arxiv.org/abs/2511.03823)
- [Unsloth](https://github.com/unslothai/unsloth)
- [Dokumentacja TRL SFTTrainer](https://huggingface.co/docs/trl/sft_trainer)
