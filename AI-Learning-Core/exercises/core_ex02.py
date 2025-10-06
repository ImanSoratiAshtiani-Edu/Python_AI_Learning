import pandas as pd

def core_ex02():
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    return df['B'].mean()
