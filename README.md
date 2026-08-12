# Machine Learning Practice

## Overview

This repository is a personal machine learning learning portfolio and practice journal. It collects four notebooks where I worked through tabular preprocessing, model tuning, time series forecasting, classification ensembles, dimensionality reduction, clustering, regime analysis, and serious mortgage delinquency prediction.

This is not a production-grade machine learning system. The notebooks are meant to show what I practiced, what I tried, and what I observed while learning.

## Why I Built This

I built this project to keep my machine learning practice organized in one public place. The goal was to turn separate notebooks into a readable learning project with clear data paths, setup instructions, and lightweight validation scripts.

Practice goal:

- keep the original learning code mostly intact
- make the notebooks easier to read from a fresh clone
- document dataset requirements and runtime limitations
- remove course-specific or prompt-style framing
- make the project useful as a record of practice, not as a polished product claim

## What I Practiced

What I tried:

- building preprocessing pipelines for tabular data
- comparing linear models, decision trees, and random forests
- using cross-validation, grid search, and randomized search
- constructing lagged time series features
- testing random forest forecasting with time-aware splits
- using SVMs for image classification practice
- comparing hard voting, soft voting, and stacking ensembles
- applying PCA, t-SNE, LLE, and k-Means
- clustering macroeconomic regimes from inflation and unemployment data
- comparing classification models for imbalanced mortgage loan outcomes
- selecting classification thresholds with time-based validation data

Observation:

The notebooks mix code experiments, outputs, and short interpretation notes. Some sections are more about practicing the workflow than producing a final best model.

## Notebook Guide

| Notebook | Practice goal | What it includes |
| --- | --- | --- |
| `notebooks/01_tabular_housing_preprocessing_and_model_tuning.ipynb` | Practice tabular preprocessing and model tuning on housing data. | Missing-value imputation, categorical encoding, feature engineering, scaling, pipelines, linear regression, tree models, random forests, cross-validation, hyperparameter search, regularization, and learning curves. |
| `notebooks/02_time_series_forecasting_and_ensemble_classification.ipynb` | Practice time series forecasting and classification ensembles. | NYSE volume forecasting, lagged features, time-series splits, baseline comparison, feature importance, path signatures, MNIST SVM classification, voting ensembles, and stacking. |
| `notebooks/03_dimensionality_reduction_clustering_and_regimes.ipynb` | Practice dimensionality reduction, clustering, and regime analysis. | PCA with SVM and random forests, t-SNE, LLE, k-Means, silhouette analysis, clustering features for classification, and macroeconomic regime clustering. |
| `notebooks/04_predicting_serious_delinquency_in_us_mortgage_loans.ipynb` | Practice predicting serious mortgage delinquency with imbalanced, time-indexed loan data. | Freddie Mac loan-level preprocessing, time-based train/validation/test splits, logistic regression, random forest, linear SVM, MLP, XGBoost, threshold selection, and model comparison. |

## Datasets Used

Included data:

- `data/NYSE.csv` is included in the repository and used by the time series notebook through `../data/NYSE.csv`.

Downloaded public data:

- The housing notebook downloads the California housing dataset from the public Hands-On Machine Learning companion data repository when it is not already cached locally.
- The time series and ensemble notebook uses `sklearn.datasets.fetch_openml()` for MNIST.
- The dimensionality reduction and clustering notebook uses `sklearn.datasets.fetch_openml()` for MNIST, `sklearn.datasets.fetch_olivetti_faces()` for the Olivetti faces dataset, and public FRED CSV URLs for the regime section.

Data that must be obtained separately:

- The mortgage delinquency notebook uses the Freddie Mac Single-Family Loan-Level Dataset. The raw sample files are not included in this repository. Access is subject to Freddie Mac's current terms and may require registration.
- After obtaining the sample data, place the files under `data/freddie_mac/orig/` and `data/freddie_mac/svcg/`. The notebook expects `sample_orig_2018.txt` through `sample_orig_2022.txt` in `orig/`, and `sample_svcg_2018.txt` through `sample_svcg_2022.txt` in `svcg/`.

Limitation:

Some notebooks need internet access the first time they are run because datasets are fetched from public sources. The mortgage notebook cannot run from a fresh clone until the separately distributed Freddie Mac files are added in the directory layout above.

## Setup

Create and activate a virtual environment, then install dependencies.

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## How To Run

Start Jupyter from the repository root:

```bash
jupyter notebook
```

Then open notebooks from the `notebooks/` directory. Run them with `notebooks/` as the working directory so repository-relative paths such as `../data/NYSE.csv` and `../data/freddie_mac/` resolve as documented.

Result:

The NYSE notebook expects to run with paths relative to the notebook folder, so `../data/NYSE.csv` resolves correctly. If a Jupyter frontend starts the kernel from the repository root instead, open a terminal in `notebooks/` before launching Jupyter or adjust the working directory before running the time series notebook.

## Learning Notes / Limitations

Observation:

- The notebooks keep prior outputs to show the learning process.
- Results may vary slightly across library versions or hardware.
- Several sections can take a while to run, especially grid search, randomized search, t-SNE, LLE, learning curves, MLP training, voting ensembles, and stacking.
- The mortgage notebook includes five model families, resampling, hyperparameter tuning, and threshold evaluation. A complete run may be slow and memory intensive on a personal computer.
- Mortgage model results depend on the exact Freddie Mac sample release and library versions. Existing outputs are retained as learning records and are not a claim of current production performance.
- The notebooks are not packaged as reusable training pipelines or deployment code.

Limitation:

This project is best read as a learning journal. It does not include production monitoring, model serving, CI-backed notebook execution, or a formal experiment tracking system.

## Next Steps

Next step ideas:

- add short reflection summaries at the end of each notebook
- reduce duplicated modeling code where it helps readability
- add lightweight notebook smoke tests that avoid expensive model searches
- add environment notes for fully reproducible long-running runs
- revisit selected models with clearer train/validation/test reporting
- test cost-sensitive and calibrated mortgage risk models while keeping threshold selection separate from the test set

## Maintenance Scripts

The `scripts/` folder contains small utilities for keeping the repository clean.

Run the notebook cleanup script after adding or restoring source notebooks:

```bash
python scripts/sanitize_notebooks.py
```

Run the validation script before publishing changes:

```bash
python scripts/validate_repo.py
```

What the scripts check:

- expected files and folders exist
- notebook markdown avoids course-specific wording
- notebook metadata does not include local environment details
- `NYSE.csv` references use `../data/NYSE.csv`
- the mortgage notebook starts with the public project title, contains no group identity wording, and uses `../data/freddie_mac`
- raw source notebooks are not left in the repository root
