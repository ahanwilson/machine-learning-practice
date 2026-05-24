"""Validate the portfolio notebook repository structure and cleanup rules."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

NOTEBOOK_1 = "01_tabular_housing_preprocessing_and_model_tuning.ipynb"
NOTEBOOK_2 = "02_time_series_forecasting_and_ensemble_classification.ipynb"
NOTEBOOK_3 = "03_dimensionality_reduction_clustering_and_regimes.ipynb"

OLD_NOTEBOOK_NAMES = [
    "01_housing" + "_preprocessing.ipynb",
    "02_time_series" + "_random_forest_svm.ipynb",
    "03_pca" + "_clustering.ipynb",
]

REQUIRED_PATHS = [
    ROOT / "README.md",
    ROOT / "requirements.txt",
    ROOT / ".gitignore",
    ROOT / "notebooks" / NOTEBOOK_1,
    ROOT / "notebooks" / NOTEBOOK_2,
    ROOT / "notebooks" / NOTEBOOK_3,
    ROOT / "data" / "NYSE.csv",
    ROOT / "scripts" / "sanitize_notebooks.py",
    ROOT / "scripts" / "validate_repo.py",
]

COURSE_ID = "C" + "FRM 421/521"
GRADING_PLATFORM = "Grade" + "scope"
DEADLINE_LABEL = "D" + "ue:"
LATE_POLICY = "Late " + "submissions"
SOURCE_NOTEBOOK_TITLE = "Home" + "work"
OPTIONAL_NN_SECTION = "Optional " + "exercise: Neural " + "Networks"
SKLEARN_CACHE_DIR = "scikit" + "_learn_data"
SOLUTION_TERM = "Sol" + "ution"
PROMPT_ITEM_TERM = "Ques" + "tion"
SCORE_MARK_TERM = "mar" + "ks"
SCORE_POINT_TERM = "poi" + "nts"
SHOULD_PHRASE = "you " + "should"
ACCEPTABLE_PHRASE = "it is " + "acceptable"
CREATE_FEATURE_PHRASE = "Create the " + "feature matrix"
SAME_SPLIT_PHRASE = "Using the same " + "split as in"

RAW_SOURCE_NOTEBOOKS = [
    ROOT / f"{SOURCE_NOTEBOOK_TITLE}{index}.ipynb" for index in (1, 2, 3)
]

FORBIDDEN_MARKDOWN = [
    COURSE_ID,
    GRADING_PLATFORM,
    DEADLINE_LABEL,
    LATE_POLICY,
    SOURCE_NOTEBOOK_TITLE,
    SOLUTION_TERM,
    PROMPT_ITEM_TERM,
    ACCEPTABLE_PHRASE,
    SHOULD_PHRASE,
    CREATE_FEATURE_PHRASE,
    SAME_SPLIT_PHRASE,
    *OLD_NOTEBOOK_NAMES,
]

GRADING_RE = re.compile(
    r"[\[(]\s*\d+(?:\.\d+)?\s*(?:" + SCORE_MARK_TERM + r"?|" + SCORE_POINT_TERM + r"?)\s*[\])]",
    re.IGNORECASE,
)
ABSOLUTE_LOCAL_PATH_RE = re.compile(
    r"(?:(?<![A-Za-z])[A-Za-z]:[\\/][^\s'\"`),]+|/(?:Users|home)/[^\s'\"`),]+|"
    r"(?:^|[\\/])(?:Desktop|Downloads)(?:[\\/]|$)|" + re.escape(SKLEARN_CACHE_DIR) + r")"
)
BAD_NYSE_RE = re.compile(r"(?<!\.\./data/)NYSE\.csv")
EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)
SECRET_RE = re.compile(
    r"(?:api[_-]?key|password|secret|token)\s*[:=]\s*['\"][^'\"]+['\"]",
    re.IGNORECASE,
)
PROMPT_TONE_RE = re.compile(
    r"\bHint:|\bTask:|\bRead the|\bTry using\b|"
    r"\bReport the|\bWhich method|\bHow many regimes|\bUse the|\bLoad the|"
    r"\bTrain the|\bConsider fitting|\bObtain |"
    + re.escape(SHOULD_PHRASE)
    + r"|"
    + re.escape(SOLUTION_TERM)
    + r"|"
    + re.escape(PROMPT_ITEM_TERM)
    + r"|"
    + re.escape(ACCEPTABLE_PHRASE)
    + r"|"
    + re.escape(CREATE_FEATURE_PHRASE)
    + r"|"
    + re.escape(SAME_SPLIT_PHRASE),
    re.IGNORECASE,
)


def validate_text_file(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    location = str(path.relative_to(ROOT))

    for phrase in [*FORBIDDEN_MARKDOWN, SOURCE_NOTEBOOK_TITLE]:
        if phrase in text:
            errors.append(f"{location}: contains {phrase!r}")
    if GRADING_RE.search(text):
        errors.append(f"{location}: contains a scoring label")
    if ABSOLUTE_LOCAL_PATH_RE.search(text):
        errors.append(f"{location}: contains an absolute local path or cache reference")
    if EMAIL_RE.search(text):
        errors.append(f"{location}: contains an email address")
    if SECRET_RE.search(text):
        errors.append(f"{location}: contains a possible credential")

    return errors


def source_text(cell: dict) -> str:
    source = cell.get("source", "")
    if isinstance(source, list):
        return "".join(source)
    return source


def iter_text_fields(value: object, location: str = ""):
    if isinstance(value, str):
        yield location, value
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from iter_text_fields(item, f"{location}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            if key in {"image/png", "image/jpeg", "application/pdf"}:
                continue
            child_location = f"{location}.{key}" if location else str(key)
            yield from iter_text_fields(item, child_location)


def validate_notebook(path: Path) -> list[str]:
    errors: list[str] = []
    notebook = json.loads(path.read_text(encoding="utf-8"))

    for meta_location, meta_text in iter_text_fields(notebook.get("metadata", {}), f"{path.relative_to(ROOT)} metadata"):
        if ABSOLUTE_LOCAL_PATH_RE.search(meta_text) or ".venv" in meta_text:
            errors.append(f"{meta_location}: contains environment-specific metadata")

    for key in {"hide_input", "latex_envs", "toc", "varInspector"}:
        if key in notebook.get("metadata", {}):
            errors.append(f"{path.relative_to(ROOT)} metadata: contains public-unfriendly metadata key {key!r}")

    for index, cell in enumerate(notebook.get("cells", [])):
        text = source_text(cell)
        location = f"{path.relative_to(ROOT)} cell {index}"

        if cell.get("metadata"):
            errors.append(f"{location}: contains non-empty cell metadata")

        for phrase in FORBIDDEN_MARKDOWN:
            if phrase in text:
                errors.append(f"{location}: source contains {phrase!r}")
        if GRADING_RE.search(text):
            errors.append(f"{location}: source contains a scoring label")
        if PROMPT_TONE_RE.search(text):
            errors.append(f"{location}: source contains prompt-style wording")

        for output_index, output in enumerate(cell.get("outputs", [])):
            if output.get("output_type") == "error":
                errors.append(f"{location}.outputs[{output_index}]: contains an error output")

        for field_location, field_text in iter_text_fields(cell, location):
            if OPTIONAL_NN_SECTION in field_text:
                errors.append(f"{field_location}: contains optional neural network section")

            if "Kernel crashed" in field_text or "vscodeJupyterKernelCrash" in field_text:
                errors.append(f"{field_location}: contains a notebook kernel crash artifact")

            if ABSOLUTE_LOCAL_PATH_RE.search(field_text):
                errors.append(f"{field_location}: contains an absolute local path")

            if EMAIL_RE.search(field_text):
                errors.append(f"{field_location}: contains an email address")

            if SECRET_RE.search(field_text):
                errors.append(f"{field_location}: contains a possible credential")

            for match in BAD_NYSE_RE.finditer(field_text):
                context = field_text[max(0, match.start() - 20) : match.end() + 20]
                errors.append(f"{field_location}: NYSE.csv reference is not ../data/NYSE.csv ({context!r})")

    return errors


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_PATHS:
        if not path.exists():
            errors.append(f"Missing required path: {path.relative_to(ROOT)}")

    for path in RAW_SOURCE_NOTEBOOKS:
        if path.exists():
            errors.append(f"Raw source notebook should not remain in the repository root: {path.name}")

    for old_name in OLD_NOTEBOOK_NAMES:
        old_path = ROOT / "notebooks" / old_name
        if old_path.exists():
            errors.append(f"Old notebook filename should not remain: {old_path.relative_to(ROOT)}")

    for path in [
        ROOT / "README.md",
        ROOT / "requirements.txt",
        ROOT / ".gitignore",
        ROOT / "scripts" / "sanitize_notebooks.py",
        ROOT / "scripts" / "validate_repo.py",
    ]:
        if path.exists():
            errors.extend(validate_text_file(path))

    for path in REQUIRED_PATHS:
        if path.suffix == ".ipynb" and path.exists():
            errors.extend(validate_notebook(path))

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed.")
    print("Checked required files, notebook cleanup, local paths, optional section, and NYSE.csv references.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
