# 🌀 Core Python Projects : 

A collection of small, focused Python projects — each one built to go deep on a
specific set of core language concepts, the way production code is written:
typed, error-handled, and runnable from the command line.

This isn't a "100 Python exercises" repo. Each project is developed by myself to learn and implemnt python concepts properly. Every line earns its place,
no boilerplate, no unused imports, no half-finished functions.

> *"Beautiful is better than ugly. Explicit is better than implicit. Simple is
> better than complex." — The Zen of Python*

---

## Projects

### 1. Log Analyzer — `01_log_analyzer.py`

A command-line tool that streams a log file and summarizes it: severity-level
counts, the time range covered, and the top recurring messages.

**Why it's interesting:**
- **Generators** — `read_lines()` uses `yield` to process the file one line at
  a time. A 5-line sample log and a 5 GB production log run with the *same*
  memory footprint.
- **Decorators** — `@timer` wraps `analyse()` and reports how long it took,
  using `functools.wraps` so the wrapped function keeps its original name and
  docstring.
- **Named regex groups** — `(?P<level>\w+)` lets the code read `match["level"]`
  instead of `match.group(2)`, which stays readable even if the pattern grows.
- **`Counter.most_common()`** — aggregates severity levels and repeated
  messages without manual dictionary bookkeeping.

**Run it:**
```bash
python 01_log_analyzer.py data1_sample.log
```

**Sample output:**

<img width="554" height="312" alt="image" src="https://github.com/user-attachments/assets/f9957d18-5c7d-43fb-84eb-7190217e478b" />

---

### 2. CSV Data Analyzer — `02_csv_data_Analyzer.py`

Reads a CSV and computes summary statistics **without pandas or numpy** —
to show the statistics actually understood, not just imported.

**Why it's interesting:**
- **`csv.DictReader`** — each row becomes a dict keyed by header, so columns
  are addressed by name (`row["Groceries"]`) instead of brittle index numbers.
- **`for...else` (an underused Python feature)** — `get_numeric_columns()`
  tries to convert every value in a column to `float`. If *any* value fails,
  `break` skips the `else`, and the whole column is excluded from numeric
  stats. One bad value correctly disqualifies the column — no partial/garbage
  averages.
- **Mode via `Counter`, not `statistics.mode`** — for continuous data (prices,
  spending amounts) every value is often unique, so `statistics.mode` would
  return a misleading "first value seen." Here, mode is only reported if a
  value actually repeats — otherwise it prints `n/a`.
- **Categorical detection** — any non-numeric column with a small number of
  unique values (≤ 20) gets a frequency breakdown automatically.

**Run it:**
```bash
python 02_csv_data_Analyzer.py data2_customer_spending.csv
```

**Sample output:**

<img width="554" height="312" alt="image" src="https://github.com/user-attachments/assets/30d83f89-ae29-4515-9d56-3d5fcc7e9a7a" />

---

### 3. OOP Bank System — `03_oop_bank_system.py`

A small banking system that's actually about **object-oriented design**, not
just "classes that hold data."

**Why it's interesting:**
- **Abstract Base Class (`ABC` + `@abstractmethod`)** — `Account.withdraw()` is
  declared but not implemented. Python *refuses to let you instantiate*
  `Account` directly — you're forced to define a subclass that decides what
  "withdraw" means.
- **Polymorphism, not just inheritance** — `SavingsAccount` enforces a ₹1,000
  minimum balance; `CurrentAccount` allows overdraft up to ₹5,000. Same method
  name (`withdraw`), same call site (`account.withdraw(amount)`), completely
  different rules — the calling code never needs to know which type it has.
- **Custom exception hierarchy** — `InsufficientFundsError` is separated from
  Python's built-in `ValueError`. This means "you typed a negative number"
  (`ValueError`) and "your account rules don't allow this" (`InsufficientFundsError`)
  can be caught and handled differently.
- **Encapsulation** — `Bank` owns a private `_accounts` dict. Account lookup,
  creation, and listing all go through `Bank`'s methods; nothing outside the
  class touches the dict directly.
- **Dunder methods** — `Transaction.__str__` and `Account.__str__` give every
  object a sensible human-readable representation, used automatically by
  `print()`.

**Run it:**
```bash
python 03_oop_bank_system.py
```
Then use the interactive menu to open an account, deposit, withdraw, transfer
between accounts, and view statements. Try withdrawing below the ₹1,000
minimum on a savings account, or beyond the ₹5,000 overdraft on a current
account, to see `InsufficientFundsError` caught and reported cleanly.

**Sample Output:** 

<img width="554" height="312" alt="image" src="https://github.com/user-attachments/assets/adb78f05-1bf9-4dc5-be19-0ddc964af85d" />


---

### 4. Text File Search Engine — `04_text_file_search_Engine.py`

A miniature search engine: builds an **inverted index** over `.txt` files in a
folder, then ranks files by how many query words they contain — the same core
idea behind real search systems, just without the scale.

**Why it's interesting:**
- **Inverted index with `defaultdict(set)`** — instead of "file → words it
  contains," the index is "word → set of files containing it." This is the
  data structure that makes search fast: looking up a word is O(1), not a
  scan of every file.
- **Stopword filtering** — common words ("the", "is", "and") are stripped
  during tokenizing. Without this, every file would score highly on every
  query just from shared filler words, making the ranking meaningless.
- **Set comprehensions + regex** — `tokenise()` does lowercasing, word
  extraction, and stopword filtering in a single readable line.
- **Relevance scoring** — results show `score/total query words matched`,
  giving a sense of *how relevant* a match is, not just a raw count.

**Run it:**
```bash
python 04_text_file_search_Engine.py .
```
This indexes `data3_AI_Ethics.txt` in the repo root. Try searching for terms
like `ethics regulation` or `data privacy` and you'll see the file and its
match score.

**Sample Output:**

<img width="554" height="312" alt="image" src="https://github.com/user-attachments/assets/dc7af0f7-10fd-4307-ae54-fa51569a0b81" />

---

### 5. Web Scraper — `05_web_scrapper.py`

Fetches book listings from [books.toscrape.com](http://books.toscrape.com/) —
a sandbox site built specifically for scraping practice — parses them with
BeautifulSoup, and saves the results as JSON.

**Why it's interesting:**
- **Defensive HTTP** — `fetch()` sets a `User-Agent`, a `timeout`, and calls
  `raise_for_status()` so a 404/500 response raises immediately instead of
  silently returning a useless page. All of it wrapped in
  `try/except requests.RequestException`.
- **Compound CSS selectors** — `item.select_one("p.instock.availability")`
  matches an element with *both* CSS classes. (`find(class_="instock availability")`
  — the more common but incorrect approach — doesn't reliably match multi-class
  attributes in BeautifulSoup.)
- **`urljoin`** — converts relative links (`catalogue/a-book/index.html`) into
  full, usable URLs relative to the page they were found on.
- **Dataclass → JSON** — `Book` is a `@dataclass`; `asdict()` converts each
  instance to a dict for `json.dump`, with `ensure_ascii=False` so currency
  symbols like `£` are written as real characters, not `\u00a3` escapes.

**Run it:**
```bash
pip install requests beautifulsoup4
python 05_web_scrapper.py
```
Prints the first 5 books with price and stock status, then saves all 20 to
`report.json`.

**Sample Output:**

<img width="554" height="312" alt="image" src="https://github.com/user-attachments/assets/790195d2-e7ee-47c3-8e5d-c9682753273f" />

---
### Fun Project: Dream Catcher — `DreamCatcher.py`

A "just for fun" script — built with `matplotlib` and `numpy`. It draws a dream catcher, and asks *you* for your dreams — placing
each one as text inside the web, using a collision-avoidance algorithm so they
don't overlap, falling back to a golden-angle spiral layout if the circle gets
crowded.
Type in a few dreams, hit `done`, and watch them appear inside the web.
```bash
python DreamCatcher.py
```

**Output:**

<img width="1364" height="646" alt="image" src="https://github.com/user-attachments/assets/7d23ce35-a0d4-4e56-9de3-4e3fcd3e9255" />

---
## Setup

All projects use **Python 3.10+** and the standard library, except the web
scraper and the bonus Dream Catcher:

```bash
pip install requests beautifulsoup4 matplotlib numpy
```

---

> It's a small reminder that this repo isn't just about proving proficiency —
it's about a genuine love for what Python lets you build, from log parsers to
dream catchers. Every project above started as "let me see if I can build
this," and that curiosity is the thing worth carrying into whatever comes
next. 

