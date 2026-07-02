import numpy as np
from typing import List, Optional, Tuple
import logging

logger = logging.getLogger("shieldnet.fl.local_trainer")


class LocalTrainer:
    def __init__(self, local_epochs: int = 3, batch_size: int = 64):
        self.local_epochs = local_epochs
        self.batch_size = batch_size
        self._model = None

    def _build_model(self):
        import tensorflow as tf
        from tensorflow import keras
        model = keras.Sequential([
            keras.layers.Input(shape=(60, 47)),
            keras.layers.LSTM(128, return_sequences=True, dropout=0.2, recurrent_dropout=0.1),
            keras.layers.LSTM(64, return_sequences=False, dropout=0.2),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dense(1, activation='sigmoid'),
        ], name='shieldnet_lstm_fl')
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy', keras.metrics.AUC(name='auc')],
        )
        self._model = model

    def set_weights(self, weights: List[np.ndarray]):
        if self._model is None:
            self._build_model()
        self._model.set_weights(weights)

    def get_weights(self) -> Optional[List[np.ndarray]]:
        if self._model is not None:
            return self._model.get_weights()
        return None

    def train(self, X_train: np.ndarray, y_train: np.ndarray,
              X_val: Optional[np.ndarray] = None,
              y_val: Optional[np.ndarray] = None) -> dict:
        if self._model is None:
            self._build_model()

        validation_data = None
        if X_val is not None and y_val is not None:
            validation_data = (X_val, y_val)

        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss' if validation_data else 'loss',
                patience=3, restore_best_weights=True),
        ]

        history = self._model.fit(
            X_train, y_train,
            validation_data=validation_data,
            epochs=self.local_epochs,
            batch_size=self.batch_size,
            callbacks=callbacks,
            verbose=0,
        )

        loss = float(history.history['loss'][-1])
        auc = float(history.history.get('auc', [0.0])[-1])
        return {
            "loss": loss,
            "auc": auc,
            "samples": len(X_train),
        }
