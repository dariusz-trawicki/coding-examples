#!/usr/bin/env bash
set -e

echo "=== Sign Language Translator — Demo ==="

echo ""
echo "[1/2] Extracting keypoints..."
uv run extract_keypoints.py --input data/videos/ --output keypoints/ --visualize --save_video

echo ""
echo "[2/2] Augmenting data and training model..."
uv run augment.py
uv run train_classifier_aug.py

echo ""
echo "=== Demo complete ==="
echo "Model saved to: keypoints/model_cnn.pt"
