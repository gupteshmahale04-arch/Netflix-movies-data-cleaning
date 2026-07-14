# Netflix Movies Dataset — Data Cleaning Project

A comprehensive, step-by-step Jupyter Notebook solution demonstrating real-world data cleaning techniques using Python, NumPy, and Pandas. This project transforms a highly inconsistent and messy dataset (`netflix_movies_dirty.csv`) into a structured, reliable, and analysis-ready format.

---

## 📌 Project Overview

Data analysts spend up to 80% of their time cleaning data. This project serves as a practical blueprint for identifying and systematically resolving common data quality issues found in production-level datasets. 

Every processing section in the notebook follows a transparent pedagogical pattern:
1. **Problem Found** — What anomaly or inconsistency was discovered.
2. **Why is this a problem?** — The real-world impact on downstream business logic or statistical analytics.
3. **How can we solve it?** — The strategic plan before touching the code.
4. **Code Implementation** — Clean, documented, and beginner-friendly Python solution.
5. **Explanation** — Breakdown of what exactly happened under the hood.

---

## 🛠️ Data Quality Issues Resolved

The pipeline implements an end-to-end cleaning workflow tackling the following issues across 17 data columns:

| Step | Target Attribute / Column | Problem Identified | Resolution Strategy |
| :--- | :--- | :--- | :--- |
| **04** | `Movie_ID` | Duplicate unique identifiers | Kept the first chronological record using `.drop_duplicates()` |
| **05** | `Title` | Structural noise (whitespace, line breaks, casing inconsistencies, trailing exclamation marks) | Developed custom `clean_title()` regex parser |
| **06** | `Genre` | Mixed delimiters (`/`, `,`, `\|`) and multi-categorical formats | Consolidated separators and extracted the *Primary Genre* only |
| **07** | `Release_Year` | Domain-rule outliers (e.g., years `1890` and `2099`) | Filtered via strict chronological domain boundaries (1900–2025) |
| **08** | `Duration` | Mixed metrics and string representations (e.g., `3h 13m` vs `160mins`) | Implemented custom multi-format parsing functions to normalize to minutes |
| **09** | `Rating` | Numerical data stored strictly as text objects | Coerced types safely using `pd.to_numeric(errors="coerce")` |
| **10** | `IMDb_Rating` | Extreme logical outliers outside the standard `[0, 10]` scale | Nullified invalid out-of-bounds ratings to protect statistical means |
| **11** | `Votes` | String-formatted numbers containing thousands commas (e.g., `"1,558,685"`) | Stripped formatting characters and cast to integer types |
| **12-13**| `Budget` & `Revenue` | Financial currency symbols (`$`), commas, and invalid `<= 0` records | Formatted string to float; coerced unrealistic zero-revenues to    `NaN` |
| **14** | `Date_Added` | Dates saved simultaneously across 4 distinct formats | Created a 10-digit compact regex patch and unified with `pd.to_datetime()` |
| **15-16**| `Country` & `Language` | Synonyms, casing variants, and abbreviations (e.g., `USA`, `U.S.`, `Hin`, `Eng`) | Handled mapping variants accurately using programmatic dictionary lookup tables |
| **18** | Near-Duplicates | Rows sharing identical `Title` and `Release_Year` values | Eliminated redundant observations while safely preserving original remakes/sequels |
| **19** | Missing Fields | Scattered missing descriptive metadata and numeric inputs | Handled metadata using `NaN` boundaries; filled specific numeric metrics via median |
| **20** | Data Types | Floating-point conversion decay caused by native Python handling of `NaN` | Converted targeted columns to Pandas' nullable integer type (`"Int64"`) |

---

## 🚀 Key Learning Takeaways

By exploring this repository, you will master how to:
* Handle missing entries strategically without creating data bias (e.g., knowing when to drop   rows vs. when to impute with the median value ).
* Write custom text-processing logic to apply across entire dataframes using `.apply()` .
* Enforce ** Domain-Rule Validations** to trap anomalies that automated validation checks miss.
* Utilize Pandas' nullable integer types (`"Int64"`) to allow integer columns to retain structural `NaN` values without   altering data shapes .

---

## 💻 Tech Stack & Environment

* **Language:** Python 3.10+
* **Libraries:** Pandas, NumPy
* **Environment:** Jupyter Notebook / Google Colab

## 📦 Getting Started

1. Clone this repository to your local computer:
   ```bash
   git clone [https://github.com/gupteshmahale04-arch/Netflix-movies-data-cleaning.git](https://github.com/gupteshmahale04-arc/Netflix-movies-data-cleaning.git)

   ## Files

- `clean_data.py` — standalone cleaning pipeline (rebuilt from your notebook,
  with gaps filled in and a few bugs fixed: genre extraction, country/language
  lookups, duration parsing). Reads the raw CSV and writes
  `netflix_movies_clean.csv`.
- `netflix_movies_clean.csv` — the cleaned dataset (1,147 of 1,560 rows kept
  after dropping unusable/duplicate records).
- `app.py` — the Streamlit dashboard.
- `requirements.txt` — dependencies.

## Run it locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually http://localhost:8501).

## What's in the dashboard

- **Sidebar filters** — year range, genre, country, language, age rating,
  minimum IMDb score, and a free-text search on title/director.
- **Overview KPIs** — titles in view, average IMDb rating, average runtime,
  combined revenue, leading genre.
- **Catalogue tab** — titles per year, genre mix, IMDb rating distribution,
  runtime by genre.
- **Box Office tab** — budget vs. revenue scatter, revenue by genre, top
  titles by vote count.
- **Geography tab** — choropleth of titles by country, language breakdown.
- **Explore Data tab** — sortable full table with a CSV download button for
  whatever's currently filtered.

## Re-running the cleaning step

If you want to regenerate `netflix_movies_clean.csv` from the raw file:

```bash
python3 clean_data.py
```

It expects the raw file at `netflix_movies_dirty.csv` in the same folder —
update `RAW_PATH` at the top of the script if yours lives elsewhere.
