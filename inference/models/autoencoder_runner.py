from typing import Optional
import numpy as np


class AutoencoderRunner:
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self._model = None
        self._training_mse = []
        self._threshold = 0.1

    def load_model(self, model_path: str):
        try:
            import tensorflow as tf
            self._model = tf.keras.models.load_model(model_path)
            self.model_path = model_path
        except ImportError:
            self._model = None
        except Exception:
            self._model = None

    def load_weights(self, weights: list):
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
        self._model = model

    def fit(self, X_train: np.ndarray, epochs: int = 100, batch_size: int = 128):
        import tensorflow as tf
        if self._model is None:
            self._build_model()
        X_train_reshaped = X_train.reshape(-1, 47, 1)
        self._model.fit(
            X_train_reshaped, X_train_reshaped,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.15,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True),
            ],
            verbose=0,
        )
        reconstructed = self._model.predict(X_train_reshaped, verbose=0)
        mse_per_sample = np.mean((X_train_reshaped - reconstructed) ** 2, axis=(1, 2))
        self._training_mse = mse_per_sample.tolist()
        mean_mse = float(np.mean(mse_per_sample))
        std_mse = float(np.std(mse_per_sample))
        self._threshold = mean_mse + 2 * std_mse

    def predict(self, feature_vector: np.ndarray) -> float:
        if self._model is None:
            return 0.0
        x = feature_vector.reshape(1, 47, 1).astype(np.float32)
        reconstructed = self._model.predict(x, verbose=0)
        mse = float(np.mean((x - reconstructed) ** 2))
        threshold_effective = max(self._threshold, 0.01)
        score = min(mse / (threshold_effective * 3), 1.0)
        return score

    def get_weights(self) -> Optional[list]:
        if self._model is not None:
            return self._model.get_weights()
        return None

    @property
    def is_loaded(self) -> bool:
        return self._model is not None
