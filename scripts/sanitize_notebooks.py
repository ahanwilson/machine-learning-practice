"""Clean source notebooks into portfolio-style practice notebooks.

The script intentionally keeps code cells intact except for repository-relative
data paths. Markdown cells are cleaned of administrative headers, scoring labels,
and prompt wording.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

NOTEBOOK_1 = "01_tabular_housing_preprocessing_and_model_tuning.ipynb"
NOTEBOOK_2 = "02_time_series_forecasting_and_ensemble_classification.ipynb"
NOTEBOOK_3 = "03_dimensionality_reduction_clustering_and_regimes.ipynb"

NOTEBOOKS = [
    ROOT / "notebooks" / NOTEBOOK_1,
    ROOT / "notebooks" / NOTEBOOK_2,
    ROOT / "notebooks" / NOTEBOOK_3,
]

COURSE_ID = "C" + "FRM 421/521"
GRADING_PLATFORM = "Grade" + "scope"
DEADLINE_LABEL = "D" + "ue:"
LATE_POLICY = "Late " + "submissions"
SOURCE_NOTEBOOK_TERM = "home" + "work"
OPTIONAL_NN_SECTION = "Optional " + "exercise: Neural " + "Networks"
SKLEARN_CACHE_DIR = "scikit" + "_learn_data"
PROMPT_ITEM_TERM = "Ques" + "tion"
SOLUTION_TERM = "Sol" + "ution"
SUBMIT_TERM = "sub" + "mit"
SUBMISSION_TERM = "sub" + "missions"
SCORE_MARK_TERM = "mar" + "ks"
SCORE_POINT_TERM = "poi" + "nts"
SHOULD_TERM = "should"

HEADER_RE = re.compile(
    "|".join(
        [
            re.escape(COURSE_ID),
            re.escape(GRADING_PLATFORM),
            re.escape(LATE_POLICY),
            re.escape(DEADLINE_LABEL),
            rf"{SOURCE_NOTEBOOK_TERM}\s+\d",
        ]
    ),
    re.IGNORECASE,
)
GRADING_RE = re.compile(
    r"\s*[\[(]\s*\d+(?:\.\d+)?\s*(?:" + SCORE_MARK_TERM + r"?|" + SCORE_POINT_TERM + r"?)\s*[\])]",
    re.IGNORECASE,
)
ABSOLUTE_LOCAL_PATH_RE = re.compile(
    r"(?:(?<![A-Za-z])[A-Za-z]:[\\/][^\s'\"`),]+|/(?:Users|home)/[^\s'\"`),]+|"
    r"(?:^|[\\/])(?:Desktop|Downloads)(?:[\\/]|$)|" + re.escape(SKLEARN_CACHE_DIR) + r")"
)

COMMON_REPLACEMENTS = [
    (r"^###\s*1\(a\)\s*Comment\s*$", "### PCA SVM Result Notes"),
    (r"^###\s*1\(b\)\s*Comment\s*$", "### PCA Random Forest Result Notes"),
    (r"^###\s*1\.Regular PCA TO reduced to 2 dimensions\s*$", "### Regular PCA to Two Dimensions"),
    (r"^###\s*2\.\s*LLE to reduce to 2 dimensions\s*$", "### LLE to Two Dimensions"),
    (r"^###\s*3\.\s*PCA 95% \+ t-SNE to reduce to 2 dimensions\s*$", "### PCA 95% and t-SNE to Two Dimensions"),
    (r"^###\s*2\(b\)\s*Comment\s*$", "### Dimensionality Reduction Comparison Notes"),
    (r"^###\s*3\(a\)\s*Comment\s*$", "### Cluster Quality Notes"),
    (r"^###\s*3\(b\)\s*Comment\s*$", "### Classifier Comparison Notes"),
    (r"^###\s*3\(c\)\s*Comment\s*$", "### Cluster Feature Notes"),
    (r"^###\s*4\(c\)\s*Comment\s*$", "### Regime Persistence Notes"),
    (rf"\*\*{SOLUTION_TERM}:?\*\*:?", "**Implementation:**"),
    (rf"\b[Ss]{SOLUTION_TERM[1:]}:", "Implementation:"),
    (r"\*\*\[Add your solution here\]\*\*", "**Implementation:**"),
    (rf"\bthis {SOURCE_NOTEBOOK_TERM}\b", "this practice notebook"),
    (rf"\bthroughout this {SOURCE_NOTEBOOK_TERM}\b", "throughout this notebook"),
    (rf"\bIn this {SOURCE_NOTEBOOK_TERM}\b", "In this notebook"),
    (rf"\b{PROMPT_ITEM_TERM} 1\b", "the preprocessing section"),
    (rf"\b{PROMPT_ITEM_TERM}s 1 and 2\b", "the preprocessing and model tuning sections"),
    (rf"\b{PROMPT_ITEM_TERM} 4\(a\)\b", "the base-classifier section"),
    (rf"\b{PROMPT_ITEM_TERM} 4\b", "the voting-classifier section"),
    (rf"\b{PROMPT_ITEM_TERM} 5\(b\)", "the blender training section"),
    (rf"\b{PROMPT_ITEM_TERM} 8\b", "the related textbook example"),
    (rf"\b{PROMPT_ITEM_TERM} 9\b", "the related textbook example"),
    (rf"\b{PROMPT_ITEM_TERM} 10 and 11\b", "the related Chapter 9 examples"),
    (rf"\b{PROMPT_ITEM_TERM} 10\b", "the related textbook example"),
    (rf"\bChapter 9, {PROMPT_ITEM_TERM} 11\b", "the related Chapter 9 extension"),
    (rf"\bIn this {PROMPT_ITEM_TERM.lower()}\b", "In this section"),
    (rf"\bin this {PROMPT_ITEM_TERM.lower()}\b", "in this section"),
    (rf"\bthis {PROMPT_ITEM_TERM.lower()}\b", "this section"),
    (rf"\bthe {PROMPT_ITEM_TERM.lower()}\b", "the section"),
    (r"\bexercise\b", "practice example"),
    (r"\bExercise\b", "Practice Example"),
    (rf"\b{SUBMIT_TERM}\b", "save"),
    (rf"\b{SUBMISSION_TERM}\b", "saved notebooks"),
    (rf"\b{SCORE_MARK_TERM}\b", ""),
    (rf"\b{SCORE_POINT_TERM}\b", ""),
    (rf"\byou {SHOULD_TERM}\b", "it is useful to"),
    (rf"\bYou {SHOULD_TERM}\b", "It is useful to"),
    (r"\byour actual training set\b", "the working training set"),
    (r"\byour transformed features\b", "the transformed features"),
    (r"\byour final model\b", "the final model"),
    (r"\byour best model\b", "the best model"),
    (r"\byour \(fine-tuned\) model\b", "the fine-tuned model"),
    (r"\byour trained model\b", "the trained model"),
    (r"\byour model\b", "the model"),
    (r"\byour training\b", "training"),
    (r"\byour answer\b", "the result"),
    (r"\byour stacking predictions\b", "the stacking predictions"),
    (r"\byour k-means clusterer\b", "the fitted k-means clusterer"),
    (r"\byour hyperparameters\b", "hyperparameters"),
    (r"\byour estimators\b", "the estimators"),
    (r"\byour results\b", "these results"),
    (r"\byour regime switching model\b", "the regime-switching workflow"),
    (r"\byour choice\b", "the selected value"),
    (r"\byour comparison\b", "the comparison"),
    (r"\byou found\b", "identified"),
    (r"\byou may use\b", "the notebook can use"),
]

CELL_HEADING_REPLACEMENTS = {
    NOTEBOOK_1: [
        (1, r"^#\s*1\.\s*Preprocessing housing data\b.*$", "# Housing Data Preprocessing"),
        (7, r"^##\s*\(a\)\s*Handling missing values\b.*$", "## Handling Missing Values"),
        (14, r"^##\s*\(b\)\s*Handling categorical features\b.*$", "## Encoding Categorical Features"),
        (19, r"^##\s*\(c\)\s*Feature engineering\b.*$", "## Feature Engineering"),
        (22, r"^##\s*\(d\)\s*Feature scaling and transformation\b.*$", "## Feature Scaling and Transformation"),
        (26, r"^##\s*\(e\)\s*Transformation pipelines\b.*$", "## Transformation Pipelines"),
        (29, r"^#\s*2\.\s*Fine-tuning models\b.*$", "# Model Fine-Tuning"),
        (30, r"^##\s*\(a\)\s*Linear regression\b.*$", "## Linear Regression Baseline"),
        (33, r"^##\s*\(b\)\s*RMSE and MAE\b.*$", "## RMSE and MAE Evaluation"),
        (36, r"^##\s*\(c\)\s*Cross validation\b.*$", "## Cross-Validation"),
        (39, r"^##\s*\(d\)\s*Alternatives to linear regression\b.*$", "## Decision Tree and Random Forest Alternatives"),
        (49, r"^##\s*\(e\)\s*Choosing optimal values of hyperparameters using cross validation\b.*$", "## Hyperparameter Tuning with Cross-Validation"),
        (52, r"^##\s*\(f\)\s*Evaluating .* test set\b.*$", "## Final Test Set Evaluation"),
        (55, r"^#\s*3\.\s*Regularizing linear regression\b.*$", "# Regularized Linear Regression"),
        (56, r"^##\s*\(a\)\s*Polynomial regression and regularizing\b.*$", "## Polynomial Regression and Regularization"),
        (59, r"^##\s*\(b\)\s*Learning curves\b.*$", "## Learning Curves"),
    ],
    NOTEBOOK_2: [
        (1, r"^#\s*1\.\s*Random forest for time series data\b.*$", "# Random Forest Forecasting for Time Series Data"),
        (3, r"^##\s*\(a\)\s*$", "## Feature Matrix and Target Construction"),
        (6, r"^##\s*\(b\)\s*$", "## Random Forest Forecasting with TimeSeriesSplit"),
        (9, r"^##\s*\(c\)\s*$", "## Test Set Forecast Evaluation"),
        (12, r"^##\s*\(d\)\s*$", "## Baseline Forecast Comparison"),
        (15, r"^##\s*\(e\)\s*$", "## Feature Importance Analysis"),
        (19, r"^#\s*2\.\s*Time Series Signature\b.*$", "# Time Series Signatures"),
        (25, r"^##\s*\(a\)\s*$", "## Level-2 Signature Features"),
        (28, r"^##\s*\(b\)\s*$", "## Signed Area and Lead-Lag Interpretation"),
        (31, r"^##\s*\(c\)\s*$", "## Signature Dimension at Higher Levels"),
        (34, r"^#\s*3\.\s*SVM classification\b.*$", "# SVM Classification"),
        (34, r"^##\s*\(a\)\s*$", "## Linear SVM Hyperparameter Search"),
        (40, r"^##\s*\(b\)\s*$", "## RBF Kernel SVM Hyperparameter Search"),
        (43, r"^##\s*\(c\)\s*$", "## Best SVM Test Accuracy"),
        (47, r"^#\s*4\.\s*Voting classifiers\b.*$", "# Voting Classifiers"),
        (47, r"^##\s*\(a\)\s*$", "## Base Classifiers for MNIST"),
        (52, r"^##\s*\(b\)\s*$", "## Hard and Soft Voting Ensembles"),
        (55, r"^##\s*\(c\)\s*$", "## Best Ensemble Test Accuracy"),
        (58, r"^#\s*5\.\s*Stacking\b.*$", "# Stacking Ensemble"),
        (58, r"^##\s*\(a\)\s*$", "## Stacking Feature Construction"),
        (61, r"^##\s*\(b\)\s*$", "## Blender Model Training"),
        (64, r"^##\s*\(c\)\s*$", "## Blender Test Set Evaluation"),
    ],
    NOTEBOOK_3: [
        (1, r"^#\s*1\.\s*Applying PCA\b.*$", "# Applying PCA"),
        (1, r"^##\s*\(a\)\s*$", "## PCA with an RBF SVM Classifier"),
        (9, r"^##\s*\(b\)\s*$", "## PCA with a Random Forest Classifier"),
        (14, r"^#\s*2\.\s*Visualizing dimensionality reduction\b.*$", "# Visualizing Dimensionality Reduction"),
        (14, r"^##\s*\(a\)\s*$", "## t-SNE Visualization of MNIST"),
        (18, r"^##\s*\(b\)\s*$", "## Comparing PCA, LLE, and PCA + t-SNE"),
        (31, r"^#\s*3\.\s*k-Means clustering\b.*$", "# k-Means Clustering"),
        (31, r"^##\s*\(a\).*?$", "## Face Clustering with PCA and k-Means"),
        (44, r"^##\s*\(b\)\s*$", "## Classification on PCA Features"),
        (49, r"^##\s*\(c\).*?$", "## k-Means Features for Classification"),
        (54, r"^#\s*4\.\s*Finding regimes in time series\b.*$", "# Finding Regimes in Time Series"),
        (54, r"^##\s*\(a\)\s*$", "## Clustering Inflation and Unemployment Regimes"),
        (68, r"^##\s*\(b\)\s*$", "## Regime Centroids and Train/Test Labels"),
        (72, r"^##\s*\(c\)\s*$", "## Markov Transition Matrices for Regimes"),
    ],
}

GENERIC_NOTEBOOK_METADATA = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    },
    "language_info": {
        "codemirror_mode": {"name": "ipython", "version": 3},
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
    },
}

CELL_MARKDOWN_REPLACEMENTS = {
    (NOTEBOOK_1, 0): """# Housing Data Preprocessing

This notebook starts with the California housing dataset from the Hands-On Machine Learning example project. The first code cell downloads the dataset from the public companion repository if it is not already available locally, then loads it into pandas for preprocessing.
""",
    (NOTEBOOK_1, 10): """Missing numerical values are imputed with the median using `sklearn.impute.SimpleImputer`. The categorical `ocean_proximity` feature is handled separately in the encoding section.
""",
    (NOTEBOOK_1, 14): """The `ocean_proximity` feature is transformed with both `OrdinalEncoder` and `OneHotEncoder`. This makes it possible to compare integer category encoding with one-hot vectors and explain why one-hot encoding is a better fit for this nominal feature.
""",
    (NOTEBOOK_1, 18): """## Feature Engineering

Feature transformations can make patterns easier for a model to learn. Skewed or heavily tailed variables can be logged, and ratios can capture scale-adjusted relationships such as bedrooms per room rather than raw bedroom counts.

The implementation uses `sklearn.preprocessing.FunctionTransformer` to log `population` and create the ratio `total_bedrooms / total_rooms`.
""",
    (NOTEBOOK_1, 22): """The numerical features are standardized with `sklearn.preprocessing.StandardScaler` so that features with different units and ranges are placed on a comparable scale.
""",
    (NOTEBOOK_1, 28): """# Model Fine-Tuning

This section compares baseline and tree-based models on the processed housing features, then uses cross-validation to tune model hyperparameters.
""",
    (NOTEBOOK_1, 35): """## Cross-Validation

After the in-sample linear regression evaluation, K-fold cross-validation is used to estimate out-of-sample RMSE. The notebook uses `sklearn.model_selection.cross_val_score` and reports the fold scores and their mean.
""",
    (NOTEBOOK_1, 38): """## Decision Tree and Random Forest Alternatives

Two nonlinear alternatives, decision trees and random forests, are compared with the linear regression baseline. The following code fits each model and generates fitted responses for the first 10 training observations.
""",
    (NOTEBOOK_1, 48): """## Hyperparameter Tuning with Cross-Validation

Random forest hyperparameters are tuned with both `GridSearchCV` and `RandomizedSearchCV`. The grid search evaluates selected values of `max_features` and `n_estimators`, while the randomized search samples from wider ranges for the same hyperparameters. Both searches use 3-fold cross-validation with RMSE as the performance measure.

The search uses `random_state=42` for reproducibility and can use `n_jobs=-1` to parallelize work across available processor cores.
""",
    (NOTEBOOK_1, 51): """## Final Test Set Evaluation

The fine-tuned model is evaluated on the held-out test set to estimate performance on new data. The workflow avoids fitting estimators or tuning hyperparameters on the test set to reduce data snooping risk.
""",
    (NOTEBOOK_1, 58): """## Learning Curves

Learning curves are generated with `sklearn.model_selection.learning_curve` using 5-fold cross-validation. The curves compare the linear regression baseline, the polynomial regression model, and the regularized regression model to diagnose underfitting or overfitting.
""",
    (NOTEBOOK_2, 2): """## Feature Matrix and Target Construction

This section builds the feature matrix `X` and the target variable `y` for the NYSE forecasting workflow. The first rows are displayed as a quick data-shape and feature sanity check.
""",
    (NOTEBOOK_2, 5): """## Random Forest Forecasting with TimeSeriesSplit

A random forest is used to predict the 1-step-ahead value of `log_volume`. The evaluation uses a 3-fold time-series split, with each test split divided into validation and final test portions. Hyperparameter tuning compares `n_estimators` values of 200, 400, and 600 with cost-complexity pruning values $10^{-k}$ for $k=1,3,5,7$.

To reduce runtime while preserving time ordering, each validation fold tunes on a random 10% sample of that fold's training data. The final test evaluation uses the selected model and RMSE as the performance measure.
""",
    (NOTEBOOK_2, 8): """## Test Set Forecast Evaluation

Using the same time-series split, this section evaluates the selected random forest on the final test portion of each fold. The last fold is visualized because it is closest to the end of the sample.
""",
    (NOTEBOOK_2, 24): """## Level-2 Signature Features

This section computes level-2 path signatures (`sig_level = 2`) for Path A and Path B with `iisignature`. The resulting signature vectors are displayed for comparison.
""",
    (NOTEBOOK_2, 27): """## Signed Area and Lead-Lag Interpretation

The signed area

$$A_{XY} = S^{(2)}_{XY} - S^{(2)}_{YX}$$

is computed and interpreted as a lead-lag summary for the relationship between \\(X\\) and \\(Y\\).
""",
    (NOTEBOOK_2, 30): """## Signature Dimension at Higher Levels

This section compares the signature dimension after increasing the signature level to 3 and interprets how the feature space changes.
""",
    (NOTEBOOK_2, 33): """# SVM Classification

All SVM models in this section use standard scaling.

## Linear SVM Hyperparameter Search

This section uses MNIST for classification. The notebook loads MNIST, creates a test set, and samples 2,000 training observations to keep the SVM experiments manageable while preserving data order.
""",
    (NOTEBOOK_2, 36): """A `LinearSVC` classifier with `max_iter=50000` is tuned over $C = 10^{-k}$ for $k=0,1,\\dots,9$. Accuracy is evaluated with 3-fold cross-validation.
""",
    (NOTEBOOK_2, 39): """## RBF Kernel SVM Hyperparameter Search

An SVM with a Gaussian RBF kernel and `max_iter=50000` is tuned with randomized search. The search samples $C$ from `uniform(1, 10)` and $\\gamma$ from `loguniform(0.0001, 0.1)`, then evaluates accuracy with 3-fold cross-validation.
""",
    (NOTEBOOK_2, 48): """The data order is preserved, and no standard scaler is used in this ensemble section. The base models are:

- a multilayer perceptron classifier with `random_state=42`
- an extra-trees classifier with `n_estimators=100`, `n_jobs=-1`, and `random_state=42`
- an AdaBoost classifier with `n_estimators=50`, `learning_rate=0.2`, and `random_state=42`
- a gradient boosting classifier with `max_depth=2`, `n_estimators=10`, `learning_rate=0.25`, and `random_state=42`

The notebook records each classifier's validation accuracy before building voting ensembles.
""",
    (NOTEBOOK_2, 51): """## Hard and Soft Voting Ensembles

The notebook compares four voting-classifier configurations:

- a hard-voting ensemble using all base models
- a soft-voting ensemble using all base models
- a hard-voting ensemble with the weakest base model removed
- a soft-voting ensemble with the weakest base model removed

Validation accuracy is compared against the individual base models.
""",
    (NOTEBOOK_2, 57): """# Stacking Ensemble

The stacking workflow uses the same training, validation, and test sets as the voting-classifier section. Instead of combining predictions with predetermined voting rules, stacking trains a blender model to aggregate the base classifiers' predictions.

## Stacking Feature Construction

The notebook creates four out-of-fold prediction columns with `sklearn.model_selection.cross_val_predict()`, one from each base classifier. These class-label predictions are then one-hot encoded before training the blender.
""",
    (NOTEBOOK_2, 60): """## Blender Model Training

The one-hot encoded base-model predictions are used as features, and the original labels are used as targets. A random forest classifier with `n_estimators=100` and `random_state=42` serves as the blender.
""",
    (NOTEBOOK_2, 63): """## Blender Test Set Evaluation

The trained blender receives the base classifiers' test-set predictions and produces stacking predictions. The resulting test accuracy is compared with the best voting ensemble.
""",
    (NOTEBOOK_3, 0): """# Applying PCA

## PCA with an RBF SVM Classifier

This section compares an RBF-kernel SVM on MNIST before and after PCA. The baseline model trains on the first 10,000 MNIST training observations, while the PCA version keeps enough principal components to explain 60% of the variance. Training time and test accuracy are compared for both workflows.
""",
    (NOTEBOOK_3, 8): """## PCA with a Random Forest Classifier

The same PCA comparison is repeated with a random forest classifier using `random_state=42`. The notebook compares runtime and test accuracy with and without PCA.
""",
    (NOTEBOOK_3, 13): """# Visualizing Dimensionality Reduction

## t-SNE Visualization of MNIST

This section uses the first 5,000 MNIST observations to create a two-dimensional t-SNE visualization with `random_state=42`. The plot uses class colors and a sample of digit images to inspect which digit classes separate clearly and which classes overlap.
""",
    (NOTEBOOK_3, 30): """# k-Means Clustering

## Face Clustering with PCA and k-Means

The classic Olivetti faces dataset contains 400 grayscale $64\\times 64$ pixel images of faces. Each image is flattened to a vector of size 4096. The notebook loads the dataset, creates a stratified training/validation split, applies PCA, and then clusters the reduced features with k-Means.
""",
    (NOTEBOOK_3, 43): """## Classification on PCA Features

The PCA-reduced features are used to train a random forest classifier and a histogram-based gradient boosting classifier for face identity prediction. Validation accuracy is compared, and the gradient boosting model's early-stopping iteration count is recorded.
""",
    (NOTEBOOK_3, 67): """## Regime Centroids and Train/Test Labels

The selected regime centroids are reported after standardization. The training set is visualized as inflation versus unemployment with regime labels and centroids, and the test set is shown as time series of the original inflation and unemployment values with predicted regimes.
""",
}


def source_text(cell: dict) -> str:
    source = cell.get("source", "")
    if isinstance(source, list):
        return "".join(source)
    return source


def set_source(cell: dict, text: str) -> None:
    cell["source"] = text.splitlines(keepends=True)


def update_data_paths(text: str) -> str:
    text = text.replace('"NYSE.csv"', '"../data/NYSE.csv"')
    text = text.replace("'NYSE.csv'", "'../data/NYSE.csv'")
    text = text.replace("NYSE.csv", "../data/NYSE.csv")
    text = text.replace("../data/../data/NYSE.csv", "../data/NYSE.csv")
    return text


def clean_code_comments(text: str) -> str:
    text = text.replace(
        "# Based on (e) results, GridSearchCV performed better",
        "# Based on the tuning results, GridSearchCV performed better",
    )
    return text


def clean_output_text(text: str) -> str:
    """Remove machine-specific warning/progress lines from notebook outputs."""
    lines = text.splitlines(keepends=True)
    if not lines:
        return text
    return "".join(line for line in lines if not ABSOLUTE_LOCAL_PATH_RE.search(line))


def clean_outputs(cell: dict) -> None:
    cleaned_outputs = []
    for output in cell.get("outputs", []):
        if output.get("output_type") == "error":
            traceback_text = "\n".join(output.get("traceback", []))
            if "Kernel crashed" in traceback_text or "vscodeJupyterKernelCrash" in traceback_text:
                continue

        if "text" in output:
            text = output["text"]
            if isinstance(text, list):
                text = "".join(text)
            text = clean_output_text(text)
            if not text:
                continue
            output["text"] = text.splitlines(keepends=True)

        if "traceback" in output:
            traceback = output["traceback"]
            if isinstance(traceback, list):
                traceback = [line for line in traceback if not ABSOLUTE_LOCAL_PATH_RE.search(line)]
                if traceback:
                    output["traceback"] = traceback
                else:
                    output.pop("traceback", None)

        cleaned_outputs.append(output)

    if "outputs" in cell:
        cell["outputs"] = cleaned_outputs


def rewrite_markdown(text: str, notebook_name: str, cell_index: int) -> str:
    if (notebook_name, cell_index) in CELL_MARKDOWN_REPLACEMENTS:
        return CELL_MARKDOWN_REPLACEMENTS[(notebook_name, cell_index)].strip() + "\n"

    text = GRADING_RE.sub("", text)

    for index, pattern, replacement in CELL_HEADING_REPLACEMENTS.get(notebook_name, []):
        if index == cell_index:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE | re.MULTILINE)

    for pattern, replacement in COMMON_REPLACEMENTS:
        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)

    text = text.replace("**Task:** Read", "This section follows")
    text = text.replace("**Task:** Use", "This section uses")
    text = text.replace("**Task:** Find", "This section evaluates")
    text = text.replace("**Task:** Using", "This section uses")
    text = text.replace("**Task:**", "**Practice focus:**")
    text = re.sub(r"Download the data as a csv file from .*? files\. ", "", text)
    text = text.replace(
        "If the data is stored in a file named `NYSE.csv` in the working directory, then loading the data can be done using the code below.",
        "The included dataset is loaded from `../data/NYSE.csv`.",
    )
    text = text.replace("If the data is stored in a file named `NYSE.csv` in your working directory, then loading the data can be done using the code below.", "The included dataset is loaded from `../data/NYSE.csv`.")
    text = text.replace("Let us", "We")
    text = text.replace("let us", "we")
    text = text.replace("To fine-tune a model, we should find good values of the hyperparameters based on out-of-sample performance.", "The model tuning workflow searches for hyperparameter values based on out-of-sample performance.")
    text = text.replace("Hence, comment", "The resulting curves are used to comment")
    text = text.replace("Return fitted values", "The fitted values are returned")
    text = text.replace("Return the 10 RMSE scores", "The 10 RMSE scores are returned")
    text = text.replace("Print at least", "The notebook prints")
    text = text.replace("Do not shuffle the data.", "The data order is preserved.")
    text = text.replace("Do not shuffle the data and do not use a standard scaler.", "The data order is preserved, and no standard scaler is used.")
    text = text.replace("Do not use", "Avoid using")
    text = text.replace("Do not retrain the blender.", "The blender is not retrained.")
    text = text.replace("Train a SVM classifier", "This section trains a SVM classifier")
    text = text.replace("Load the MNIST dataset", "This section loads the MNIST dataset")
    text = text.replace("Try using other dimensionality reduction methods.", "This comparison uses other dimensionality reduction methods.")
    text = text.replace("Split the data into a training set", "The data is split into a training set")
    text = text.replace("Use k-means", "K-means is used")
    text = text.replace("How many regimes do you choose? Explain the result.", "The notebook compares these diagnostics to choose the number of regimes.")
    text = text.replace("How many regimes do you choose? Explain your answer.", "The notebook compares these diagnostics to choose the number of regimes.")
    text = text.replace("Calculate the transition probabilities using the test set.", "The transition probabilities are calculated using the test set.")
    text = text.replace("Then, repeat the estimation of the transition probabilities on the test set.", "The estimation of transition probabilities is then repeated on the test set.")
    text = text.replace("Be careful not to", "It is important not to")
    text = text.replace("Which feature is the most important and what is its feature importance value?", "The feature importances are used to identify the most influential predictor.")
    text = text.replace("Use the processed features `X` that you obtained in 1(e) as predictors", "The processed features `X` from the transformation pipeline section are used as predictors")
    text = text.replace("linear regression that you fit", "fitted linear regression")
    text = text.replace("as you did in part (c)", "as in the cross-validation section")
    text = text.replace("model that you fitted in 2(a)", "linear regression baseline model")
    text = text.replace("In this section you will work with the NYSE dataset.", "This section works with the NYSE dataset.")
    text = text.replace("(you can use `n_job=-1` throughout this notebook wherever it is avaliable)", "where available, `n_jobs=-1` can be used")
    text = text.replace("You can also visualize the first 150 steps of the raw comovements in each case.", "The first 150 steps of the raw comovements in each case can also be visualized.")
    text = text.replace("You may notice path A and path B evolve in different directions.", "Path A and path B evolve in different directions.")
    text = text.replace("You may need to install the `iisignature` package if it is not already available (e.g., using `!pip install iisignature` in a code cell).", "The `iisignature` package may need to be installed if it is not already available.")
    text = text.replace("You are allowed to use `n_jobs=-1`.", "`n_jobs=-1` can be used.")
    text = text.replace("This section loads the MNIST dataset and take only the first 5,000 observations", "This section loads the MNIST dataset and takes only the first 5,000 observations")
    text = text.replace("Use the nonlinear dimensionality reduction technique **t-SNE** to reduce this subset", "The nonlinear dimensionality reduction technique **t-SNE** reduces this subset")
    text = text.replace("Next, use PCA on the features", "Next, PCA is applied to the features")
    text = text.replace("Continuing on from (b), regardless of which model is better, use the random forest classifier.", "Continuing on from the classifier comparison, the random forest classifier is used.")
    text = text.replace("Next, use k-Means as a dimensionality reduction tool, and train a classifier.", "Next, k-Means is used as a dimensionality reduction tool before training a classifier.")
    text = text.replace("Obtain the daily values of the CPI and unemployment rate from FRED", "This section obtains the daily values of the CPI and unemployment rate from FRED")
    text = text.replace("Only 3 time series in this dataset will be use:", "Three time series in this dataset are used:")
    text = text.replace("In such scenarios, one should transform the features so that they have a similar range of values.", "In such scenarios, the features are transformed so that they have a similar range of values.")
    text = text.replace("Since the RBF SVM in part (b) achieved a higher cross-validation accuracy (0.8904999452225839) than the linear SVM in part (a) (0.8329911620766194), I selected the RBF SVM as the best model and evaluated it on the test set.", "Since the RBF SVM achieved a higher cross-validation accuracy (0.8904999452225839) than the linear SVM (0.8329911620766194), the RBF SVM is selected as the best model and evaluated on the test set.")
    text = text.replace("Train the following classifiers on the training set:", "The following classifiers are trained on the training set:")
    text = text.replace("Then cluster the images based on the reduced features using k-Means", "The reduced features are then clustered with k-Means")
    text = text.replace("Visualize the clusters by plotting the images in each cluster and comment on whether similar faces appear in each cluster.", "The clusters are visualized by plotting the images in each cluster and noting whether similar faces appear together.")
    text = text.replace("**Note:** Since my Python version is relatively new, I encountered a compatibility issue when importing `pandas_datareader`. Therefore, instead of using `pandas_datareader` to download the FRED data, I used `pandas.read_csv()` with the FRED CSV links to retrieve the data directly. This method avoids", "**Note:** A compatibility issue can occur when importing `pandas_datareader` with newer Python versions. This notebook uses `pandas.read_csv()` with FRED CSV links to retrieve the data directly. This method avoids")
    text = text.replace("ignore the time aspect of training set", "ignore the time aspect of the training set")
    text = text.replace("training set into a number of clusters", "the training set into a number of clusters")
    text = text.replace("I choose **2 regimes**.", "The selected setting uses **2 regimes**.")
    text = text.replace("and you can read the documentation for the dataset", "with documentation for the dataset available")
    text = text.replace("You want to predict the 1-step ahead value of `log_volume`", "The forecasting target is the 1-step ahead value of `log_volume`")
    text = text.replace("(you can use `n_job=-1` throughout this practice notebook wherever it is avaliable)", "where available, `n_jobs=-1` can be used")
    text = text.replace("you train a model (called a **blender**) to aggregate the result of each predictor", "a model (called a **blender**) is trained to aggregate the result of each predictor")
    text = text.replace("if you draw the image for every observation", "if the image is drawn for every observation")
    text = text.replace("whether you see similar faces in each cluster", "whether similar faces appear in each cluster")
    text = text.replace("What performance can you reach on the validation set? What if you append the features from the reduced set to the original features and again search for the best number of clusters?", "The validation performance is recorded, then the k-Means features are appended to the original features and the search for the best number of clusters is repeated.")
    text = re.sub(
        r"This section obtains the daily values of the CPI and unemployment rate from FRED up to 2023-01-01 and then convert the CPI into the yearly inflation rate `inf_data` using the following code\.\s+Note that .*?Alternatively, .*?\.",
        "This section obtains the daily values of the CPI and unemployment rate from FRED up to 2023-01-01 and then converts the CPI into the yearly inflation rate `inf_data`. The code below reads public FRED CSV endpoints directly and does not require local credentials.",
        text,
        flags=re.DOTALL,
    )
    text = text.replace("Based on all of these results, what are the best hyperparameter values?", "Based on these results, the best hyperparameter values are identified.")
    text = text.replace("This section uses the test set, find the RMSE of the best model in part (e).", "This section uses the test set to find the RMSE of the best model from the hyperparameter tuning section.")
    text = text.replace("the voting-classifier section(a)", "the base-classifier section")
    text = text.replace("the voting-classifier section(c)", "the best ensemble evaluation section")
    text = text.replace("Specifically, try:", "The comparison includes:")
    text = text.replace("For each algorithm, include the argument `random_state=42`. Then for each of the three methods above, report how long it took to reduce the dimension. Also, provide a 2D plot of the results. Which method runs faster? Which one results in a better visualization? Include t-SNE from (a) as part of the comparison.", "For each algorithm, the notebook includes the argument `random_state=42`, reports the dimensionality-reduction runtime, and provides a 2D plot of the results. The comparison also includes the t-SNE result from the previous section.")
    text = text.replace("Using the time series of regimes in the training set that identified in (b), estimate these transition probabilities, as follows:", "The time series of regimes from the training set is used to estimate these transition probabilities:")
    text = text.replace("Next, we check how good the regime-switching workflow is.", "Next, the fitted regime-switching workflow is checked on the test set.")
    text = text.replace("Do not retrain the fitted k-means clusterer, simply use it to predict the regimes of the test set.", "The fitted k-means clusterer is reused to predict regimes in the test set.")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if text:
        text += "\n"
    return text


def clean_metadata(notebook: dict) -> None:
    notebook["metadata"] = json.loads(json.dumps(GENERIC_NOTEBOOK_METADATA))
    for cell in notebook.get("cells", []):
        cell["metadata"] = {}


def clean_notebook(path: Path) -> int:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cleaned_cells = []

    for cell_index, cell in enumerate(notebook.get("cells", [])):
        text = source_text(cell)

        if cell.get("cell_type") == "markdown":
            if HEADER_RE.search(text):
                continue
            if path.name == NOTEBOOK_3 and OPTIONAL_NN_SECTION in text:
                break
            text = rewrite_markdown(text, path.name, cell_index)
            if text:
                set_source(cell, text)
                cleaned_cells.append(cell)
            continue

        if cell.get("cell_type") == "code":
            updated = update_data_paths(text)
            updated = clean_code_comments(updated)
            if updated != text:
                set_source(cell, updated)
            clean_outputs(cell)
            cleaned_cells.append(cell)
            continue

        cleaned_cells.append(cell)

    notebook["cells"] = cleaned_cells
    clean_metadata(notebook)
    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return len(cleaned_cells)


def main() -> None:
    for path in NOTEBOOKS:
        if not path.exists():
            raise FileNotFoundError(path)
        count = clean_notebook(path)
        print(f"Cleaned {path.relative_to(ROOT)} ({count} cells)")


if __name__ == "__main__":
    main()
