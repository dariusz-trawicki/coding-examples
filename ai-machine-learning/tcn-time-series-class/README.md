# TCN Time-Series Classification

## Overview
A Temporal Convolutional Network (TCN) trained to classify 1-D synthetic signals into
three categories. Demonstrates how dilated causal convolutions capture long-range temporal
dependencies without recurrence.

## Problem
Given a time-series of length 128, predict which of three signal classes it belongs to:

| Class | Description |
|-------|-------------|
| `sine` | Sine wave with random frequency and phase |
| `sawtooth` | Sawtooth wave with random frequency and phase |
| `noise` | Band-limited (smoothed) Gaussian noise |

All signals have additive Gaussian noise to make the task non-trivial.


## Architecture

```
Input: (B, 1, 128)  — batch × channels × time
  ↓
TCNBlock  dilation=1   receptive field: 15 steps
  ↓
TCNBlock  dilation=2   receptive field: 29 steps
  ↓
TCNBlock  dilation=4   receptive field: 57 steps
  ↓
TCNBlock  dilation=8   receptive field: 113 steps
  ↓
TCNBlock  dilation=16  receptive field: 225 steps  (> seq_len=128 ✓)
  ↓
Last time-step  →  Linear(64 → 3)  →  CrossEntropyLoss
```

**Total receptive field: 435 steps** — the network "sees" the entire input sequence.

### TCN Block (per dilation level)
```
CausalConv1d → WeightNorm → ReLU → Dropout
CausalConv1d → WeightNorm → ReLU → Dropout
+ residual connection (1×1 conv if channels differ)
```

### Causal Convolution
Left-side padding only — the model never looks at future time steps.
This makes TCN suitable for real-time / online inference.

### Dilated Convolution
Skips `d-1` steps between filter taps. Doubling the dilation at each layer
gives an exponentially growing receptive field with O(log N) layers.

```
dilation=1:  [x][x][x][x][x]      normal conv
dilation=2:  [x][ ][x][ ][x]      skip every other step
dilation=4:  [x][ ][ ][ ][x]...   skip 3 steps
```

## Training Details
| Setting | Value |
|---------|-------|
| Optimizer | Adam |
| Scheduler | CosineAnnealingLR |
| Loss | CrossEntropyLoss |
| Epochs (default) | 30 |
| Batch size | 64 |
| Dataset size | 3,000 signals (80/20 train/val split) |
| Device | MPS / CUDA / CPU (auto) |

## Dataset
Generated synthetically at runtime — no download required.
Seed is fixed for reproducibility.

## Results
~99% validation accuracy after 30 epochs. The task is intentionally designed so
that a network without sufficient receptive field (plain CNN, shallow dilations) would
struggle, while TCN solves it easily.

## Usage
```bash
uv run main.py              # train for 30 epochs
uv run main.py --epochs 50  # longer training
uv run main.py --lr 5e-4    # custom learning rate
```

## Live Output
- **Training window** — loss and accuracy curves (train vs val) updated after each epoch
- **Prediction grid** — 3×3 sample signals after training with true and predicted labels;
  green title = correct, red = incorrect
