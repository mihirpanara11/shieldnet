import argparse
import numpy as np
import tensorflow as tf
from tensorflow import keras
from pathlib import Path
import json


def build_autoencoder():
    encoder_input = keras.layers.Input(shape=(47, 1))
    x = keras.layers.Conv1D(32, 3, activation='relu', padding='same')(encoder_input)
    x = keras.layers.MaxPooling1D(2)(x)
    x = keras.layers.Conv1D(16, 3, activation='relu', padding='same')(x)
    x = keras.layers.MaxPooling1D(2)(x)
    x = keras.layers.Flatten()(x)
    x = keras.layers.Dense(32, activation='relu')(x)
    bottleneck = keras.layers.Dense(16, activation='relu', name='bottleneck')(x)
    x = keras.layers.Dense(32, activation='relu')(bottleneck)
    x = keras.layers.Dense(176, activation='relu')(x)
    x = keras.layers.Reshape((11, 16))(x)
    x = keras.layers.UpSampling1D(2)(x)
    x = keras.layers.Conv1DTranspose(16, 3, activation='relu', padding='same')(x)
    x = keras.layers.UpSampling1D(2)(x)
    x = keras.layers.Conv1DTranspose(32, 3, activation='relu', padding='same')(x)
    x = keras.layers.Conv1DTranspose(1, 3, activation='linear', padding='same')(x)
    x = keras.layers.Flatten()(x)
    output = keras.layers.Dense(47, activation='linear')(x)
    model = keras.Model(inputs=encoder_input, outputs=output, name='shieldnet_ae')
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001), loss='mse')
    return model


def train(args):
    print(f"Training Autoencoder for category: {args.category}")
    import pandas as pd

    df = pd.read_csv(args.dataset)
    X = df.values.astype(np.float32)
    print(f"  Samples: {len(X)}, Features: {X.shape[1]}")

    model = build_autoencoder()
    model.summary()

    X_reshaped = X.reshape(-1, 47, 1)

    callbacks = [
        keras.callbacks.EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6),
        keras.callbacks.CSVLogger(f"{args.output}/training_log.csv"),
    ]

    history = model.fit(
        X_reshaped, X_reshaped,
        epochs=args.epochs,
        batch_size=args.batch_size,
        validation_split=0.15,
        callbacks=callbacks,
        verbose=1,
    )

    reconstructed = model.predict(X_reshaped, verbose=0)
    mse_per_sample = np.mean((X_reshaped - reconstructed) ** 2, axis=(1, 2))
    mean_mse = float(np.mean(mse_per_sample))
    std_mse = float(np.std(mse_per_sample))
    threshold = mean_mse + 2 * std_mse

    print(f"\nTraining MSE: mean={mean_mse:.6f}, std={std_mse:.6f}")
    print(f"Anomaly threshold: {threshold:.6f}")

    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)
    model.save(output_path / f"ae_{args.category}_v1.keras")

    metadata = {
        "category": args.category,
        "input_shape": [47, 1],
        "mean_mse": mean_mse,
        "std_mse": std_mse,
        "threshold": threshold,
        "train_samples": len(X),
        "epochs_trained": len(history.history['loss']),
        "model_type": "ConvAutoencoder",
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
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch_size", type=int, default=128)
    parser.add_argument("--output", required=True)
    train(parser.parse_args())
