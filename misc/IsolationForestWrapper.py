from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import IsolationForest
import numpy as np

class IsolationForestWrapper(BaseEstimator, TransformerMixin):
    def __init__(self, n_estimators=100, max_features=1.0, contamination='auto', random_state=25):
        self.n_estimators = n_estimators
        self.max_features = max_features
        self.contamination = contamination
        self.random_state = random_state
        self.model = None

    def fit(self, X, y=None):
        self.model = IsolationForest(
            n_estimators=self.n_estimators,
            max_features=self.max_features,
            contamination=self.contamination,
            random_state=self.random_state
        )
        self.model.fit(X)
        return self

    def predict(self, X):
        preds = self.model.predict(X)
        # Map: 1 -> 'BENIGN', -1 -> 'ANOMALY'
        return np.where(preds == 1, 'BENIGN', 'ANOMALY')