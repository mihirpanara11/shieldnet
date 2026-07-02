import numpy as np
import pandas as pd
from typing import Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shieldnet.data.feature_pipeline")


def build_sequences(X: np.ndarray, y: np.ndarray,
                    seq_length: int = 60) -> Tuple[np.ndarray, np.ndarray]:
    sequences = []
    labels = []
    for i in range(len(X) - seq_length):
        seq = X[i:i + seq_length]
        label = y[i + seq_length]
        sequences.append(seq)
        labels.append(label)
    return np.array(sequences), np.array(labels)


def process_dataset(features_path: str, labels_path: str,
                    seq_length: int = 60) -> dict:
    X = np.load(features_path)
    y = np.load(labels_path)
    logger.info(f"Loaded {len(X)} samples with {X.shape[1]} features")

    X_seq, y_seq = build_sequences(X, y, seq_length)
    logger.info(f"Created {len(X_seq)} sequences of length {seq_length}")

    split = int(len(X_seq) * 0.7)
    split_val = int(len(X_seq) * 0.85)

    return {
        "X_train": X_seq[:split],
        "y_train": y_seq[:split],
        "X_val": X_seq[split:split_val],
        "y_val": y_seq[split:split_val],
        "X_test": X_seq[split_val:],
        "y_test": y_seq[split_val:],
    }


def save_sequences_h5(data: dict, output_path: str, category: str):
    import h5py
    with h5py.File(output_path, 'a') as f:
        if category in f:
            del f[category]
        grp = f.create_group(category)
        grp.create_dataset('X_train', data=data['X_train'], compression='gzip')
        grp.create_dataset('y_train', data=data['y_train'], compression='gzip')
        grp.create_dataset('X_val', data=data['X_val'], compression='gzip')
        grp.create_dataset('y_val', data=data['y_val'], compression='gzip')
        grp.create_dataset('X_test', data=data['X_test'], compression='gzip')
        grp.create_dataset('y_test', data=data['y_test'], compression='gzip')
    logger.info(f"Saved sequences for {category} to {output_path}")
