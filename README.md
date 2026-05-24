# Machine Learning Practice

A portfolio-style collection of personal machine learning practice notebooks. The notebooks explore data preprocessing, supervised learning, time series modeling, dimensionality reduction, clustering, and model evaluation.

## Repository Structure

```text
machine-learning-practice/
|-- README.md
|-- requirements.txt
|-- .gitignore
|-- data/
|   `-- NYSE.csv
|-- notebooks/
|   |-- 01_housing_preprocessing.ipynb
|   |-- 02_time_series_random_forest_svm.ipynb
|   `-- 03_pca_clustering.ipynb
`-- scripts/
    |-- sanitize_notebooks.py
    `-- validate_repo.py
```

## Contents

| Notebook | Focus | Concepts covered |
| --- | --- | --- |
| `notebooks/01_housing_preprocessing.ipynb` | Housing data preprocessing and model tuning | Missing-value imputation, categorical encoding, feature engineering, scaling, pipelines, linear regression, decision trees, random forests, cross-validation, grid search, randomized search, regularization, learning curves |
| `notebooks/02_time_series_random_forest_svm.ipynb` | Time series forecasting and classification practice | Lagged features, random forest forecasting, time-series cross-validation, baseline comparison, feature importance, path signatures, SVM classification, voting ensembles, stacking |
| `notebooks/03_pca_clustering.ipynb` | PCA, dimensionality reduction, clustering, and regimes | PCA with SVM and random forests, t-SNE, LLE, k-Means clustering, silhouette analysis, classification with cluster features, macroeconomic regime clustering |

## Data

`NYSE.csv` is included under `data/NYSE.csv`. The time series notebook loads it with the relative path `../data/NYSE.csv`.

The other notebooks use public datasets that are downloaded by the notebook code when they are not already cached:

- `01_housing_preprocessing.ipynb` downloads the California housing dataset from the companion Hands-On Machine Learning data repository and stores it under a local `datasets/` folder.
- `02_time_series_random_forest_svm.ipynb` uses `sklearn.datasets.fetch_openml()` for MNIST.
- `03_pca_clustering.ipynb` uses `sklearn.datasets.fetch_openml()` for MNIST, `sklearn.datasets.fetch_olivetti_faces()` for the Olivetti faces dataset, and public FRED CSV URLs for the macroeconomic regime section.

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

Open the notebooks in order from the `notebooks/` directory.

The notebook code assumes relative paths are resolved from inside the `notebooks/` directory. This is how many Jupyter frontends launch kernels when a notebook is opened from that folder. If a Jupyter environment starts kernels from the repository root instead, open a terminal in `notebooks/` before launching Jupyter or adjust the working directory before running the time series notebook.

## Limitations

Some notebooks may not fully execute from a fresh clone without internet access because several datasets are downloaded from public sources. Several cells can also take a while to run depending on hardware, especially cross-validation, grid search, randomized search, t-SNE, LLE, learning curves, MLP training, voting ensembles, and stacking.

## Maintenance Scripts

Run the cleanup script after adding or restoring original notebooks:

```bash
python scripts/sanitize_notebooks.py
```

Validate the repository structure and notebook cleanup rules:

```bash
python scripts/validate_repo.py
```
