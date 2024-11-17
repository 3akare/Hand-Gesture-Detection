#!/usr/bin/env bash

python3 create_dataset.py
if [ $? -ne 0 ]; then
  echo "create_dataset failed"
  exit 1
fi

python3 train_classifier.py
if [ $? -ne 0 ]; then
  echo "train_classifier failed"
  exit 1
fi

python3 inference_classifier.py
if [ $? -ne 0 ]; then
  echo "inference_classifier failed"
  exit 1
fi
