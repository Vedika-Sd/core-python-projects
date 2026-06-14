"""CSV data analyzer — basic stats for numeric columns, frequency info for
categorical columns. No numpy/pandas."""

import csv
import statistics
import sys
from pathlib import Path
from collections import Counter


def load_csv(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_numeric_columns(rows: list[dict]) -> dict[str, list[float]]:
    numeric = {}
    for col in rows[0]:
        values = []
        for r in rows:
            val = (r[col] or "").strip()
            if not val:
                continue
            try:
                values.append(float(val))
            except ValueError:
                break  
        else:
            if values:
                numeric[col] = values
    return numeric


def get_categorical_columns(
    rows: list[dict], numeric_cols: set[str], max_unique: int = 20
) -> dict[str, Counter]:
    categorical = {}
    for col in rows[0]:
        if col in numeric_cols:
            continue
        values = [(r[col] or "").strip() for r in rows if (r[col] or "").strip()]
        unique = set(values)
        if 0 < len(unique) <= max_unique:
            categorical[col] = Counter(values)
    return categorical


def print_numeric_summary(numeric: dict[str, list[float]]) -> None:
    if not numeric:
        return
    print(f"\n{'Column':20} {'Mean':>10} {'Median':>10} {'Mode':>10} {'Min':>10} {'Max':>10}")
    print("-" * 72)
    for col, vals in numeric.items():
        counts = Counter(vals)
        top_val, top_freq = counts.most_common(1)[0]
        mode = f"{top_val:.2f}" if top_freq > 1 else "n/a"
        print(
            f"{col:20}"
            f"{statistics.mean(vals):>10.2f}"
            f"{statistics.median(vals):>10.2f}"
            f"{mode:>10}"
            f"{min(vals):>10.2f}"
            f"{max(vals):>10.2f}"
        )


def print_categorical_summary(categorical: dict[str, Counter]) -> None:
    if not categorical:
        return
    print("\nCategorical columns:")
    for col, counts in categorical.items():
        print(f"\n  {col} ({len(counts)} unique values)")
        for value, freq in counts.most_common():
            print(f"    {value:20} {freq}")


def analyse(filepath: str) -> None:
    rows = load_csv(filepath)
    if not rows:
        print("CSV file is empty.")
        return

    print(f"\n{filepath}  ({len(rows)} rows, {len(rows[0])} columns)")

    numeric = get_numeric_columns(rows)
    categorical = get_categorical_columns(rows, set(numeric))

    print_numeric_summary(numeric)
    print_categorical_summary(categorical)


def main() -> None:
    path = sys.argv[1] if len(sys.argv) >= 2 else input("Enter path to CSV file: ").strip()

    if not Path(path).exists():
        print(f"File not found: {path}")
        sys.exit(1)

    analyse(path)


if __name__ == "__main__":
    main()