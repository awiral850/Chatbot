import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import make_scorer, precision_score, recall_score, f1_score

# TODO: Replace with your actual student ID
STUDENT_ID = 1

def diagnostic_eda(csv_file):
    """Visualizes classification clusters to predict model suitability."""
    analysis_png = f'{csv_file.split(".")[0]}_eda.png'
    df = pd.read_csv(csv_file)
    
    # Classification EDA usually requires looking at feature interactions
    # We assume 'feat1' and 'feat2' are the coordinates
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='feat1', y='feat2', hue='target', palette='bright', alpha=0.6)
    plt.title(f"Class Distribution and Geometry: {csv_file}")
    
    plt.tight_layout()
    plt.savefig(analysis_png)
    plt.close()
    print(f"EDA visual saved to {analysis_png}")

def evaluate_model_ability(csv_file, model_type):
    """Evaluates intrinsic classification abilities using a standard pipeline."""
    df = pd.read_csv(csv_file)
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Model Selection logic for Classification
    if model_type == 'logistic':
        model = LogisticRegression(random_state=STUDENT_ID)
    elif model_type == 'knn':
        model = KNeighborsClassifier(n_neighbors=5)
    elif model_type == 'svm':
        # SVC is the classifier version of SVR
        model = SVC(kernel='rbf', C=1.0, random_state=STUDENT_ID)
    elif model_type == 'tree':
        model = DecisionTreeClassifier(random_state=STUDENT_ID)
    else:
        raise ValueError("Invalid model type. Choose: logistic, knn, svm, tree")

    # Pipeline with StandardScaler (Essential for KNN and SVM)
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', model)
    ])

    # StratifiedKFold is better for classification as it preserves class proportions
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=STUDENT_ID)
    scoring = {
        'accuracy': 'accuracy',
        'precision': make_scorer(precision_score, zero_division=0),
        'recall': make_scorer(recall_score, zero_division=0),
        'f1': make_scorer(f1_score, zero_division=0)
    }
    cv_results = cross_validate(pipeline, X, y, cv=cv, scoring=scoring)
    
    return {
        'filename': csv_file,
        'Model': model_type.upper(),
        'Accuracy': float(cv_results['test_accuracy'].mean()),
        'Precision': float(cv_results['test_precision'].mean()),
        'Recall': float(cv_results['test_recall'].mean()),
        'F1_Score': float(cv_results['test_f1'].mean())
    }

if __name__ == "__main__":
    # Accuracy and F1_Score should be as close to 1 as possible
    # Change the filename to data_4, data_5, data_6, or data_7 as needed
    filename = 'data_4.csv' 
    
    diagnostic_eda(csv_file=filename)
    
    # TODO: Keep changing model and document results in a table for your report
    # Models: logistic, knn, svm, tree
    result = evaluate_model_ability(csv_file=filename, model_type='logistic')
    print(result)