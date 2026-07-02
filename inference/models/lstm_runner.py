from typing import Optional, List
import numpy as np


class LSTMRunner:
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self._model = None
        self._sequence: List[np.ndarray] = []
        self.max_sequence_length = 60

    def load_model(self, model_path: str):
        try:
            import tensorflow as tf
            self._model = tf.keras.models.load_model(model_path)
            self.model_path = model_path
        except ImportError:
            self._model = None
        except Exception:
            self._model = None

    def load_weights(self, weights: List[np.ndarray]):
        try:
            import tensorflow as tf
            if self._model is None:
                self._build_model()
            self._model.set_weights(weights)
        except ImportError:
            pass

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
        ], name='shieldnet_lstm')
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy', keras.metrics.AUC(name='auc')],
        )
        self._model = model

    def add_features(self, feature_vector: np.ndarray):
        self._sequence.append(feature_vector)
        if len(self._sequence) > self.max_sequence_length:
            self._sequence = self._sequence[-self.max_sequence_length:]

    def predict(self, feature_vector: np.ndarray) -> float:
        self.add_features(feature_vector)
        if len(self._sequence) < self.max_sequence_length:
            return 0.0
        import tensorflow as tf
        sequence = np.array(self._sequence[-self.max_sequence_length:])
        sequence = sequence.reshape(1, self.max_sequence_length, 47)
        sequence = sequence.astype(np.float32)
        if self._model is None:
            return 0.0
        pred = self._model.predict(sequence, verbose=0)
        return float(pred[0][0])

    def predict_on_sequence(self, sequence: np.ndarray) -> float:
        if sequence.shape != (1, 60, 47):
            sequence = sequence.reshape(1, 60, 47)
        sequence = sequence.astype(np.float32)
        if self._model is None:
            return 0.0
        pred = self._model.predict(sequence, verbose=0)
        return float(pred[0][0])

    def get_weights(self) -> Optional[List[np.ndarray]]:
        if self._model is not None:
            return self._model.get_weights()
        return None

    @property
    def is_loaded(self) -> bool:
        return self._model is not None
