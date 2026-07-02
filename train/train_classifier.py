import argparse
import numpy as np
import pandas as pd
from pathlib import Path
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shieldnet.train.classifier")


def train(args):
    logger.info(f"Training XGBoost threat classifier on {args.dataset}")
    df = pd.read_csv(args.dataset)

    feature_cols = [c for c in df.columns if c.startswith('F') and c != 'F_label']
    label_col = 'F_label'

    X = df[feature_cols].values.astype(np.float32)
    y = df[label_col].values.astype(int)

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    logger.info(f"Train: {len(X_train)}, Test: {len(X_test)}, Classes: {np.unique(y)}")

    import xgboost as xgb
    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=8,
        learning_rate=0.1,
        objective='multi:softprob',
        num_class=7,
        random_state=42,
        eval_metric='mlogloss',
    )

    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=False,
    )

    from sklearn.metrics import accuracy_score, classification_report
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    logger.info(f"Test accuracy: {acc:.4f}")
    logger.info(f"\n{report}")

    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)
    import joblib
    model_path = output_path / "xgb_threat_classifier_v1.pkl"
    joblib.dump(model, model_path)

    metadata = {
        "model_type": "XGBoost",
        "num_classes": 7,
        "num_features": len(feature_cols),
        "test_accuracy": float(acc),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
    }
    with open(output_path / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    logger.info(f"Model saved to {model_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--output", required=True)
    train(parser.parse_args())
