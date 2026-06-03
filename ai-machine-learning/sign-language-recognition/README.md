# Sign Language Recognition — Demo

Polish Sign Language (PJM) recognition proof-of-concept.

## What it does

Extracts body and hand keypoints from video using MediaPipe, trains a 1D CNN
classifier to recognize PJM signs.

## Pipeline

```
video (.mp4) → keypoints extraction → tensor (N, 90, 225) → 1D CNN → sign label
```

## Project structure

```
.
├── data/videos/                  # source videos
│   ├── 01_czesc.mp4
│   ├── 02_dzien_dobry.mp4
│   └── 03_dobry_wieczor.mp4
├── keypoints/                   # extracted data
│   ├── dataset.npy              # tensor (N, 90, 225)
│   ├── dataset_aug.npy          # augmented tensor (33, 90, 225)
│   ├── labels.json              # class names
│   ├── labels_aug.npy           # numeric labels for augmented dataset
│   └── model_cnn.pt             # trained model weights
├── extract_keypoints.py         # keypoint extraction script
├── augment.py                   # data augmentation script
├── train_classifier_aug.py      # model training script
└── README.md
```

## Feature vector (225 float32 per frame)

```
pose        33 × (x, y, z) =  99
left hand   21 × (x, y, z) =  63
right hand  21 × (x, y, z) =  63
──────────────────────────────
total                         225
```

Coordinates normalized to [0, 1] relative to frame. Missing landmarks = zeros.

## Setup

Requires Python 3.10+, [uv](https://github.com/astral-sh/uv).

## Usage

```bash
./run_demo.sh      # Running the entire demo
```

Step by step:

**1. Extract keypoints**
```bash
uv run extract_keypoints.py --input data/videos/ --output keypoints/
```

With live preview:
```bash
uv run extract_keypoints.py --input data/videos/ --output keypoints/ --visualize
```

Save annotated video:
```bash
uv run extract_keypoints.py --input data/videos/ --output keypoints/ --save_video
```

**2. Augment data**
```bash
uv run augment.py
```

Generates 10 augmented samples per class → tensor (33, 90, 225).

**3. Train classifier**
```bash
uv run train_classifier_aug.py
# Output:
# Epoch  20 | loss: 0.0437 | train: 1.00 | val: 1.00
# Epoch  40 | loss: 0.0144 | train: 1.00 | val: 1.00
# Epoch  60 | loss: 0.0028 | train: 1.00 | val: 1.00
# Epoch  80 | loss: 0.0005 | train: 1.00 | val: 1.00
# Epoch 100 | loss: 0.0003 | train: 1.00 | val: 1.00
# Epoch 120 | loss: 0.0008 | train: 1.00 | val: 1.00
# Epoch 140 | loss: 0.0001 | train: 1.00 | val: 1.00
# Epoch 160 | loss: 0.0002 | train: 1.00 | val: 1.00
# Epoch 180 | loss: 0.0002 | train: 1.00 | val: 1.00
# Epoch 200 | loss: 0.0001 | train: 1.00 | val: 1.00
```

## Model

1D CNN trained on keypoint sequences:

```
Conv1d(225→128) → ReLU → Dropout(0.3)
Conv1d(128→64)  → ReLU
AdaptiveAvgPool1d(1)
Linear(64→num_classes)
```

## Current results

| Video | Frames | Left hand | Right hand |
|---|---|---|---|
| 01_czesc | 75 | 4% | 46% |
| 02_dzien_dobry | 150 | 56% | 34% |
| 03_dobry_wieczor | 100 | 71% | 35% |

Training accuracy: 1.00 (3 classes, memorization expected at this dataset size).

## Limitations

- 3 classes only — not enough for real generalization
- Single recording per class — no true train/val split possible
- Augmented validation is not independent from training data


## Environment

- macOS arm64 (Apple Silicon M1 Max)
- Python 3.11 via uv
- MediaPipe 0.10.x
- PyTorch 2.x

## About PJM

Polish Sign Language (Polski Język Migowy) is an autonomous visual-spatial
language, not a signed version of Polish. It has its own grammar, spatial
syntax, and simultaneous morphology with no written form.

## Data

Source videos are from YouTube:
 - https://www.youtube.com/watch?v=kAPkLzE4gpI
