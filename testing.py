from preprocessing import Preprocessing
import pickle 
import numpy as np
from sklearn.linear_model import LogisticRegression

X_train, y_train, X_test = Preprocessing(list(range(20,27)))()
model = LogisticRegression(class_weight = 'balanced')
model.fit(X_train[:, 3:], y_train)


def predictions(model: LogisticRegression, X_test: np.ndarray) -> list[str]:
    probs = model.predict_proba(X_test[:, 3:])[:, 1]
    indices = np.argsort(probs)[-15:]
    return X_test[indices[::-1], 0]

