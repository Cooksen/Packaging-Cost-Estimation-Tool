"""train_linear_model.py
This module contains the function to train a Linear Regression model.
It saves the trained model to a specified path and returns the training loss and R² score.
"""

import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def train_linear_model(X, y, save_path):
    model = LinearRegression()
    model.fit(X.reshape(-1, 1), y)

    # 預測並計算 loss
    X = X.reshape(-1, 1)

    predictions = model.predict(X)
    loss = mean_squared_error(y, predictions)
    r2 = r2_score(y, predictions)

    print(f"Training loss (MSE): {loss:.4f}")

    # 儲存模型
    joblib.dump(model, save_path)
    print(f"Model saved to {save_path}")

    return loss, r2
