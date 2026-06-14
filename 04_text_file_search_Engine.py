"""Mini text file search engine — builds an inverted word index over .txt
files in a folder and ranks files by how many query words they contain."""

from pathlib import Path
from collections import defaultdict
import re
import sys

STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "in", "on", "of", "to",
    "for", "and", "or", "as", "by", "with", "it", "this", "that", "be",
    "at", "from", "but", "not", "can", "will",
}


def tokenise(text: str) -> set[str]:
    """Lowercase, extract words, drop stopwords and noise."""
    words = re.findall(r"\b[a-z]{2,}\b", text.lower())
    return {w for w in words if w not in STOPWORDS}


def build_index(folder: str) -> dict[str, set[str]]:
    """Map each word -> set of .txt filenames that contain it."""
    index: dict[str, set[str]] = defaultdict(set)
    for path in Path(folder).glob("**/*.txt"):
        for word in tokenise(path.read_text(errors="ignore")):
            index[word].add(path.name)
    return dict(index)


def search(index: dict[str, set[str]], query: str) -> list[tuple[str, int]]:
    """Return (filename, match_count) sorted by how many query words matched."""
    query_words = tokenise(query)
    scores: dict[str, int] = defaultdict(int)
    for word in query_words:
        for filename in index.get(word, ()):
            scores[filename] += 1
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def main() -> None:
    folder = sys.argv[1] if len(sys.argv) >= 2 else input("Folder to search: ").strip()

    if not Path(folder).is_dir():
        print(f"Not a folder: {folder}")
        sys.exit(1)

    index = build_index(folder)
    if not index:
        print(f"No .txt files found in {folder}")
        return

    print(f"Indexed {len(index)} unique words from {folder}\n")

    while True:
        query = input("Search (blank to quit): ").strip()
        if not query:
            break

        query_words = tokenise(query)
        if not query_words:
            print("  (query had no usable words — try different terms)\n")
            continue

        results = search(index, query)
        if not results:
            print("  No matches.\n")
            continue

        for filename, score in results:
            print(f"  {filename:30} {score}/{len(query_words)} terms matched")
        print()


if __name__ == "__main__":
    main()