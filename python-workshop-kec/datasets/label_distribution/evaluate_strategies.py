import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    make_scorer,
    f1_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
)
from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline

# TODO: Replace with your actual student ID
STUDENT_ID = 1


def diagnostic_eda(csv_file):
    analysis_png = f'{csv_file.split(".")[0]}_analysis.png'
    df = pd.read_csv(csv_file)

    fig, axes = plt.subplots(1, 2, figsize=(18, 6))

    # 1. Class Distribution
    sns.countplot(
        x="target", hue="target", data=df, ax=axes[0], palette="viridis", legend=False
    )
    axes[0].set_title("1. Class Distribution (Imbalance Check)")

    # 2. Geometric Distribution (Scatter Plot)
    # This helps decide between SMOTE (clean clusters) and Weights (overlap)
    sns.scatterplot(x="feat1", y="feat2", hue="target", data=df, ax=axes[1], alpha=0.6)
    axes[1].set_title("2. Feature Space (Overlap Check)")

    plt.tight_layout()
    plt.savefig(analysis_png)
    print(f"EDA saved to {analysis_png}")


def evaluate_strategy(csv_file, strategy):
    """
    Applies imbalance handling and evaluates classification performance.
    Strategies: 'none', 'under', 'over', 'smote', 'weights'
    """
    df = pd.read_csv(csv_file)
    X = df.drop("target", axis=1)
    y = df["target"]

    # Define Model (Logistic Regression is sensitive to imbalance)
    # For 'weights', we use the built-in class_weight parameter
    if strategy == "weights":
        model = LogisticRegression(class_weight="balanced", random_state=STUDENT_ID)
        steps = [("model", model)]
    else:
        model = LogisticRegression(random_state=STUDENT_ID)

        # Define Samplers
        if strategy == "none":
            steps = [("model", model)]
        elif strategy == "under":
            steps = [
                ("sampler", RandomUnderSampler(random_state=STUDENT_ID)),
                ("model", model),
            ]
        elif strategy == "over":
            steps = [
                ("sampler", RandomOverSampler(random_state=STUDENT_ID)),
                ("model", model),
            ]
        elif strategy == "smote":
            steps = [
                ("sampler", SMOTE(random_state=STUDENT_ID, k_neighbors=2)),
                ("model", model),
            ]
        else:
            raise ValueError(
                "Strategy must be 'none', 'under', 'over', 'smote', or 'weights'"
            )

    # Create Pipeline (Essential to prevent leakage: only resample the training fold)
    clf_pipeline = Pipeline(steps=steps)

    cv_method = StratifiedKFold(n_splits=5, shuffle=True, random_state=STUDENT_ID)

    # Scoring metrics for imbalance
    scoring = {
        "precision": make_scorer(
            precision_score, zero_division=0
        ),  # When I predicted minority, how often was I right?
        "recall": make_scorer(
            recall_score, zero_division=0
        ),  # Of all the actual minority points, how many did I find?
        "f1": make_scorer(f1_score),
        "balanced_acc": make_scorer(balanced_accuracy_score),
    }

    cv_results = cross_validate(
        clf_pipeline, X, y, cv=cv_method, scoring=scoring, return_train_score=False
    )

    return {
        "Strategy": strategy,
        "F1-Score": float(cv_results["test_f1"].mean()),
        "Precision": float(cv_results["test_precision"].mean()),
        "Recall": float(cv_results["test_recall"].mean()),
        "Balanced Accuracy": float(cv_results["test_balanced_acc"].mean()),
    }


if __name__ == "__main__":
    # Test on one of the imbalanced datasets
    filename = "data_1.csv"
    diagnostic_eda(csv_file=filename)
    # Strategies: none, under, over, smote, weights
    result = evaluate_strategy(csv_file=filename, strategy="smote")
    print(result)
