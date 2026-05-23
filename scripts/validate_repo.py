"""Validate the portfolio notebook repository structure and cleanup rules."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    ROOT / "notebooks" / "01_housing_preprocessing.ipynb",
    ROOT / "notebooks" / "02_time_series_random_forest_svm.ipynb",
    ROOT / "notebooks" / "03_pca_clustering.ipynb",
    ROOT / "data" / "NYSE.csv",
]

FORBIDDEN_MARKDOWN = [
    "CFRM 421/521",
    "Gradescope",
    "Due:",
    "Late submissions",
]

GRADING_RE = re.compile(
    r"[\[(]\s*\d+(?:\.\d+)?\s*(?:marks?|points?)\s*[\])]",
    re.IGNORECASE,
)
ABSOLUTE_LOCAL_PATH_RE = re.compile(
    r"(?:(?<![A-Za-z])[A-Za-z]:[\\/][^\s'\"`),]+|/(?:Users|home)/[^\s'\"`),]+)"
)
BAD_NYSE_RE = re.compile(r"(?<!\.\./data/)NYSE\.csv")


def source_text(cell: dict) -> str:
    source = cell.get("source", "")
    if isinstance(source, list):
        return "".join(source)
    return source


def validate_notebook(path: Path) -> list[str]:
    errors: list[str] = []
    notebook = json.loads(path.read_text(encoding="utf-8"))

    for index, cell in enumerate(notebook.get("cells", [])):
        text = source_text(cell)
        location = f"{path.relative_to(ROOT)} cell {index}"

        if cell.get("cell_type") == "markdown":
            for phrase in FORBIDDEN_MARKDOWN:
                if phrase in text:
                    errors.append(f"{location}: markdown contains {phrase!r}")
            if GRADING_RE.search(text):
                errors.append(f"{location}: markdown contains a grading mark")

        if "Optional exercise: Neural Networks" in text:
            errors.append(f"{location}: contains optional neural network section")

        if ABSOLUTE_LOCAL_PATH_RE.search(text):
            errors.append(f"{location}: contains an absolute local path")

        for match in BAD_NYSE_RE.finditer(text):
            context = text[max(0, match.start() - 20) : match.end() + 20]
            errors.append(f"{location}: NYSE.csv reference is not ../data/NYSE.csv ({context!r})")

    return errors


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_PATHS:
        if not path.exists():
            errors.append(f"Missing required path: {path.relative_to(ROOT)}")

    for path in REQUIRED_PATHS:
        if path.suffix == ".ipynb" and path.exists():
            errors.extend(validate_notebook(path))

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed.")
    print("Checked required notebooks, data file, markdown cleanup, local paths, optional section, and NYSE.csv references.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
