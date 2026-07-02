import argparse
import numpy as np
import pandas as pd
from pathlib import Path
import joblib
from sklearn.ensemble import IsolationForest
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shieldnet.train.isolation_forest")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device_id", required=True)
    parser.add_argument("--baseline_data", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    logger.info(f"Initializing Isolation Forest for device {args.device_id}")
    df = pd.read_csv(args.baseline_data)
    X = df.values.astype(np.float32)
    n_samples = len(X)

    logger.info(f"Loaded {n_samples} baseline samples")

    model = IsolationForest(
        n_estimators=200,
        max_samples=min(256, n_samples),
        contamination=0.05,
        max_features=1.0,
        bootstrap=False,
        random_state=42,
    )
    model.fit(X)

    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)
    model_file = output_path / f"if_{args.device_id}.pkl"
    joblib.dump(model, model_file)
    logger.info(f"Isolation Forest model saved to {model_file}")


if __name__ == "__main__":
    main()
