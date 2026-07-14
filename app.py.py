import pandas as pd


import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Netflix Catalogue Intelligence",
    
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# Design system — "screening room" theme
# Palette: near-black stage (#0B0D10), warning-tape red (#E50914 used sparingly
# as the single accent), warm marquee gold (#E8B94D) for secondary highlights,
# projector-grey text tiers. Type: a tall condensed display face for headings
# (Bebas Neue) paired with a workmanlike grotesk (Inter) for body/data.
# ----------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root{
    --stage:#0B0D10;
    --stage-2:#111418;
    --panel:#15181D;
    --panel-border:#22262D;
    --red:#E50914;
    --gold:#E8B94D;
    --text-hi:#F2F2F0;
    --text-mid:#A7ADB5;
    --text-lo:#686F79;
}

html, body, [class*="css"]{
    font-family:'Inter', sans-serif;
}

.stApp{
    background:
        radial-gradient(ellipse 900px 500px at 15% -10%, rgba(229,9,20,0.10), transparent 60%),
        radial-gradient(ellipse 700px 500px at 100% 0%, rgba(232,185,77,0.06), transparent 55%),
        var(--stage);
    color: var(--text-hi);
}

/* Kill default streamlit chrome */
#MainMenu, footer, header{visibility:hidden;}
.block-container{padding-top:2rem; padding-bottom:3rem; max-width:1340px;}

/* ---------- Marquee header ---------- */
.marquee{
    display:flex; align-items:baseline; gap:14px;
    border-bottom:1px solid var(--panel-border);
    padding-bottom:18px; margin-bottom:6px;
}
.marquee .slash{ color:var(--red); font-family:'Bebas Neue', sans-serif; font-size:2.6rem; line-height:1;}
.marquee h1{
    font-family:'Bebas Neue', sans-serif;
    font-weight:400;
    letter-spacing:0.03em;
    font-size:2.6rem;
    color:var(--text-hi);
    margin:0;
    line-height:1;
}
.marquee .tag{
    font-family:'JetBrains Mono', monospace;
    font-size:0.72rem;
    color:var(--text-lo);
    text-transform:uppercase;
    letter-spacing:0.12em;
    margin-left:auto;
    padding-top:6px;
}
.subhead{
    font-size:0.92rem; color:var(--text-mid); margin:10px 0 28px 0; max-width:720px;
}

/* ---------- Section labels ---------- */
.section-eyebrow{
    font-family:'JetBrains Mono', monospace;
    font-size:0.7rem;
    letter-spacing:0.14em;
    text-transform:uppercase;
    color:var(--gold);
    margin: 30px 0 10px 0;
    display:flex; align-items:center; gap:10px;
}
.section-eyebrow::after{
    content:"";
    flex:1;
    height:1px;
    background:var(--panel-border);
}

/* ---------- KPI stat cards ---------- */
.stat-row{ display:flex; gap:14px; flex-wrap:wrap; }
.stat-card{
    background:var(--panel);
    border:1px solid var(--panel-border);
    border-radius:6px;
    padding:16px 18px;
    flex:1;
    min-width:150px;
    position:relative;
    overflow:hidden;
}
.stat-card::before{
    content:"";
    position:absolute; left:0; top:0; bottom:0; width:3px;
    background:var(--red);
}
.stat-label{
    font-family:'JetBrains Mono', monospace;
    font-size:0.66rem;
    letter-spacing:0.1em;
    text-transform:uppercase;
    color:var(--text-lo);
    margin-bottom:8px;
}
.stat-value{
    font-family:'Bebas Neue', sans-serif;
    font-size:2.1rem;
    color:var(--text-hi);
    line-height:1;
}
.stat-sub{ font-size:0.74rem; color:var(--text-mid); margin-top:6px;}

/* ---------- Panel wrapper for charts ---------- */
.panel{
    background:var(--panel);
    border:1px solid var(--panel-border);
    border-radius:6px;
    padding:18px 20px 8px 20px;
}
.panel-title{
    font-weight:700; font-size:0.95rem; color:var(--text-hi); margin-bottom:2px;
}
.panel-caption{
    font-size:0.76rem; color:var(--text-lo); margin-bottom:10px;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"]{
    background:var(--stage-2);
    border-right:1px solid var(--panel-border);
}
section[data-testid="stSidebar"] .block-container{padding-top:1.6rem;}
.sidebar-title{
    font-family:'Bebas Neue', sans-serif;
    font-size:1.5rem;
    letter-spacing:0.03em;
    color:var(--text-hi);
    border-bottom:1px solid var(--panel-border);
    padding-bottom:12px;
    margin-bottom:18px;
}
.sidebar-title span{color:var(--red);}

/* Streamlit widget label tone-down */
label, .stMarkdown p{ color:var(--text-mid) !important; }
section[data-testid="stSidebar"] label { font-size:0.8rem !important; font-weight:600 !important; color:var(--text-hi) !important;}

/* Selectbox / multiselect chips */
div[data-baseweb="select"] > div{
    background:var(--panel) !important;
    border-color:var(--panel-border) !important;
}
span[data-baseweb="tag"]{
    background:var(--red) !important;
}

/* DataFrame */
[data-testid="stDataFrame"]{
    border:1px solid var(--panel-border);
    border-radius:6px;
    overflow:hidden;
}

/* Divider */
hr{ border-color: var(--panel-border); }

/* Footer credit */
.credit{
    font-family:'JetBrains Mono', monospace;
    font-size:0.68rem;
    color:var(--text-lo);
    text-align:center;
    margin-top:40px;
    letter-spacing:0.05em;
}

/* Tabs */
button[data-baseweb="tab"]{
    font-family:'Inter', sans-serif;
    font-weight:600;
    color:var(--text-mid);
}
button[data-baseweb="tab"][aria-selected="true"]{
    color:var(--text-hi) !important;
}
div[data-baseweb="tab-highlight"]{
    background-color: var(--red) !important;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

PLOTLY_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#A7ADB5", size=12),
        title_font=dict(family="Inter, sans-serif", color="#F2F2F0", size=14),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="#22262D", zerolinecolor="#22262D"),
        yaxis=dict(gridcolor="#22262D", zerolinecolor="#22262D"),
        margin=dict(l=10, r=10, t=40, b=10),
    )
)
ACCENT_RED = "#E50914"
ACCENT_GOLD = "#E8B94D"
SEQ_PALETTE = ["#E50914", "#E8B94D", "#8C1017", "#B3862E", "#5C5F66",
               "#F2637A", "#F0D28C", "#3D4048", "#C4404C", "#7A5C1E"]


# ----------------------------------------------------------------------------
# Data loading
# ----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_movies_clean.csv")
    df["Date_Added"] = pd.to_datetime(df["Date_Added"], errors="coerce")
    return df


df = load_data()

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="marquee">
        <span class="slash">//</span>
        <h1>NETFLIX CATALOGUE INTELLIGENCE</h1>
        <span class="tag">Cleaned Dataset &middot; 1,147 Titles</span>
    </div>
    <div class="subhead">
        An exploratory dashboard built on a fully cleaned and validated Netflix
        movies dataset &mdash; deduplicated IDs, standardised genres, currencies,
        dates, countries and languages, with domain-rule outlier handling on
        ratings, runtime, budget and revenue.
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Sidebar filters
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">FILTER<span>.</span>ROOM</div>', unsafe_allow_html=True)

    year_min, year_max = int(df["Release_Year"].min()), int(df["Release_Year"].max())
    year_range = st.slider("Release year", year_min, year_max, (year_min, year_max))

    genres = sorted(df["Genre"].dropna().unique())
    pick_genres = st.multiselect("Genre", genres, default=[])

    countries = sorted(df["Country"].dropna().unique())
    pick_countries = st.multiselect("Country", countries, default=[])

    languages = sorted(df["Language"].dropna().unique())
    pick_languages = st.multiselect("Language", languages, default=[])

    age_ratings = sorted(df["Age_Rating"].dropna().unique())
    pick_age = st.multiselect("Age rating", age_ratings, default=[])

    min_imdb = st.slider("Minimum IMDb rating", 0.0, 10.0, 0.0, 0.1)

    st.markdown("---")
    search = st.text_input("Search title / director", "")

mask = (
    df["Release_Year"].between(year_range[0], year_range[1])
    & (df["IMDb_Rating"].fillna(0) >= min_imdb)
)
if pick_genres:
    mask &= df["Genre"].isin(pick_genres)
if pick_countries:
    mask &= df["Country"].isin(pick_countries)
if pick_languages:
    mask &= df["Language"].isin(pick_languages)
if pick_age:
    mask &= df["Age_Rating"].isin(pick_age)
if search:
    s = search.lower()
    mask &= (
        df["Title"].str.lower().str.contains(s, na=False)
        | df["Director"].str.lower().str.contains(s, na=False)
    )

fdf = df[mask].copy()

# ----------------------------------------------------------------------------
# KPI row
# ----------------------------------------------------------------------------
st.markdown('<div class="section-eyebrow">Overview</div>', unsafe_allow_html=True)

total_titles = len(fdf)
avg_imdb = fdf["IMDb_Rating"].mean()
avg_runtime = fdf["Duration"].mean()
total_revenue = fdf["Revenue"].sum(skipna=True)
top_genre = fdf["Genre"].mode().iloc[0] if not fdf.empty else "—"

k1, k2, k3, k4, k5 = st.columns(5)
kpi_data = [
    (k1, "Titles in view", f"{total_titles:,}", f"of {len(df):,} total"),
    (k2, "Avg IMDb rating", f"{avg_imdb:.1f}" if pd.notna(avg_imdb) else "—", "out of 10"),
    (k3, "Avg runtime", f"{avg_runtime:.0f} min" if pd.notna(avg_runtime) else "—", "per title"),
    (k4, "Combined revenue", f"${total_revenue/1e9:.2f}B" if total_revenue else "$0", "reported titles only"),
    (k5, "Leading genre", top_genre, "by title count"),
]
for col, label, value, sub in kpi_data:
    with col:
        st.markdown(
            f"""<div class="stat-card">
                    <div class="stat-label">{label}</div>
                    <div class="stat-value">{value}</div>
                    <div class="stat-sub">{sub}</div>
                </div>""",
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Tabs
# ----------------------------------------------------------------------------
tab_overview, tab_money, tab_geo, tab_table = st.tabs(
    ["📊 Catalogue", "💰 Box Office", "🌍 Geography", "🗂 Explore Data"]
)

# ---- Tab 1: Catalogue ----
with tab_overview:
    c1, c2 = st.columns([1.1, 1])

    with c1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Titles added, by year</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-caption">Release year distribution across the filtered catalogue</div>', unsafe_allow_html=True)
        year_counts = fdf["Release_Year"].value_counts().sort_index()
        fig = go.Figure(go.Bar(
            x=year_counts.index, y=year_counts.values,
            marker_color=ACCENT_RED, marker_line_width=0,
        ))
        fig.update_layout(
              **PLOTLY_TEMPLATE["layout"],
              height=320,
              xaxis_title=None,
              yaxis_title="Titles"
              )

    with c2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Genre mix</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-caption">Share of titles by primary genre</div>', unsafe_allow_html=True)
        genre_counts = fdf["Genre"].value_counts()
        fig = go.Figure(go.Pie(
            labels=genre_counts.index, values=genre_counts.values, hole=0.58,
            marker=dict(colors=SEQ_PALETTE, line=dict(color="#0B0D10", width=2)),
            textfont=dict(color="#F2F2F0"),
        ))
        fig.update_layout(**PLOTLY_TEMPLATE["layout"], height=320, showlegend=True)
        fig.update_layout(legend=dict(orientation="v", font=dict(size=10)))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">IMDb rating distribution</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-caption">How critically rated titles are spread</div>', unsafe_allow_html=True)
        fig = go.Figure(go.Histogram(
            x=fdf["IMDb_Rating"], nbinsx=20, marker_color=ACCENT_GOLD,
        ))
        fig.update_layout(**PLOTLY_TEMPLATE["layout"], height=300,
                           xaxis_title="IMDb rating", yaxis_title="Titles")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Runtime by genre</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-caption">Median runtime (minutes), top genres</div>', unsafe_allow_html=True)
        med_runtime = fdf.groupby("Genre")["Duration"].median().sort_values(ascending=True)
        fig = go.Figure(go.Bar(
            x=med_runtime.values, y=med_runtime.index, orientation="h",
            marker_color=ACCENT_RED,
        ))
        fig.update_layout(**PLOTLY_TEMPLATE["layout"], height=300,
                           xaxis_title="Minutes", yaxis_title=None)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

# ---- Tab 2: Box Office ----
with tab_money:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Budget vs. revenue</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-caption">Each point is a title with both figures reported</div>', unsafe_allow_html=True)
        money_df = fdf.dropna(subset=["Budget", "Revenue"])
        fig = go.Figure(go.Scatter(
            x=money_df["Budget"], y=money_df["Revenue"], mode="markers",
            marker=dict(color=ACCENT_RED, size=7, opacity=0.65,
                        line=dict(color="#0B0D10", width=0.5)),
            text=money_df["Title"], hovertemplate="%{text}<br>Budget: $%{x:,.0f}<br>Revenue: $%{y:,.0f}<extra></extra>",
        ))
        fig.update_layout(**PLOTLY_TEMPLATE["layout"], height=340,
                           xaxis_title="Budget ($)", yaxis_title="Revenue ($)")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Revenue by genre</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-caption">Total reported revenue, top genres</div>', unsafe_allow_html=True)
        rev_genre = fdf.groupby("Genre")["Revenue"].sum().sort_values(ascending=False).head(10)
        fig = go.Figure(go.Bar(
            x=rev_genre.index, y=rev_genre.values, marker_color=ACCENT_GOLD,
        ))
        fig.update_layout(**PLOTLY_TEMPLATE["layout"], height=340,
                           xaxis_title=None, yaxis_title="Revenue ($)")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Top 10 titles by votes</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-caption">Audience engagement leaders in the current filter</div>', unsafe_allow_html=True)
    top_votes = fdf.nlargest(10, "Votes")[["Title", "Votes", "IMDb_Rating"]].sort_values("Votes")
    fig = go.Figure(go.Bar(
        x=top_votes["Votes"], y=top_votes["Title"], orientation="h",
        marker_color=ACCENT_RED,
        text=top_votes["IMDb_Rating"].map(lambda v: f"IMDb {v:.1f}"),
        textposition="outside", textfont=dict(color="#A7ADB5"),
    ))
    fig.update_layout(**PLOTLY_TEMPLATE["layout"], height=380,
                       xaxis_title="Votes", yaxis_title=None)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# ---- Tab 3: Geography ----
with tab_geo:
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Titles by country</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-caption">Production country footprint</div>', unsafe_allow_html=True)
        country_counts = fdf["Country"].value_counts()
        fig = go.Figure(go.Choropleth(
            locations=country_counts.index, locationmode="country names",
            z=country_counts.values, colorscale=[[0, "#22262D"], [1, ACCENT_RED]],
            marker_line_color="#0B0D10", marker_line_width=0.5,
            colorbar=dict(title="Titles", tickfont=dict(color="#A7ADB5")),
        ))
        fig.update_geos(bgcolor="rgba(0,0,0,0)", showframe=False, showcoastlines=False,
                         landcolor="#15181D", oceancolor="#0B0D10", showocean=True)
        fig.update_layout(**PLOTLY_TEMPLATE["layout"], height=380, geo=dict(bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Language breakdown</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-caption">Titles by primary language</div>', unsafe_allow_html=True)
        lang_counts = fdf["Language"].value_counts()
        fig = go.Figure(go.Bar(
            x=lang_counts.values, y=lang_counts.index, orientation="h",
            marker_color=ACCENT_GOLD,
        ))
        fig.update_layout(**PLOTLY_TEMPLATE["layout"], height=380,
                           xaxis_title="Titles", yaxis_title=None)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

# ---- Tab 4: Explore Data ----
with tab_table:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Filtered dataset</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-caption">Every column post-cleaning &mdash; sort, scroll, or export below</div>', unsafe_allow_html=True)
    st.dataframe(
        fdf.reset_index(drop=True),
        use_container_width=True,
        height=460,
    )
    st.download_button(
        "⬇ Download filtered CSV",
        data=fdf.to_csv(index=False).encode("utf-8"),
        file_name="netflix_movies_filtered.csv",
        mime="text/csv",
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    '<div class="credit">CLEANED WITH PANDAS &middot; BUILT WITH STREAMLIT + PLOTLY</div>',
    unsafe_allow_html=True,
)