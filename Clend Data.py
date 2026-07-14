"""
Netflix Movies — Data Cleaning Pipeline
Rebuilt from netflix_cleaning.ipynb, with gaps filled in and a few bugs fixed
(e.g. clean_genre used to keep everything before the first space instead of
the first comma/pipe/slash-separated genre; clean_country / clean_language
lookups now match case-insensitively; clean_duration now handles the
"mins" vs "min" vs plain-number vs "Xh Ym" formats safely).
"""

import numpy as np
import pandas as pd

RAW_PATH = "/mnt/user-data/uploads/netflix_movies_dirty.csv"
CLEAN_PATH = "/home/claude/netflix_app/netflix_movies_clean.csv"


def clean_title(title):
    if pd.isnull(title):
        return np.nan
    title = str(title).replace("\n", " ").replace("\t", " ")
    title = " ".join(title.split())
    title = title.rstrip("!").rstrip()
    # Trim overly long "extended edition" style titles at the first parenthesis
    if "(" in title:
        cut = title.index("(")
        if cut > 0:
            title = title[:cut].strip()
    title = title.title()
    return title if title else np.nan


def clean_genre(genre):
    if pd.isnull(genre):
        return np.nan
    genre = str(genre).replace("\n", " ").replace("\t", " ").strip()
    for sep in ["|", "/"]:
        genre = genre.replace(sep, ",")
    genre = genre.split(",")[0]
    genre = " ".join(genre.split())
    return genre.title() if genre else np.nan


def clean_year(year):
    try:
        if pd.isnull(year):
            return np.nan
        year = float(year)
        if year < 1900 or year > 2025:
            return np.nan
        return year
    except (ValueError, TypeError):
        return np.nan


def clean_duration(duration):
    if pd.isnull(duration):
        return np.nan
    d = str(duration).strip().lower()
    try:
        if "h" in d:
            hours, minutes = d.split("h")
            hours = int(hours.strip())
            minutes = minutes.replace("m", "").strip()
            minutes = int(minutes) if minutes else 0
            total = hours * 60 + minutes
        elif "min" in d:
            total = int(d.replace("mins", "").replace("min", "").strip())
        else:
            total = int(float(d))
    except (ValueError, TypeError):
        return np.nan
    if total < 30 or total > 600:
        return np.nan
    return total


def clean_rating(rating):
    try:
        if pd.isnull(rating):
            return np.nan
        return float(rating)
    except (ValueError, TypeError):
        return np.nan


def clean_imdb(rating):
    r = clean_rating(rating)
    if pd.isnull(r):
        return np.nan
    if r > 10 or r < 0:
        return np.nan
    return r


def clean_votes(votes):
    if pd.isnull(votes):
        return np.nan
    v = str(votes).replace(",", "").strip()
    try:
        return int(float(v))
    except (ValueError, TypeError):
        return np.nan


def clean_budget(budget):
    if pd.isnull(budget):
        return np.nan
    b = str(budget).replace("$", "").replace(",", "").strip()
    try:
        b = float(b)
    except (ValueError, TypeError):
        return np.nan
    return np.nan if b < 0 else b


def clean_revenue(revenue):
    if pd.isnull(revenue):
        return np.nan
    r = str(revenue).replace("$", "").replace(",", "").strip()
    try:
        r = float(r)
    except (ValueError, TypeError):
        return np.nan
    return np.nan if r <= 0 else r


COUNTRY_MAP = {
    "u.s.": "United States", "us": "United States", "usa": "United States",
    "u.s.a": "United States", "united states": "United States",
    "u.k.": "United Kingdom", "uk": "United Kingdom",
    "britain": "United Kingdom", "united kingdom": "United Kingdom",
}


def clean_country(value):
    if pd.isnull(value):
        return np.nan
    v = str(value).strip()
    key = v.lower()
    return COUNTRY_MAP.get(key, v.title())


LANGUAGE_MAP = {
    "eng": "English", "english": "English",
    "hin": "Hindi", "hindi": "Hindi",
    "kor": "Korean", "korean": "Korean",
    "ger": "German", "german": "German",
    "fre": "French", "french": "French",
    "jap": "Japanese", "japanese": "Japanese",
    "spa": "Spanish", "spanish": "Spanish",
    "ita": "Italian", "italian": "Italian",
    "chinese": "Chinese",
}


def clean_language(lang):
    if pd.isnull(lang):
        return np.nan
    key = str(lang).strip().lower()
    return LANGUAGE_MAP.get(key, str(lang).strip().title())


def clean_date(series):
    s = series.astype(str).str.strip()
    # Compact YYYYMMDD -> YYYY-MM-DD so pd.to_datetime can parse it too
    compact_mask = s.str.match(r"^\d{8}$")
    s = s.where(~compact_mask, s.str[:4] + "-" + s.str[4:6] + "-" + s.str[6:8])
    return pd.to_datetime(s, format="mixed", errors="coerce")


def clean_text_field(value):
    if pd.isnull(value):
        return np.nan
    v = " ".join(str(value).replace("\n", " ").replace("\t", " ").split())
    return v if v else np.nan


def run_pipeline():
    df = pd.read_csv(RAW_PATH, dtype=str)
    original_rows = len(df)

    # Drop rows missing a Movie_ID entirely
    df = df.dropna(subset=["Movie_ID"])
    # Remove duplicate Movie_IDs, keep first
    df = df.drop_duplicates(subset="Movie_ID", keep="first")

    df["Title"] = df["Title"].apply(clean_title)
    df = df.dropna(subset=["Title"])

    df["Genre"] = df["Genre"].apply(clean_genre)
    df["Release_Year"] = df["Release_Year"].apply(clean_year)
    df["Duration"] = df["Duration"].apply(clean_duration)
    df["Rating"] = df["Rating"].apply(clean_rating)
    df["IMDb_Rating"] = df["IMDb_Rating"].apply(clean_imdb)
    df["Votes"] = df["Votes"].apply(clean_votes)
    df["Budget"] = df["Budget"].apply(clean_budget)
    df["Revenue"] = df["Revenue"].apply(clean_revenue)
    df["Date_Added"] = clean_date(df["Date_Added"])
    df["Country"] = df["Country"].apply(clean_country)
    df["Language"] = df["Language"].apply(clean_language)
    df["Age_Rating"] = df["Age_Rating"].apply(clean_text_field)
    df["Director"] = df["Director"].apply(clean_text_field)
    df["Cast"] = df["Cast"].apply(clean_text_field)
    df["Production_House"] = df["Production_House"].apply(clean_text_field)

    # Near-duplicate rows: same Title + Release_Year
    df = df.drop_duplicates(subset=["Title", "Release_Year"], keep="first")

    # Fill remaining numeric gaps with median (robust to outliers)
    for col in ["Duration", "Rating", "IMDb_Rating", "Votes"]:
        df[col] = df[col].fillna(df[col].median())
    # Release_Year: fill with median, keep as nullable Int
    df["Release_Year"] = df["Release_Year"].fillna(df["Release_Year"].median())

    # Final dtypes
    df["Release_Year"] = df["Release_Year"].astype("Int64")
    df["Duration"] = df["Duration"].round().astype("Int64")
    df["Votes"] = df["Votes"].round().astype("Int64")
    df["Rating"] = df["Rating"].round(1)
    df["IMDb_Rating"] = df["IMDb_Rating"].round(1)
    df["Budget"] = df["Budget"].round(0)
    df["Revenue"] = df["Revenue"].round(0)

    df = df.reset_index(drop=True)

    print(f"Original rows: {original_rows}")
    print(f"Cleaned rows:  {len(df)}")
    print(f"Rows removed:  {original_rows - len(df)}")
    print(df.isnull().sum())

    df.to_csv(CLEAN_PATH, index=False)
    print(f"\nSaved cleaned dataset -> {CLEAN_PATH}")
    return df


if __name__ == "__main__":
    run_pipeline()