import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import KFold, cross_validate, TimeSeriesSplit
from sklearn.impute import KNNImputer
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# TODO: Replace with your actual student ID
STUDENT_ID = 1

def diagnostic_eda(csv_file):
    analysis_png = f'{csv_file.split(".")[0]}_analysis.png'
    df = pd.read_csv(csv_file)

    rows_with_missing = df.isnull().any(axis=1).sum()
    total_rows = len(df)
    print({"Total Rows": total_rows, "Rows with Missing Values": int(rows_with_missing)})
    
    # Identify numeric columns for correlation and ACF
    numeric_df = df.select_dtypes(include=[np.number])
    target_col = 'target'
    features = [c for c in numeric_df.columns if c != target_col]
    
    fig, axes = plt.subplots(1, 2, figsize=(18, 5))
    
    # 1. Missingness Map
    sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap='viridis', ax=axes[0])
    axes[0].set_title("1. Missingness Pattern")
    

    # 3. Correlation Heatmap (Fixed the error here)
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=axes[1])
    axes[1].set_title("3. Correlation Matrix")
    
    plt.tight_layout()

    plt.savefig(analysis_png)

def evaluate_strategy(csv_file, strategy):
    # Load data
    df = pd.read_csv(csv_file)
    
    # 2. Handle Time Features
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        # Convert to ordinal so it's a numeric feature for KNN
        df['time_numeric'] = df['date'].map(pd.Timestamp.toordinal)
        df = df.sort_values('date') 
    
    # 3. Define Features and Target
    target_col = 'target'
    features_to_ignore = [target_col, 'date', 'time_index', 'time_numeric']
    feature_cols = [c for c in df.columns if c not in features_to_ignore]

    X = df[feature_cols]
    y = df[target_col]
    
    # Apply imputation strategy
    if strategy == 'drop':
        mask = X.notna().all(axis=1)
        X, y = X[mask], y[mask]
        
    elif strategy == 'mean':
        X = X.fillna(X.mean())
        
    elif strategy == 'median':
        X = X.fillna(X.median())
        
    elif strategy == 'knn':
        imputer = KNNImputer(n_neighbors=5)
        X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)
    
    elif strategy == 'ffill':
        X = X.ffill().bfill()
        
    elif strategy == 'bfill':
        X = X.bfill().ffill()
        
    else:
        raise ValueError(f"Unknown strategy: {strategy}")
    
    if 'date' in df.columns:
        cv_method = TimeSeriesSplit(n_splits=5)
    else:
        cv_method = KFold(n_splits=5, shuffle=True, random_state=STUDENT_ID)
    
    model = KNeighborsRegressor(n_neighbors=3)
    
    cv_results = cross_validate(
        model, X, y,
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
    # RAE means how far off the predictions are from the actual values, so lower is better
    filename = 'data_1.csv'
    diagnostic_eda(csv_file=filename)
    # TODO : Keep changing strategy and document results in a table for your report
    # Strategies : drop, mean, median, knn, ffill, bfill
    result = evaluate_strategy(csv_file=filename, strategy='mean')
    print(result)
