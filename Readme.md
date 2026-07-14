# Netflix Catalogue Intelligence

A professional Streamlit dashboard built on top of a fully cleaned Netflix
movies dataset.

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