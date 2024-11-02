#!/usr/bin/env bash

python3 create_dataset.py;
echo $?

if [ $? -eq 0 ]; then
  python3 train_classifier.py;
else
  echo "train_classifier failed"
  exit 1
fi

echo $?
if [ $? -eq 0 ]; then
  python3 inference_classifier.py;
else
  echo "inference_classifier failed"
  exit 1
fi