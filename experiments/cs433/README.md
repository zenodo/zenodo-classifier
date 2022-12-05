# Experiments

Luka Secilmis, Thomas Ecabert, Yanis De Busschere

## Abstract

This folder contains all the notebooks used for experimenting with the differents models during the project.

## Summary of experiments

| Experiment          | Folder                                             | Training Time | Prediction Time | Accuracy | F1-Score |
|---------------------|----------------------------------------------------|---------------|-----------------|----------|----------|
| BERT (english only) | [./en-spam-classifier](./en-spam-classifier)       | 1h02          | 0.005s          | 98.759   | 98.600   |
| BERT (multilingual) | [./multi-spam-classifier](./multi-spam-classifier) | 1h09          | 0.005           | 98.814   | 98.779   |

All computation and time measurement were made using an NVIDIA RTX A5000.
