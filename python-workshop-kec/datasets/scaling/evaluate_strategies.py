import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from sklearn.model_selection import KFold, cross_validate
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt
import seaborn as sns

# TODO: Replace with your actual student ID
STUDENT_ID = 1

def diagnostic_eda(csv_file):
    analysis_png = f'{csv_file.split(".")[0]}_analysis.png'
    df = pd.read_csv(csv_file)
    
    target_col = 'target'
    numeric_df = df.select_dtypes(include=[np.number])
    features = [c for c in numeric_df.columns if c != target_col]
    
    fig, axes = plt.subplots(1, 1, figsize=(18, 5))
    
    # 1. Feature Scale Comparison
    df[features].boxplot(ax=axes)
    axes.set_title("1. Feature Scales (Before Scaling)")
    axes.set_ylabel("Value")
    axes.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(analysis_png)

def evaluate_strategy(csv_file, strategy):
    """
    Applies scaling and evaluates model performance.
    Strategies: 'none', 'minmax', 'standard', 'robust'
    """
    # Load data
    df = pd.read_csv(csv_file)
    
    target_col = 'target'
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    
    # Apply scaling
    if strategy == 'none':
        X_scaled = X.copy()
        
    elif strategy == 'minmax':
        scaler = MinMaxScaler()
        X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
        
    elif strategy == 'standard':
        scaler = StandardScaler()
        X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
        
        
    else:
        raise ValueError("Strategy must be 'none', 'minmax', or 'standard'")
    
    # KNN is EXTREMELY sensitive to feature scaling
    # Distance calculation: sqrt((x1-y1)² + (x2-y2)² + ...)
    # Large-scale features dominate without scaling
    cv_method = KFold(n_splits=5, shuffle=True, random_state=STUDENT_ID)
    model = KNeighborsRegressor(n_neighbors=5)
    
    cv_results = cross_validate(
        model, X_scaled, y,
        cv=cv_method,
        scoring=['r2', 'neg_mean_squared_error', 'neg_mean_absolute_error'],
        return_train_score=False
    )
    
    result = {
        'Strategy': strategy,
        'R²': float(cv_results['test_r2'].mean()),
        'MSE': float(-cv_results['test_neg_mean_squared_error'].mean()),
        'MAE': float(-cv_results['test_neg_mean_absolute_error'].mean()),
    }
    return result


if __name__ == "__main__":
    # R² should be as close to 1 as possible
    # MSE and MAE should be as low as possible
    filename = 'data_2.csv'
    diagnostic_eda(csv_file=filename)
    # TODO: Keep changing strategy and document results in a table for your report
    # Strategies: none, minmax, standard
    result = evaluate_strategy(csv_file=filename, strategy='minmax')
    print(result)