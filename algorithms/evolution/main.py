import numpy as np

from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from evolution import Evolution
X, y = make_regression(1000, 10, bias=0)

loss_function = lambda w: np.sum((X @ w - y) ** 2) / X.shape[0]
evolution = Evolution(max_iter=10_000, probability=0.5, alpha=1).fit(vector_size=X.shape[1], loss_function=loss_function)
reg = LinearRegression().fit(X, y)
print(mean_squared_error(y, X @ evolution.best))
print("Evolution weights", evolution.best)
print(mean_squared_error(y, reg.predict(X)))
print("Reg weights", reg.coef_)