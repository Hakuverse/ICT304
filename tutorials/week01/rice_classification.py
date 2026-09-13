"""
ICT304 Tutorial 1 - Question 5
Rice Grain Classification: Cammeo vs Osmancik

This script trains and evaluates machine learning models that classify
rice grains into one of two species (Cammeo, Osmancik) using 7 morphological
features extracted from grain images.

Dataset source:
Cinar, I. and Koklu, M. (2019). Classification of Rice Varieties Using
Artificial Intelligence Methods. International Journal of Intelligent
Systems and Applications in Engineering, 7(3), 188-194.
https://doi.org/10.18201/ijisae.2019355381
Data: https://archive.ics.uci.edu/ml/datasets/Rice+%28Cammeo+and+Osmancik%29

How to run:
    1. Install Python 3.9+ and the packages listed in requirements.txt
       (pip install -r requirements.txt)
    2. Put Rice_Cammeo_Osmancik.arff in the same folder as this script
    3. Run:  python rice_classification.py
    4. Results print to the console and are also saved to results.txt,
       confusion_matrices.png and feature_importance.png
"""

import time
import numpy as np
import pandas as pd
from scipy.io import arff

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score
)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RANDOM_STATE = 42

# ---------------------------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------------------------
data, meta = arff.loadarff("Rice_Cammeo_Osmancik.arff")
df = pd.DataFrame(data)
# Class column comes back as bytes (b'Cammeo') from scipy's arff reader -> decode
df["Class"] = df["Class"].str.decode("utf-8")

print("=" * 70)
print("STEP 1: DATASET OVERVIEW")
print("=" * 70)
print(f"Shape: {df.shape[0]} rows (rice grains), {df.shape[1]} columns")
print("\nFirst 5 rows:")
print(df.head())
print("\nClass balance:")
print(df["Class"].value_counts())
print(f"\nClass balance (%):\n{df['Class'].value_counts(normalize=True) * 100}")
print("\nMissing values per column:")
print(df.isnull().sum())
print("\nDescriptive statistics:")
print(df.describe().T)

# ---------------------------------------------------------------------------
# 2. PRE-PROCESSING
# ---------------------------------------------------------------------------
# a) Separate features (X) and target label (y)
X = df.drop(columns=["Class"])
y = df["Class"]

# b) Encode the text label (Cammeo / Osmancik) into 0 / 1 for the models
le = LabelEncoder()
y_encoded = le.fit_transform(y)  # Cammeo -> 0, Osmancik -> 1 (alphabetical)
print(f"\nLabel encoding: {dict(zip(le.classes_, le.transform(le.classes_)))}")

# c) Train / test split - stratified so both classes keep their ~57/43 ratio
#    in both the training set and the test set
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.20, random_state=RANDOM_STATE, stratify=y_encoded
)
print(f"\nTraining rows: {len(X_train)} | Test rows: {len(X_test)}")

# d) Feature scaling - REQUIRED here because the 7 features are on very
#    different numeric scales (e.g. Area ~ 10,000-19,000 pixels vs
#    Eccentricity ~ 0.4-0.99). Distance-based models (KNN, SVM) and
#    gradient-based models (Logistic Regression) are sensitive to this,
#    so we standardise every feature to mean=0, std=1 using ONLY the
#    training data statistics (to avoid data leakage from the test set).
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ---------------------------------------------------------------------------
# 3. MODEL TRAINING - we compare 4 candidate algorithms
# ---------------------------------------------------------------------------
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
    "K-Nearest Neighbors (k=5)": KNeighborsClassifier(n_neighbors=5),
    "Support Vector Machine (RBF)": SVC(kernel="rbf", probability=True, random_state=RANDOM_STATE),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE),
}

results = []
fitted_models = {}
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

print("\n" + "=" * 70)
print("STEP 2: TRAIN & EVALUATE EACH MODEL")
print("=" * 70)

for name, model in models.items():
    t0 = time.time()
    model.fit(X_train_scaled, y_train)
    train_time = time.time() - t0

    y_pred = model.predict(X_test_scaled)
    y_proba = model.predict_proba(X_test_scaled)[:, 1] if hasattr(model, "predict_proba") else None

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba) if y_proba is not None else np.nan

    # 5-fold cross-validation on the training set (more robust accuracy estimate)
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=skf, scoring="accuracy")

    results.append({
        "Model": name,
        "Test Accuracy": acc,
        "Precision": prec,
        "Recall": rec,
        "F1-score": f1,
        "ROC-AUC": auc,
        "5-fold CV Accuracy (mean)": cv_scores.mean(),
        "5-fold CV Accuracy (std)": cv_scores.std(),
        "Train time (s)": train_time,
    })
    fitted_models[name] = (model, y_pred)

    print(f"\n--- {name} ---")
    print(f"Test Accuracy : {acc:.4f}")
    print(f"Precision     : {prec:.4f}")
    print(f"Recall        : {rec:.4f}")
    print(f"F1-score      : {f1:.4f}")
    print(f"ROC-AUC       : {auc:.4f}")
    print(f"5-fold CV Acc : {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    print("Confusion matrix ([[TN,FP],[FN,TP]]):")
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred, target_names=le.classes_))

results_df = pd.DataFrame(results).sort_values("Test Accuracy", ascending=False)
print("\n" + "=" * 70)
print("STEP 3: MODEL COMPARISON SUMMARY (sorted by test accuracy)")
print("=" * 70)
print(results_df.to_string(index=False))

best_model_name = results_df.iloc[0]["Model"]
print(f"\nBest performing model: {best_model_name}")

# ---------------------------------------------------------------------------
# 4. SAVE OUTPUTS
# ---------------------------------------------------------------------------
results_df.to_csv("model_comparison_results.csv", index=False)

with open("results.txt", "w") as f:
    f.write("ICT304 Tutorial 1 - Q5 Rice Classification Results\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Dataset: {df.shape[0]} rows, class balance:\n{df['Class'].value_counts().to_string()}\n\n")
    f.write(results_df.to_string(index=False))
    f.write(f"\n\nBest performing model: {best_model_name}\n")

# Confusion matrix plots for all 4 models
fig, axes = plt.subplots(1, 4, figsize=(20, 5))
for ax, (name, (model, y_pred)) in zip(axes, fitted_models.items()):
    cm = confusion_matrix(y_test, y_pred)
    im = ax.imshow(cm, cmap="Blues")
    ax.set_title(name, fontsize=10)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_xticks([0, 1]); ax.set_xticklabels(le.classes_)
    ax.set_yticks([0, 1]); ax.set_yticklabels(le.classes_)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha="center", va="center",
                     color="white" if cm[i, j] > cm.max() / 2 else "black")
plt.tight_layout()
plt.savefig("confusion_matrices.png", dpi=150)
plt.close()

# Feature importance from Random Forest (helps answer "which features matter")
rf_model = fitted_models["Random Forest"][0]
importances = pd.Series(rf_model.feature_importances_, index=X.columns).sort_values()
plt.figure(figsize=(8, 5))
importances.plot(kind="barh", color="#4C72B0")
plt.title("Feature Importance (Random Forest)")
plt.xlabel("Importance")
plt.tight_layout()
plt.savefig("feature_importance.png", dpi=150)
plt.close()

print("\nSaved: model_comparison_results.csv, results.txt, "
      "confusion_matrices.png, feature_importance.png")
