from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from visualizator import visualize_all


import numpy as np
def generate_data(n_samples=600, n_features=6, noise=0.1, random_state=42):
    X,y = make_regression(n_samples=n_samples, n_features=n_features, noise=noise, random_state=random_state)
    return X,y


def split_data(X,y,test_size=.2, random_state=42):
    return train_test_split(X,y,test_size=test_size, random_state=random_state)
def train_model(X_train, y_train):
    model =LinearRegression()
    model.fit(X_train, y_train)
    return model
def evaluate_model(model, X_test, y_test):
    y_pred= model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    return mse
def core_ex25():
    if __name__=="__main__":
        X,y=generate_data(noise=15.0)
        visualize_all(X, y)
        X_train, y_train, X_test, y_test = split_data(X,y)
        model = train_model(X_train, y_train)
        mse = evaluate_model(model, X_test, y_test)
    return mse
core_ex25()