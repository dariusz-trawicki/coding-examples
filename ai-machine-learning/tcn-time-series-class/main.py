import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import argparse
from torch.utils.data import Dataset, DataLoader, random_split

# ── device ────────────────────────────────────────────────────────────────────
DEVICE = (
    torch.device("mps") if torch.backends.mps.is_available()
    else torch.device("cuda") if torch.cuda.is_available()
    else torch.device("cpu")
)
print(f"Device: {DEVICE}")

CLASSES = ["sine", "sawtooth", "noise"]
SEQ_LEN = 128
N_CLASSES = 3

# ── dataset ───────────────────────────────────────────────────────────────────
class SignalDataset(Dataset):
    """
    3 classes of 1-D signals, each of length SEQ_LEN:
      0 — sine wave      (random freq + phase)
      1 — sawtooth wave  (random freq + phase)
      2 — band-limited noise
    All signals have additive Gaussian noise to make the task non-trivial.
    """
    def __init__(self, n_samples: int = 3000, seq_len: int = SEQ_LEN, seed: int = 42):
        rng = np.random.default_rng(seed)
        t = np.linspace(0, 1, seq_len)
        X, y = [], []

        per_class = n_samples // N_CLASSES
        for cls in range(N_CLASSES):
            for _ in range(per_class):
                freq  = rng.uniform(3, 15)
                phase = rng.uniform(0, 2 * np.pi)
                noise = rng.normal(0, 0.15, seq_len)

                if cls == 0:   # sine
                    sig = np.sin(2 * np.pi * freq * t + phase)
                elif cls == 1: # sawtooth
                    sig = 2 * (freq * t + phase / (2 * np.pi)
                               - np.floor(freq * t + phase / (2 * np.pi))) - 1
                else:          # band-limited noise
                    raw = rng.normal(0, 1, seq_len)
                    # smooth with a short moving average
                    kernel = np.ones(8) / 8
                    sig = np.convolve(raw, kernel, mode="same")
                    sig = sig / (np.std(sig) + 1e-8)

                X.append((sig + noise).astype(np.float32))
                y.append(cls)

        self.X = torch.tensor(np.array(X)).unsqueeze(1)  # (N, 1, SEQ_LEN)
        self.y = torch.tensor(y, dtype=torch.long)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


def get_loaders(batch_size: int = 64):
    ds = SignalDataset()
    n_val = int(0.2 * len(ds))
    train_ds, val_ds = random_split(ds, [len(ds) - n_val, n_val],
                                    generator=torch.Generator().manual_seed(0))
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader   = DataLoader(val_ds,   batch_size=batch_size, shuffle=False)
    return train_loader, val_loader, ds


# ── TCN building blocks ───────────────────────────────────────────────────────
class CausalConv1d(nn.Module):
    """Conv1d with left-only (causal) padding so the model never sees the future."""
    def __init__(self, in_ch, out_ch, kernel_size, dilation):
        super().__init__()
        self.pad = (kernel_size - 1) * dilation
        self.conv = nn.Conv1d(in_ch, out_ch, kernel_size,
                              dilation=dilation, padding=0)

    def forward(self, x):
        x = nn.functional.pad(x, (self.pad, 0))
        return self.conv(x)


class TCNBlock(nn.Module):
    """
    One residual TCN block:
      CausalConv → WeightNorm → ReLU → Dropout
      CausalConv → WeightNorm → ReLU → Dropout
      + residual (1×1 conv if channel sizes differ)
    """
    def __init__(self, in_ch, out_ch, kernel_size, dilation, dropout=0.2):
        super().__init__()

        def _wn_causal(in_c, out_c, ks, d):
            block = CausalConv1d(in_c, out_c, ks, d)
            block.conv = nn.utils.parametrizations.weight_norm(block.conv)
            return block

        self.net = nn.Sequential(
            _wn_causal(in_ch,  out_ch, kernel_size, dilation),
            nn.ReLU(),
            nn.Dropout(dropout),
            _wn_causal(out_ch, out_ch, kernel_size, dilation),
            nn.ReLU(),
            nn.Dropout(dropout),
        )
        self.downsample = nn.Conv1d(in_ch, out_ch, 1) if in_ch != out_ch else None
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.net(x)
        res = x if self.downsample is None else self.downsample(x)
        return self.relu(out + res)


class TCN(nn.Module):
    """
    Temporal Convolutional Network for sequence classification.

    Key idea: exponentially increasing dilations give a large receptive field
    with O(log N) layers instead of O(N) layers needed by a plain CNN.

    Receptive field = 1 + 2 * (kernel_size-1) * sum(dilations)
    With kernel=8, dilations=[1,2,4,8,16]: RF = 1 + 14*(1+2+4+8+16) = 435 > SEQ_LEN=128 ✓
    """
    def __init__(self, in_ch=1, n_classes=N_CLASSES,
                 channels=64, kernel_size=8,
                 dilations=(1, 2, 4, 8, 16), dropout=0.2):
        super().__init__()
        layers = []
        ch_in = in_ch
        for d in dilations:
            layers.append(TCNBlock(ch_in, channels, kernel_size, d, dropout))
            ch_in = channels
        self.tcn = nn.Sequential(*layers)
        self.head = nn.Linear(channels, n_classes)

    def forward(self, x):
        # x: (B, 1, T)
        out = self.tcn(x)          # (B, C, T)
        out = out[:, :, -1]        # take last time-step  (B, C)
        return self.head(out)      # (B, n_classes)


# ── live plot ─────────────────────────────────────────────────────────────────
def make_live_plot():
    fig, (ax_loss, ax_acc) = plt.subplots(1, 2, figsize=(11, 4))
    fig.suptitle("TCN — Signal Classification Training", fontsize=13, fontweight="bold")
    for ax, title, ylabel in [
        (ax_loss, "Loss",     "Loss"),
        (ax_acc,  "Accuracy", "Accuracy %"),
    ]:
        ax.set_title(title); ax.set_xlabel("Epoch"); ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)
    plt.tight_layout(); plt.ion(); plt.show()
    return fig, ax_loss, ax_acc


def update_live_plot(fig, ax_loss, ax_acc, tr_losses, val_losses, tr_accs, val_accs):
    epochs = range(1, len(tr_losses) + 1)
    for ax in (ax_loss, ax_acc): ax.cla()

    ax_loss.set_title("Loss"); ax_loss.set_xlabel("Epoch"); ax_loss.set_ylabel("Loss")
    ax_loss.plot(epochs, tr_losses,  "b-o", ms=4, label="train")
    ax_loss.plot(epochs, val_losses, "r-o", ms=4, label="val")
    ax_loss.legend(); ax_loss.grid(True, alpha=0.3)

    ax_acc.set_title("Accuracy"); ax_acc.set_xlabel("Epoch"); ax_acc.set_ylabel("Accuracy %")
    ax_acc.plot(epochs, tr_accs,  "b-o", ms=4, label="train")
    ax_acc.plot(epochs, val_accs, "r-o", ms=4, label="val")
    ax_acc.legend(); ax_acc.grid(True, alpha=0.3)

    fig.canvas.draw(); fig.canvas.flush_events()


# ── train / eval ──────────────────────────────────────────────────────────────
def run_epoch(model, loader, criterion, optimizer=None):
    training = optimizer is not None
    model.train() if training else model.eval()
    total_loss, correct, total = 0.0, 0, 0
    ctx = torch.enable_grad() if training else torch.no_grad()
    with ctx:
        for X, y in loader:
            X, y = X.to(DEVICE), y.to(DEVICE)
            out = model(X)
            loss = criterion(out, y)
            if training:
                optimizer.zero_grad(); loss.backward(); optimizer.step()
            total_loss += loss.item() * y.size(0)
            correct    += (out.argmax(1) == y).sum().item()
            total      += y.size(0)
    return total_loss / total, 100.0 * correct / total


# ── prediction grid ───────────────────────────────────────────────────────────
def show_predictions(model, dataset):
    """Show 9 sample signals with true label and predicted label."""
    model.eval()
    indices = np.random.choice(len(dataset), 9, replace=False)
    fig, axes = plt.subplots(3, 3, figsize=(12, 7))
    fig.suptitle("TCN Predictions — Signal Classification", fontsize=13, fontweight="bold")
    colors = ["#4C72B0", "#DD8452", "#55A868"]

    for ax, idx in zip(axes.flat, indices):
        x, true_label = dataset[idx]
        with torch.no_grad():
            pred = model(x.unsqueeze(0).to(DEVICE)).argmax(1).item()
        signal = x.squeeze().numpy()
        color = colors[true_label]
        ax.plot(signal, color=color, linewidth=0.9)
        correct = pred == true_label
        title_color = "green" if correct else "red"
        ax.set_title(
            f"true: {CLASSES[true_label]}  pred: {CLASSES[pred]}",
            color=title_color, fontsize=8
        )
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_edgecolor("#cccccc")

    plt.tight_layout()
    plt.ioff(); plt.show()


# ── main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int,   default=30)
    parser.add_argument("--lr",     type=float, default=1e-3)
    args = parser.parse_args()

    train_loader, val_loader, full_dataset = get_loaders()
    model     = TCN().to(DEVICE)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)

    total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Params: {total_params:,}")

    # print receptive field info
    kernel, dilations = 8, [1, 2, 4, 8, 16]
    rf = 1 + 2 * (kernel - 1) * sum(dilations)
    print(f"Receptive field: {rf} steps  (seq_len={SEQ_LEN})")

    fig, ax_loss, ax_acc = make_live_plot()
    tr_losses, val_losses, tr_accs, val_accs = [], [], [], []

    for epoch in range(1, args.epochs + 1):
        tr_loss, tr_acc   = run_epoch(model, train_loader, criterion, optimizer)
        val_loss, val_acc = run_epoch(model, val_loader,   criterion)
        scheduler.step()

        tr_losses.append(tr_loss);   val_losses.append(val_loss)
        tr_accs.append(tr_acc);      val_accs.append(val_acc)

        print(f"Epoch {epoch:2d}/{args.epochs} | "
              f"loss {tr_loss:.3f}/{val_loss:.3f} | "
              f"acc {tr_acc:.1f}%/{val_acc:.1f}%")

        update_live_plot(fig, ax_loss, ax_acc, tr_losses, val_losses, tr_accs, val_accs)

    print("\nTraining done!")
    show_predictions(model, full_dataset)


if __name__ == "__main__":
    main()
