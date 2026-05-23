# Machine Learning Practice

A portfolio-style collection of personal machine learning practice notebooks. The notebooks explore data preprocessing, supervised learning, time series modeling, dimensionality reduction, clustering, and model evaluation.

## Repository Structure

```text
machine-learning-practice/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── NYSE.csv
├── notebooks/
│   ├── 01_housing_preprocessing.ipynb
│   ├── 02_time_series_random_forest_svm.ipynb
│   └── 03_pca_clustering.ipynb
└── scripts/
    ├── sanitize_notebooks.py
    └── validate_repo.py
```

## Contents

| Notebook | Focus | Concepts covered |
| --- | --- | --- |
| `notebooks/01_housing_preprocessing.ipynb` | Housing data preprocessing and model tuning | Missing-value imputation, categorical encoding, feature engineering, scaling, pipelines, linear regression, decision trees, random forests, cross-validation, grid search, randomized search, regularization, learning curves |
| `notebooks/02_time_series_random_forest_svm.ipynb` | Time series forecasting and classification practice | Lagged features, random forest forecasting, time-series cross-validation, baseline comparison, feature importance, path signatures, SVM classification, voting ensembles, stacking |
| `notebooks/03_pca_clustering.ipynb` | PCA, dimensionality reduction, clustering, and regimes | PCA with SVM and random forests, t-SNE, LLE, k-Means clustering, silhouette analysis, classification with cluster features, macroeconomic regime clustering |

## Data

`NYSE.csv` is included under `data/NYSE.csv`. The time series notebook loads it with the relative path `../data/NYSE.csv`.

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Running the Notebooks

Start Jupyter from the repository root:

```bash
jupyter notebook
```

Open the notebooks in order from the `notebooks/` directory. Running from the repository root keeps relative data paths consistent.

## Limitations

Some notebooks may not fully execute from a fresh clone without internet access. The housing notebook downloads the California housing dataset, and the PCA/clustering notebook reads public FRED CSV endpoints for the macroeconomic regime section. Several model search and dimensionality-reduction cells can also take a while to run depending on hardware.

## Maintenance Scripts

Run the cleanup script after adding or restoring original notebooks:

```bash
python scripts/sanitize_notebooks.py
```

Validate the repository structure and notebook cleanup rules:

```bash
python scripts/validate_repo.py
```
