import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.neural_network import MLPRegressor

class EnsembleAnomalyDetector:
    def __init__(self, scaler, iso, svm, ae):
        self.scaler = scaler
        self.iso = iso
        self.svm = svm
        self.ae = ae
        self.meta = None

    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        preds = np.vstack([
            self.iso.predict(X_scaled),
            self.svm.predict(X_scaled),
            self.ae.predict(X_scaled)
        ])
        # Só considera anomalia se TODOS os modelos concordarem (unanimidade)
        y_pred = np.where(np.all(preds == -1, axis=0), -1, 1)
        return y_pred