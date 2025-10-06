import unittest
from exercises.core_ex25 import (
    generate_data,
    split_data,
    train_model,
    evaluate_model,
)

class TestCoreEx25(unittest.TestCase):
    def test_generate_data_shape(self):
        X, y = generate_data(n_samples=100, n_features=5, noise=10.0)
        self.assertEqual(X.shape, (100, 5))
        self.assertEqual(y.shape, (100,))

    def test_split_data_ratio(self):
        X, y = generate_data(n_samples=100)
        X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.25)
        self.assertEqual(len(X_test), 25)
        self.assertEqual(len(y_test), 25)
        self.assertEqual(len(X_train), 75)
        self.assertEqual(len(y_train), 75)

    def test_train_model_type(self):
        X, y = generate_data()
        X_train, X_test, y_train, y_test = split_data(X, y)
        model = train_model(X_train, y_train)
        self.assertEqual(model.__class__.__name__, "LinearRegression")

    def test_evaluate_model_output(self):
        X, y = generate_data(noise=20.0)
        X_train, X_test, y_train, y_test = split_data(X, y)
        model = train_model(X_train, y_train)
        mse = evaluate_model(model, X_test, y_test)
        self.assertIsInstance(mse, float)
        self.assertGreaterEqual(mse, 0.0)
        self.assertLess(mse, 10000.0)

if __name__ == "__main__":
    unittest.main()