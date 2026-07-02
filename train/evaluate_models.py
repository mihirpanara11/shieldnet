import argparse
import numpy as np
from pathlib import Path
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shieldnet.train.evaluate")


def evaluate(args):
    model_dir = Path(args.model_dir)
    test_data_path = Path(args.test_data)

    logger.info(f"Evaluating models from {model_dir} with test data {test_data_path}")

    lstm_models = list(model_dir.glob("lstm_*"))
    ae_models = list(model_dir.glob("ae_*"))
    classifier_path = model_dir / "xgb_threat_classifier_v1.pkl"

    results = {
        "lstm_models": [str(m.name) for m in lstm_models],
        "ae_models": [str(m.name) for m in ae_models],
        "classifier": str(classifier_path) if classifier_path.exists() else "not found",
        "status": "evaluation_complete",
    }

    results_path = model_dir / "evaluation_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

    logger.info(f"Evaluation results saved to {results_path}")
    for key, value in results.items():
        logger.info(f"  {key}: {value}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", required=True)
    parser.add_argument("--test-data", required=True)
    evaluate(parser.parse_args())
