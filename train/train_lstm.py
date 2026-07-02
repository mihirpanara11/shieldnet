import argparse
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import roc_auc_score, f1_score, classification_report
from pathlib import Path
import json


def build_lstm_model(input_shape=(60, 47)):
    model = keras.Sequential([
        keras.layers.Input(shape=input_shape),
        keras.layers.LSTM(128, return_sequences=True, dropout=0.2, recurrent_dropout=0.1),
        keras.layers.LSTM(64, return_sequences=False, dropout=0.2),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(16, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid'),
    ], name='shieldnet_lstm')

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy', keras.metrics.AUC(name='auc'),
                 keras.metrics.Precision(name='precision'),
                 keras.metrics.Recall(name='recall')],
    )
    return model


def train(args):
    print(f"Training LSTM for category: {args.category}")
    import h5py

    with h5py.File(args.dataset, 'r') as f:
        group = f[args.category]
        X_train = group['X_train'][:]
        y_train = group['y_train'][:]
        X_val = group['X_val'][:]
        y_val = group['y_val'][:]
        X_test = group['X_test'][:]
        y_test = group['y_test'][:]

    print(f"  Train: {len(X_train)} | Val: {len(X_val)} | Test: {len(X_test)}")
    print(f"  Attack ratio train: {y_train.mean():.2%}")

    model = build_lstm_model()
    model.summary()

    callbacks = [
        keras.callbacks.EarlyStopping(monitor='val_auc', patience=10, mode='max', restore_best_weights=True),
        keras.callbacks.ModelCheckpoint(filepath=f"{args.output}/checkpoint.keras", save_best_only=True, monitor='val_auc', mode='max'),
        keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6),
        keras.callbacks.CSVLogger(f"{args.output}/training_log.csv"),
    ]

    neg, pos = np.bincount(y_train.astype(int))
    class_weight = {0: 1.0, 1: neg / pos}
    print(f"  Class weights: {class_weight}")

    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=args.epochs,
        batch_size=args.batch_size,
        class_weight=class_weight,
        callbacks=callbacks,
        verbose=1,
    )

    y_pred_prob = model.predict(X_test, batch_size=256).flatten()
    y_pred = (y_pred_prob >= 0.5).astype(int)

    auc = roc_auc_score(y_test, y_pred_prob)
    f1 = f1_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=['Normal', 'Attack'])

    print(f"\nTEST RESULTS - {args.category}")
    print(f"AUC-ROC : {auc:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print(report)

    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)
    model.save(output_path / f"lstm_{args.category}_v1.keras")

    metadata = {
        "category": args.category,
        "input_shape": [60, 47],
        "auc_roc": float(auc),
        "f1_score": float(f1),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "epochs_trained": len(history.history['loss']),
        "threshold": 0.5,
        "model_type": "LSTM",
    }
    with open(output_path / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"Model saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", required=True,
                        choices=["traffic", "camera", "energy", "water",
                                 "emergency", "environmental", "other"])
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--output", required=True)
    train(parser.parse_args())
