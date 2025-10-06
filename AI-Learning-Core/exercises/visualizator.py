import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_all(X, y=None, target_name=None):
    print("🔍 Starting data exploration...")

    # Convert X to DataFrame if needed
    if isinstance(X, np.ndarray):
        X = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(X.shape[1])])

    # Handle y if provided
    if y is not None:
        if isinstance(y, np.ndarray):
            target_name = target_name or 'target'
            y = pd.Series(y, name=target_name)
        elif isinstance(y, pd.DataFrame):
            y = y.squeeze()
            target_name = target_name or y.name or 'target'
        elif isinstance(y, pd.Series):
            target_name = target_name or y.name or 'target'
            y.name = target_name
        else:
            raise TypeError("y must be a NumPy array, Pandas Series, or single-column DataFrame")

        df = X.copy()
        df[target_name] = y
    else:
        df = X.copy()

    # Identify numeric and categorical columns
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'bool', 'category']).columns.tolist()

    # Remove target from numeric if present
    if target_name in numeric_cols:
        numeric_cols.remove(target_name)

    # 1. Histograms
    df[numeric_cols].hist(figsize=(12, 8), bins=20)
    plt.suptitle("Histograms of Numeric Features")
    plt.tight_layout()
    plt.show()

    # 2. KDE plots
    for col in numeric_cols:
        sns.kdeplot(df[col], shade=True)
        plt.title(f"KDE Plot: {col}")
        plt.xlabel(col)
        plt.show()

    # 3. Boxplot
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df[numeric_cols])
    plt.title("Boxplot of Numeric Features")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # 4. Correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.show()

    # 5. Countplots for categorical features
    for col in categorical_cols:
        sns.countplot(x=col, data=df)
        plt.title(f"Countplot: {col}")
        plt.xticks(rotation=45)
        plt.show()

    # 6. Pairplot
    if y is not None and target_name in df.columns:
        sns.pairplot(df, hue=target_name)
        plt.suptitle("Pairplot Colored by Target", y=1.02)
        plt.show()
    else:
        sns.pairplot(df)
        plt.suptitle("Pairplot Without Target Coloring", y=1.02)
        plt.show()

    # 7. Violin plots
    if y is not None and target_name in df.columns:
        for col in numeric_cols:
            sns.violinplot(x=target_name, y=col, data=df)
            plt.title(f"Violin Plot: {col} by {target_name}")
            plt.show()

    print("✅ Data exploration complete.")
    '''
    from visualizator import visualize_all

     
    or
    visualize_all(X_np, y_np, target_name='passed')
    or 
    visualize_all(X)


    
    '''