import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
from visualizator import visualize_all


def generate_data(n=100):
    np.random.seed(42)
    df = pd.DataFrame({
        'hours_studied': np.random.normal(10, 3, n).clip(0),
        'attendance_rate': np.random.uniform(30, 100, n),       #درصد حضور در کلاس‌ها
        'homework_score': np.random.uniform(30, 100, n),        # میانگین نمره تمرین‌های خانه
        'previous_exam_score': np.random.uniform(20, 100, n),   # نمره امتحان قبلی
        'parental_support': np.random.choice([0, 1, 2], n, p=[0.3, 0.5, 0.2]),  # 0: کم، 1: متوسط، 2: زیاد  
        'extracurricular': np.random.choice([True, False], n)       # آیا در فعالیت‌های فوق برنامه شرکت می‌کند؟
    })
    # تابع ساده برای تولید برچسب قبولی
    def predict_pass(row):
        score = (                   
            row['hours_studied'] * 0.3 +
            row['attendance_rate'] * 0.2 +
            row['homework_score'] * 0.2 +
            row['previous_exam_score'] * 0.2 +
            row['parental_support'] * 5 +
            (5 if row['extracurricular'] else 0)
        )
        print(score)
        return int(score > 50)  # آستانه قبولی 50 است
    df['passed'] = df.apply(predict_pass, axis=1)
    X = df.drop(columns=['passed'])
    y = df['passed']
    print("generate_data: OK")
    return X, y

def split_data(X, y, test_size=.2, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
    print("split_data: OK")
    print(y_train.value_counts())
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    model = LogisticRegression(max_iter=100)
    model.fit(X_train, y_train)
    print("train_model: OK")
    return model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    matrix = confusion_matrix(y_test, y_pred)
    print("evaluate_model: OK")
    return y_pred, accuracy, report, matrix
def visualize_results(y_pred, y_test, matrix, accuracy, report):
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.scatter(range(len(y_test)), y_test, label='Actual', alpha=0.7, color='blue', marker='X')
    plt.scatter(range(len(y_pred)), y_pred, label='Predicted', alpha=0.7, color='orange', marker='o')
    plt.title('Actual vs Predicted')
    plt.xlabel('Sample Index')
    plt.ylabel('Passed (1) / Failed (0)')
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.imshow(matrix, cmap='Blues', interpolation='nearest')
    plt.title(f'Confusion Matrix (Accuracy: {accuracy:.2f})')
    plt.colorbar()
    plt.xticks([0, 1], ['Failed', 'Passed'])
    plt.yticks([0, 1], ['Failed', 'Passed'])
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            plt.text(j, i, matrix[i, j], ha='center', va='center', color='red')
    plt.tight_layout()
    plt.show()

def core_ex26():
    if __name__ == "__main__":
        X, y = generate_data(1000)
        visualize_all(X, y, target_name='passed')
        X_train, X_test, y_train, y_test = split_data(X, y)
        model = train_model(X_train, y_train)
        y_pred, accuracy, report, matrix = evaluate_model(model, X_test, y_test)
        visualize_results(y_pred, y_test, matrix, accuracy, report )
core_ex26()