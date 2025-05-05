import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.neural_network import MLPRegressor

class AutoencoderAnomaly(BaseEstimator, ClassifierMixin):
    def __init__(self):
        self.model = None
        self.threshold = None

    def fit(self, X, y=None):
        self.model = MLPRegressor(hidden_layer_sizes=(X.shape[1]*2, X.shape[1]), max_iter=200)
        self.model.fit(X, X)
        recon = self.model.predict(X)
        # Torna o threshold mais exigente (percentil 99)
        self.threshold = np.percentile(np.mean((X - recon) ** 2, axis=1), 99)
        return self

    def predict(self, X):
        recon = self.model.predict(X)
        errors = np.mean((X - recon) ** 2, axis=1)
        return np.where(errors > self.threshold, -1, 1)
