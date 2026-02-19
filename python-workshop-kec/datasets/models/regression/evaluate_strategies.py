import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold, cross_validate
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.pipeline import Pipeline

# TODO: Replace with your actual student ID
STUDENT_ID = 1

def diagnostic_eda(csv_file):
    """Visualizes the regression data to predict model suitability."""
    analysis_png = f'{csv_file.split(".")[0]}_eda.png'
    df = pd.read_csv(csv_file)
    
    # We assume 'feat1' is our primary feature and 'target' is continuous
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # 1. Scatter Plot (Trend Analysis)
    sns.scatterplot(data=df, x='feat1', y='target', ax=axes[0], alpha=0.5)
    axes[0].set_title(f"Target vs Feature Trend: {csv_file}")
    
    # 2. Residual/Distribution Analysis (Density)
    sns.histplot(df['target'], kde=True, ax=axes[1], color='green')
    axes[1].set_title("Target Variable Distribution")
    
    plt.tight_layout()
    plt.savefig(analysis_png)
    plt.close() # Close to free up memory
    print(f"EDA visual saved to {analysis_png}")

def evaluate_model_ability(csv_file, model_type):
    """Evaluates intrinsic model abilities using a standard pipeline."""
    df = pd.read_csv(csv_file)
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Model Selection logic
    if model_type == 'linear':
        model = LinearRegression()
    elif model_type == 'knn':
        model = KNeighborsRegressor(n_neighbors=5)
    elif model_type == 'svm':
        model = SVR(kernel='rbf', C=1.0, epsilon=0.1)
    elif model_type == 'tree':
        model = DecisionTreeRegressor(random_state=STUDENT_ID)
    else:
        raise ValueError("Invalid model type.")

    # Pipeline with StandardScaler
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', model)
    ])

    cv = KFold(n_splits=5, shuffle=True, random_state=STUDENT_ID)
    cv_results = cross_validate(pipeline, X, y, cv=cv, scoring=['r2', 'neg_mean_squared_error'])
    
    return {
        'Model': model_type.upper(),
        'R²': float(cv_results['test_r2'].mean()),
        'MSE': float(-cv_results['test_neg_mean_squared_error'].mean())
    }

if __name__ == "__main__":
    # R² should be as close to 1 as possible
    # MSE should be as low as possible
    filename = 'data_1.csv'
    diagnostic_eda(csv_file=filename)
    # TODO: Keep changing model and document results in a table for your report
    # Models: linear, knn, svm, tree
    result = evaluate_model_ability(csv_file=filename, model_type='linear')
    print(result)