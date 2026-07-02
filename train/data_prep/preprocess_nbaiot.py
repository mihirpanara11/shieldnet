import argparse
import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shieldnet.data.nbaiot")


def preprocess(args):
    logger.info(f"Preprocessing N-BaIoT data from {args.input}")
    df = pd.read_csv(args.input)
    logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")

    feature_cols = [c for c in df.columns if c not in ('Label', 'Category')]
    X = df[feature_cols].fillna(0).values.astype(np.float32)
    y = (df['Label'] != 'Benign').astype(int).values

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_test, y_test, test_size=0.5, random_state=42)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    np.save(output_dir / "X_train.npy", X_train)
    np.save(output_dir / "y_train.npy", y_train)
    np.save(output_dir / "X_val.npy", X_val)
    np.save(output_dir / "y_val.npy", y_val)
    np.save(output_dir / "X_test.npy", X_test)
    np.save(output_dir / "y_test.npy", y_test)

    logger.info(f"Saved: Train={len(X_train)}, Val={len(X_val)}, Test={len(X_test)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    preprocess(parser.parse_args())
