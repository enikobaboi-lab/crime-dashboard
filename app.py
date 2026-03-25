import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title='UK Crime Intelligence Dashboard',
    page_icon='🔍',
    layout='wide',
    initial_sidebar_state='expanded'
)

PRIMARY  = '#1e3a5f'
ACCENT   = '#2563eb'
SUCCESS  = '#16a34a'
WARNING  = '#d97706'
DANGER   = '#dc2626'
NEUTRAL  = '#6b7280'

REGION_COLORS = {
    'London (Met)':    '#2563eb',
    'Manchester':      '#dc2626',
    'West Midlands':   '#7c3aed',
    'West Yorkshire':  '#059669',
    'Thames Valley':   '#d97706',
    'Devon & Cornwall':'#0891b2',
}
POPULATION = {
    'London (Met)':    8_866_180,
    'Manchester':      2_867_800,
    'West Midlands':   2_947_600,
    'West Yorkshire':  2_361_600,
    'Thames Valley':   2_432_100,
    'Devon & Cornwall':1_785_500,
}

# ============================================================
# CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter','Segoe UI',sans-serif; }
.stApp { background-color: #f0f2f6; }

/* ── Sidebar ── */
[data-testid="stSidebar"] { background-color: #0f2035 !important; }
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0.5rem !important;
    padding-left: 0 !important; padding-right: 0 !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] .stMarkdown p { color: #ffffff !important; }

/* Multiselect */
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background-color: #162d4a !important;
    border: 1px solid #2d5a8e !important; border-radius: 8px !important;
}
[data-testid="stSidebar"] .stMultiSelect > div > div:focus-within {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.2) !important;
}
[data-testid="stSidebar"] .stMultiSelect input {
    color: #ffffff !important; caret-color: #60a5fa !important;
}
[data-testid="stSidebar"] .stMultiSelect input::placeholder { color: #475569 !important; }
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background-color: #1d4ed8 !important;
    border-radius: 20px !important; border: none !important;
    padding: 2px 8px !important; max-width: 140px !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] span {
    color: #ffffff !important; font-size: 0.71rem !important;
    font-weight: 600 !important; white-space: nowrap !important;
    overflow: hidden !important; text-overflow: ellipsis !important;
    max-width: 110px !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] svg {
    color: #ffffff !important; fill: #ffffff !important;
}

/* Dropdown options */
[data-baseweb="popover"] ul,
[data-baseweb="popover"] [data-baseweb="menu"] {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12) !important;
}
[data-baseweb="popover"] li,
[data-baseweb="popover"] [role="option"] {
    color: #1e3a5f !important; background-color: #ffffff !important;
    font-size: 0.82rem !important;
}
[data-baseweb="popover"] li:hover,
[data-baseweb="popover"] [aria-selected="true"] {
    background-color: #eff6ff !important; color: #1d4ed8 !important;
}

/* Sidebar buttons — bulletproof all states */
[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] .stButton > button:link,
[data-testid="stSidebar"] .stButton > button:visited,
[data-testid="stSidebar"] .stButton > button:focus,
[data-testid="stSidebar"] .stButton > button:focus-visible,
[data-testid="stSidebar"] .stButton button,
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"],
[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] {
    background-color: #1a3a5c !important;
    background: #1a3a5c !important;
    background-image: none !important;
    color: #ffffff !important;
    border: 1px solid #2d5a8e !important;
    border-radius: 8px !important;
    font-family: 'Inter','Segoe UI',sans-serif !important;
    font-weight: 600 !important; font-size: 0.74rem !important;
    width: 100% !important; padding: 0.45rem 0.5rem !important;
    line-height: 1.35 !important; box-shadow: none !important;
    outline: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover,
[data-testid="stSidebar"] .stButton button:hover,
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover,
[data-testid="stSidebar"] [data-testid="stBaseButton-primary"]:hover {
    background-color: #1e4a7a !important;
    background: #1e4a7a !important;
    border-color: #3b82f6 !important; color: #ffffff !important;
}
[data-testid="stSidebar"] .stButton > button:active,
[data-testid="stSidebar"] .stButton button:active {
    background-color: #1d4ed8 !important;
    background: #1d4ed8 !important; color: #ffffff !important;
}
[data-testid="stSidebar"] .stButton > button *,
[data-testid="stSidebar"] .stButton button *,
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] *,
[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] * {
    color: #ffffff !important; background: transparent !important;
}

/* Toggle */
[data-testid="stSidebar"] .stToggle label,
[data-testid="stSidebar"] .stToggle span,
[data-testid="stSidebar"] .stToggle p { color: #ffffff !important; }

/* Download button */
[data-testid="stSidebar"] .stDownloadButton > button {
    background-color: #0e4a2a !important; background: #0e4a2a !important;
    color: #ffffff !important; border: 1px solid #16a34a !important;
    border-radius: 8px !important; font-weight: 700 !important;
    width: 100% !important;
}
[data-testid="stSidebar"] .stDownloadButton > button:hover {
    background-color: #166534 !important; background: #166534 !important;
    color: #ffffff !important;
}
[data-testid="stSidebar"] .stDownloadButton > button * { color: #ffffff !important; }

[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.12) !important; margin: 0.6rem 0 !important; }

/* Sidebar helpers */
.sb-filter-hdr { display:flex; align-items:center; gap:7px; padding:0.6rem 1rem 0.25rem 1rem; }
.sb-filter-lbl { font-size:0.76rem; font-weight:700; color:#e2e8f0 !important; flex:1; }
.sb-filter-badge {
    background-color:#162d4a; color:#60a5fa !important;
    border:1px solid #2d5a8e; border-radius:20px;
    padding:1px 9px; font-size:0.62rem; font-weight:700;
}
.sb-count-box {
    background-color:#081526; border:1px solid #1a3a5c;
    border-radius:10px; padding:10px 13px; margin:0.4rem 1rem 0.6rem 1rem;
}
.sb-count-box .cbt { font-size:0.58rem; font-weight:700; text-transform:uppercase;
    letter-spacing:0.12em; color:#334155 !important; margin-bottom:6px; }
.sb-count-box .cbn { font-size:1.35rem; font-weight:800;
    color:#3b82f6 !important; display:block; margin-bottom:6px; }
.sb-count-box .cbr { font-size:0.7rem; color:#64748b !important; padding:1px 0; }
.sb-count-box .cbr b { color:#cbd5e1 !important; }

/* ── Main content ── */
.dash-header {
    background: linear-gradient(135deg,#0f2040 0%,#1e3a5f 45%,#1d4ed8 100%);
    padding: 2rem 2.5rem; border-radius: 20px; margin-bottom: 1.5rem;
    display: flex; align-items: center; justify-content: space-between;
    gap: 1rem; position: relative; overflow: hidden;
    box-shadow: 0 8px 32px rgba(30,58,95,0.28), 0 2px 8px rgba(0,0,0,0.12);
}
.dash-header::before {
    content:''; position:absolute; width:380px; height:380px;
    background:rgba(255,255,255,0.06); border-radius:50%;
    top:-160px; right:-60px; pointer-events:none;
}
.dash-header-text { position:relative; z-index:1; }
.dash-header-text h1 { color:#fff; font-size:1.85rem; font-weight:800; margin:0; line-height:1.2; letter-spacing:-0.02em; }
.dash-header-text p { color:rgba(255,255,255,0.65); margin:0.4rem 0 0; font-size:0.88rem; }
.dash-header-badge {
    background:rgba(255,255,255,0.15); backdrop-filter:blur(12px);
    border:1px solid rgba(255,255,255,0.25); color:#fff;
    padding:0.5rem 1.3rem; border-radius:50px;
    font-size:0.82rem; font-weight:600; white-space:nowrap;
    flex-shrink:0; position:relative; z-index:1;
}

/* Key Insights box */
.insights-box {
    background: linear-gradient(135deg, #0f2040 0%, #1e3a5f 100%);
    border-radius: 16px; padding: 1.4rem 1.8rem;
    margin-bottom: 1.4rem;
    box-shadow: 0 4px 20px rgba(30,58,95,0.2);
    border: 1px solid rgba(255,255,255,0.08);
}
.insights-box h3 {
    color: #ffffff; font-size: 0.78rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.12em;
    margin: 0 0 0.9rem 0; opacity: 0.7;
}
.insight-item {
    display: flex; gap: 10px; margin-bottom: 0.6rem;
    align-items: flex-start;
}
.insight-icon { font-size: 1rem; flex-shrink: 0; margin-top: 1px; }
.insight-text { font-size: 0.84rem; color: rgba(255,255,255,0.88); line-height: 1.5; }
.insight-text strong { color: #93c5fd; }

.kpi-card {
    background:#fff; border-radius:16px; padding:1.3rem 1.2rem 1rem;
    box-shadow:0 1px 3px rgba(0,0,0,0.06),0 4px 16px rgba(0,0,0,0.05);
    border-top:4px solid; height:100%;
    transition:transform .2s,box-shadow .2s; overflow:hidden;
}
.kpi-card:hover { transform:translateY(-4px); box-shadow:0 12px 32px rgba(0,0,0,0.1); }
.kpi-label { font-size:0.69rem; font-weight:700; text-transform:uppercase; letter-spacing:0.09em; color:#6b7280; margin-bottom:0.5rem; }
.kpi-value { font-size:2rem; font-weight:800; line-height:1.05; margin-bottom:0.3rem; letter-spacing:-0.02em; }
.kpi-sub { font-size:0.74rem; color:#9ca3af; }

.section-card {
    background:#fff; border-radius:16px; padding:1.5rem 1.6rem;
    box-shadow:0 1px 3px rgba(0,0,0,0.06),0 4px 16px rgba(0,0,0,0.05);
    border:1px solid rgba(0,0,0,0.04); margin-bottom:1.2rem;
}
.section-title {
    font-size:1.05rem; font-weight:700; color:#1e3a5f;
    margin-bottom:0.25rem; display:flex; align-items:center; gap:0.5rem;
}
.section-title::before {
    content:''; display:inline-block; width:4px; min-width:4px; height:1em;
    background:linear-gradient(180deg,#2563eb,#1e3a5f); border-radius:2px;
}
.section-subtitle { font-size:0.82rem; color:#6b7280; margin-bottom:1rem; line-height:1.5; padding-left:0.6rem; }
.insight-box {
    background:linear-gradient(135deg,#eff6ff,#dbeafe);
    border-left:4px solid #2563eb; border-radius:0 10px 10px 0;
    padding:0.9rem 1.1rem; margin-top:0.9rem;
    font-size:0.85rem; color:#1e40af; line-height:1.6;
}
.insight-box strong { color:#1e3a5f; }
.region-card {
    background:#fff; border-radius:14px; padding:1.2rem 1.1rem;
    box-shadow:0 1px 3px rgba(0,0,0,0.06),0 4px 12px rgba(0,0,0,0.05);
    border:1px solid rgba(0,0,0,0.04); border-top:4px solid;
    margin-bottom:1rem; transition:transform .2s,box-shadow .2s;
}
.region-card:hover { transform:translateY(-3px); box-shadow:0 8px 24px rgba(0,0,0,0.1); }
.region-card .rc-name { font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.07em; margin-bottom:0.4rem; }
.region-card .rc-count { font-size:1.9rem; font-weight:800; color:#1e3a5f; line-height:1; letter-spacing:-0.02em; }
.region-card .rc-sub { font-size:0.74rem; color:#9ca3af; margin-bottom:0.6rem; }
.region-card .rc-detail { font-size:0.8rem; color:#374151; line-height:1.75; background:#f9fafb; border-radius:8px; padding:0.6rem 0.75rem; margin-top:0.5rem; }

/* About section */
.about-card {
    background: #ffffff; border-radius: 16px; padding: 2rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.05);
    border: 1px solid rgba(0,0,0,0.04);
}
.about-section-title {
    font-size: 1.1rem; font-weight: 700; color: #1e3a5f;
    margin-bottom: 0.8rem; padding-bottom: 0.5rem;
    border-bottom: 2px solid #e5e7eb;
}
.about-row { display: flex; gap: 1rem; margin-bottom: 0.5rem; }
.about-label { font-size: 0.78rem; font-weight: 700; color: #6b7280; min-width: 120px; }
.about-val { font-size: 0.83rem; color: #374151; }
.tech-pill {
    display: inline-block; background: #eff6ff; color: #1d4ed8;
    border: 1px solid #bfdbfe; border-radius: 20px;
    padding: 3px 12px; font-size: 0.75rem; font-weight: 600;
    margin: 3px 4px 3px 0;
}

.stTabs [data-baseweb="tab-list"] {
    background:#fff; border-radius:14px; padding:0.35rem 0.4rem;
    gap:0.2rem; box-shadow:0 1px 4px rgba(0,0,0,0.07); margin-bottom:1.3rem;
}
.stTabs [data-baseweb="tab"] { border-radius:10px; padding:0.5rem 1.1rem; font-size:0.85rem; font-weight:500; color:#6b7280; }
.stTabs [data-baseweb="tab"]:hover { background:#f3f4f6; color:#1e3a5f; }
.stTabs [aria-selected="true"] {
    background:linear-gradient(135deg,#1e3a5f,#1d4ed8) !important;
    color:#fff !important; box-shadow:0 2px 10px rgba(30,58,95,0.35);
}
.empty-state { text-align:center; padding:4rem 2rem; color:#9ca3af; }
.empty-state h3 { color:#6b7280; margin-bottom:0.5rem; font-size:1.1rem; }
.dash-footer {
    text-align:center; color:#9ca3af; font-size:0.77rem;
    padding:1.5rem; border-top:1px solid #e5e7eb; margin-top:2rem; line-height:1.8;
}
.dash-footer a { color:#2563eb; text-decoration:none; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA LOADING
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_crime_data.csv.gz', compression='gzip')
    df['Month'] = pd.to_datetime(df['Month'])
    region_map = {
        'Metropolitan Police Service': 'London (Met)',
        'Greater Manchester Police':   'Manchester',
        'West Midlands Police':        'West Midlands',
        'West Yorkshire Police':       'West Yorkshire',
        'Thames Valley Police':        'Thames Valley',
        'Devon & Cornwall Police':     'Devon & Cornwall',
    }
    if 'Region' in df.columns:
        df['Region_Short'] = df['Region'].map(region_map).fillna(
            df.get('Region_Short', df['Region']))
    df['Region_Short'] = df['Region_Short'].fillna(df['Region'])
    if 'Outcome' in df.columns:
        df['Outcome'] = df['Outcome'].fillna('Unknown')
    return df

df = load_data()

# ============================================================
# PRE-COMPUTE
# ============================================================
all_regions = sorted(df['Region_Short'].dropna().unique())
all_crimes  = sorted(df['Crime_Type'].dropna().unique())
all_months  = df.sort_values('Month')['Month_Name'].unique().tolist()

region_counts = df['Region_Short'].value_counts().to_dict()
crime_counts  = df['Crime_Type'].value_counts().to_dict()
month_counts  = df['Month_Name'].value_counts().to_dict()

def fmt_count(n):
    if n >= 1_000_000: return f'{n/1_000_000:.1f}M'
    if n >= 1_000:     return f'{round(n/1_000)}k'
    return str(n)

r_opts = [f"{r} — {fmt_count(region_counts.get(r,0))}" for r in all_regions]
c_opts = [f"{c} — {fmt_count(crime_counts.get(c,0))}"  for c in all_crimes]
m_opts = [f"{m} — {fmt_count(month_counts.get(m,0))}"  for m in all_months]

r_map = {lbl: r for r, lbl in zip(all_regions, r_opts)}
c_map = {lbl: c for c, lbl in zip(all_crimes,  c_opts)}
m_map = {lbl: m for m, lbl in zip(all_months,  m_opts)}
r_inv = {r: lbl for lbl, r in r_map.items()}
c_inv = {c: lbl for lbl, c in c_map.items()}
m_inv = {m: lbl for lbl, m in m_map.items()}

rk_res = ['Offender given','Local resolution','charged','summonsed','Formal action']
res_by_region = {
    r: round(df[df['Region_Short']==r]['Outcome']
             .apply(lambda x: any(k.lower() in str(x).lower() for k in rk_res)).sum()
             / max(len(df[df['Region_Short']==r]),1)*100, 1)
    for r in all_regions
}
top3_regions     = df['Region_Short'].value_counts().head(3).index.tolist()
top3_crimes      = df['Crime_Type'].value_counts().head(3).index.tolist()
top3_res_regions = sorted(res_by_region, key=res_by_region.get, reverse=True)[:3]

monthly_total = df.groupby('Month').size().reset_index(name='Count').sort_values('Month')
monthly_total['Pct'] = monthly_total['Count'].pct_change() * 100
spike_month = None
if len(monthly_total) >= 2 and monthly_total.iloc[-1]['Pct'] > 5:
    spike_month = monthly_total.iloc[-1]['Month']


# ============================================================
# SESSION STATE
# ============================================================
if 'sel_regions' not in st.session_state: st.session_state.sel_regions = all_regions.copy()
if 'sel_crimes'  not in st.session_state: st.session_state.sel_crimes  = all_crimes.copy()
if 'sel_months'  not in st.session_state: st.session_state.sel_months  = all_months.copy()
if 'show_rate'   not in st.session_state: st.session_state.show_rate   = False


def _reset_widgets(*keys):
    for k in keys:
        if k in st.session_state:
            del st.session_state[k]

def _sync_r():
    labels = st.session_state.get('ms_r', [])
    st.session_state.sel_regions = [r_map[l] for l in labels if l in r_map]

def _sync_c():
    labels = st.session_state.get('ms_c', [])
    st.session_state.sel_crimes = [c_map[l] for l in labels if l in c_map]

def _sync_m():
    labels = st.session_state.get('ms_m', [])
    st.session_state.sel_months = [m_map[l] for l in labels if l in m_map]


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 1rem 0.2rem 1rem;">
      <div style="font-size:1.1rem;font-weight:800;color:#ffffff;letter-spacing:-0.01em;">
        🔍 Crime Dashboard</div>
      <div style="font-size:0.7rem;color:#475569;margin-top:3px;">
        UK Regional Overview · 2024–2025</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")

    # Quick Apply
    st.markdown('<div style="padding:0 1rem 0.3rem 1rem;font-size:0.6rem;font-weight:700;'
                'text-transform:uppercase;letter-spacing:0.13em;color:#64748b;">⚡ QUICK APPLY</div>',
                unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    with p1:
        if st.button("🏙️ Most Active\nRegions", key="pre_active", use_container_width=True,
                     help="Top 3 regions by crime volume"):
            st.session_state.sel_regions = top3_regions.copy()
            _reset_widgets('ms_r'); st.rerun()
        if st.button("📈 Trending\nCrimes", key="pre_trend", use_container_width=True,
                     help="Top 3 most reported crime types"):
            st.session_state.sel_crimes = top3_crimes.copy()
            _reset_widgets('ms_c'); st.rerun()
    with p2:
        if st.button("⚖️ Best Resolution\nRegions", key="pre_res", use_container_width=True,
                     help="Top 3 regions by resolution rate"):
            st.session_state.sel_regions = top3_res_regions.copy()
            _reset_widgets('ms_r'); st.rerun()
        if spike_month:
            sn = spike_month.strftime('%b %Y')
            if st.button(f"🚨 Crime Spike\n{sn}", key="pre_spike", use_container_width=True):
                st.session_state.sel_months = [spike_month.strftime('%B %Y')]
                _reset_widgets('ms_m'); st.rerun()
        else:
            if st.button("📅 Latest\n3 Months", key="pre_recent", use_container_width=True,
                         help="Most recent 3 months"):
                st.session_state.sel_months = all_months[-3:].copy()
                _reset_widgets('ms_m'); st.rerun()
    st.markdown("---")

    # Region
    n_r = len(st.session_state.sel_regions)
    st.markdown(f'<div class="sb-filter-hdr"><span style="font-size:0.9rem;">🗺️</span>'
                f'<span class="sb-filter-lbl">Region</span>'
                f'<span class="sb-filter-badge">{n_r}/{len(all_regions)}</span></div>',
                unsafe_allow_html=True)
    ra, rb = st.columns(2)
    with ra:
        if st.button("✓ Select All", key="r_all", use_container_width=True):
            st.session_state.sel_regions = all_regions.copy()
            _reset_widgets('ms_r'); st.rerun()
    with rb:
        if st.button("✕ Clear All", key="r_clr", use_container_width=True):
            st.session_state.sel_regions = []
            _reset_widgets('ms_r'); st.rerun()
    r_default = [r_inv[r] for r in st.session_state.sel_regions if r in r_inv]
    st.multiselect("Regions", options=r_opts, default=r_default,
                   label_visibility="collapsed", placeholder="Search regions…",
                   key="ms_r", on_change=_sync_r)
    st.markdown("---")

    # Crime Type
    n_c = len(st.session_state.sel_crimes)
    st.markdown(f'<div class="sb-filter-hdr"><span style="font-size:0.9rem;">🚨</span>'
                f'<span class="sb-filter-lbl">Crime Type</span>'
                f'<span class="sb-filter-badge" style="color:#a78bfa !important;">'
                f'{n_c}/{len(all_crimes)}</span></div>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca:
        if st.button("✓ Select All", key="c_all", use_container_width=True):
            st.session_state.sel_crimes = all_crimes.copy()
            _reset_widgets('ms_c'); st.rerun()
    with cb:
        if st.button("✕ Clear All", key="c_clr", use_container_width=True):
            st.session_state.sel_crimes = []
            _reset_widgets('ms_c'); st.rerun()
    c_default = [c_inv[c] for c in st.session_state.sel_crimes if c in c_inv]
    st.multiselect("Crime Types", options=c_opts, default=c_default,
                   label_visibility="collapsed", placeholder="Search crime types…",
                   key="ms_c", on_change=_sync_c)
    st.markdown("---")

    # Month
    n_m = len(st.session_state.sel_months)
    st.markdown(f'<div class="sb-filter-hdr"><span style="font-size:0.9rem;">📅</span>'
                f'<span class="sb-filter-lbl">Month</span>'
                f'<span class="sb-filter-badge" style="color:#22d3ee !important;">'
                f'{n_m}/{len(all_months)}</span></div>', unsafe_allow_html=True)
    ma, mb = st.columns(2)
    with ma:
        if st.button("✓ Select All", key="m_all", use_container_width=True):
            st.session_state.sel_months = all_months.copy()
            _reset_widgets('ms_m'); st.rerun()
    with mb:
        if st.button("✕ Clear All", key="m_clr", use_container_width=True):
            st.session_state.sel_months = []
            _reset_widgets('ms_m'); st.rerun()
    m_default = [m_inv[m] for m in st.session_state.sel_months if m in m_inv]
    st.multiselect("Months", options=m_opts, default=m_default,
                   label_visibility="collapsed", placeholder="Search months…",
                   key="ms_m", on_change=_sync_m)
    st.markdown("---")

    # Display mode
    st.markdown('<div style="padding:0 1rem 0.2rem 1rem;font-size:0.6rem;font-weight:700;'
                'text-transform:uppercase;letter-spacing:0.13em;color:#64748b;">📊 DISPLAY MODE</div>',
                unsafe_allow_html=True)
    st.toggle("Adjust for population size", value=st.session_state.show_rate,
              key="toggle_rate",
              help="Shows crimes per 100,000 residents for fair regional comparison")
    st.session_state.show_rate = st.session_state.toggle_rate
    st.markdown("---")

    # Summary
    _r = st.session_state.sel_regions or all_regions
    _c = st.session_state.sel_crimes  or all_crimes
    _m = st.session_state.sel_months  or all_months
    _n = len(df[df['Region_Short'].isin(_r) & df['Crime_Type'].isin(_c) & df['Month_Name'].isin(_m)])
    st.markdown(f"""
    <div class="sb-count-box">
        <div class="cbt">📋 Active Filters</div>
        <span class="cbn">{_n:,}</span>
        <div class="cbr">🗺️ &nbsp;<b>{len(_r)}</b> of {len(all_regions)} regions</div>
        <div class="cbr">🚨 &nbsp;<b>{len(_c)}</b> of {len(all_crimes)} crime types</div>
        <div class="cbr">📅 &nbsp;<b>{len(_m)}</b> of {len(all_months)} months</div>
    </div>""", unsafe_allow_html=True)

    # Reset
    if st.button("🔄  Reset All Filters", key="reset_all", use_container_width=True):
        st.session_state.sel_regions = all_regions.copy()
        st.session_state.sel_crimes  = all_crimes.copy()
        st.session_state.sel_months  = all_months.copy()
        st.session_state.show_rate   = False
        _reset_widgets('ms_r','ms_c','ms_m','toggle_rate'); st.rerun()

    # ── DOWNLOAD DATA BUTTON (enhancement #7) ────────────────
    st.markdown("---")
    st.markdown('<div style="padding:0 1rem 0.3rem 1rem;font-size:0.6rem;font-weight:700;'
                'text-transform:uppercase;letter-spacing:0.13em;color:#64748b;">⬇️ EXPORT</div>',
                unsafe_allow_html=True)

    @st.cache_data
    def to_csv(d): return d.to_csv(index=False).encode('utf-8')

    _preview_df = df[df['Region_Short'].isin(_r) & df['Crime_Type'].isin(_c) & df['Month_Name'].isin(_m)]
    st.download_button(
        label=f"Download Filtered Data ({len(_preview_df):,} rows)",
        data=to_csv(_preview_df),
        file_name='uk_crime_filtered.csv',
        mime='text/csv',
        use_container_width=True
    )
    st.markdown("""
    <div style="text-align:center;font-size:0.62rem;color:#334155;padding:8px 0 6px;line-height:1.7;">
        <a href="https://data.police.uk" style="color:#3b82f6;">data.police.uk</a>
        &nbsp;·&nbsp; Dec 2024 – May 2025
    </div>""", unsafe_allow_html=True)


# ============================================================
# FINAL SELECTIONS
# ============================================================
selected_regions = st.session_state.sel_regions or all_regions
selected_crimes  = st.session_state.sel_crimes  or all_crimes
selected_months  = st.session_state.sel_months  or all_months
show_rate        = st.session_state.show_rate

filtered = df[
    df['Region_Short'].isin(selected_regions) &
    df['Crime_Type'].isin(selected_crimes) &
    df['Month_Name'].isin(selected_months)
].copy()


# ============================================================
# HELPERS
# ============================================================
def style_chart(fig, height=360, legend=True):
    fig.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        font=dict(family='Inter, Segoe UI, sans-serif', color='#374151', size=11),
        margin=dict(l=16, r=80, t=20, b=16),
        height=height, hovermode='closest',
    )
    if legend:
        fig.update_layout(legend=dict(
            orientation='h', yanchor='bottom', y=-0.32,
            xanchor='center', x=0.5, font=dict(size=10),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(0,0,0,0.06)', borderwidth=1,
        ))
    else:
        fig.update_layout(showlegend=False)
    fig.update_xaxes(showgrid=False, tickfont=dict(size=10),
                     showline=True, linecolor='#e5e7eb', zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor='#f3f4f6', gridwidth=1,
                     tickfont=dict(size=10), zeroline=False)
    return fig

def no_data(msg="No data matches your current filters.",
            hint="Try widening your selections in the sidebar."):
    st.markdown(f'<div class="empty-state"><h3>{msg}</h3><p>{hint}</p></div>',
                unsafe_allow_html=True)

def sc(title, subtitle=None):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="section-subtitle">{subtitle}</div>', unsafe_allow_html=True)

def sc_end(): st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================
active_count = (
    (len(selected_regions) < len(all_regions)) +
    (len(selected_crimes)  < len(all_crimes))  +
    (len(selected_months)  < len(all_months))
)
badge_text = (f'📡 {active_count} Filter{"s" if active_count!=1 else ""} Active'
              if active_count else '📡 All Data Shown')

st.markdown(f"""
<div class="dash-header">
    <div class="dash-header-text">
        <h1>🔍 UK Regional Crime Dashboard</h1>
        <p>Interactive intelligence overview · England · December 2024 – May 2025 · Source: data.police.uk</p>
    </div>
    <div class="dash-header-badge">{badge_text}</div>
</div>""", unsafe_allow_html=True)


# ============================================================
# ENHANCEMENT #1 — KEY INSIGHTS NARRATIVE BOX
# ============================================================
def render_insights(df_f):
    if len(df_f) == 0:
        return
    total      = len(df_f)
    top_crime  = df_f['Crime_Type'].value_counts().idxmax()
    top_cnt    = df_f['Crime_Type'].value_counts().max()
    top_pct    = round(top_cnt / total * 100, 1)
    top_region = df_f['Region_Short'].value_counts().idxmax()
    top_r_cnt  = df_f['Region_Short'].value_counts().max()

    # Month-on-month change
    mc = (df_f.groupby(['Month','Region_Short']).size()
          .reset_index(name='Count').sort_values(['Region_Short','Month']))
    mc['Pct'] = mc.groupby('Region_Short')['Count'].pct_change() * 100
    latest = mc[mc['Month'] == mc['Month'].max()].dropna(subset=['Pct'])
    biggest_change = latest.loc[latest['Pct'].abs().idxmax()] if len(latest) > 0 else None

    # Resolution
    rk = ['Offender given','Local resolution','charged','summonsed','Formal action']
    resolved = df_f['Outcome'].apply(lambda x: any(k.lower() in str(x).lower() for k in rk)).sum()
    rr = round(resolved / total * 100, 1)

    # Build insight bullets
    items = [
        ("🔴", f"<strong>{top_crime}</strong> is the most reported crime type — "
               f"accounting for <strong>{top_pct}%</strong> ({top_cnt:,} incidents) "
               f"of all selected records."),
        ("📍", f"<strong>{top_region}</strong> recorded the highest number of crimes "
               f"with <strong>{top_r_cnt:,}</strong> reports in the selected period."),
        ("⚖️", f"The overall case resolution rate is <strong>{rr}%</strong> — "
               f"meaning {100-rr:.0f}% of cases were closed without a formal outcome."),
    ]
    if biggest_change is not None:
        direction = "increased" if biggest_change['Pct'] > 0 else "decreased"
        arrow     = "▲" if biggest_change['Pct'] > 0 else "▼"
        items.append((
            "📈",
            f"<strong>{biggest_change['Region_Short']}</strong> saw the largest month-on-month shift: "
            f"crime <strong>{direction} by {arrow}{abs(biggest_change['Pct']):.1f}%</strong> in the latest month."
        ))

    if show_rate:
        # Find lowest per-100k region
        rc = df_f.groupby('Region_Short').size().reset_index(name='Total')
        rc['Pop'] = rc['Region_Short'].map(POPULATION).fillna(1)
        rc['Rate'] = (rc['Total'] / rc['Pop'] * 100000).round(1)
        safest = rc.loc[rc['Rate'].idxmin()]
        items.append((
            "🏅",
            f"When adjusted for population, <strong>{safest['Region_Short']}</strong> has the "
            f"lowest crime rate at <strong>{safest['Rate']:,.1f} per 100,000 residents</strong>."
        ))

    bullets = ''.join(f'''
    <div class="insight-item">
        <span class="insight-icon">{icon}</span>
        <span class="insight-text">{text}</span>
    </div>''' for icon, text in items)

    st.markdown(f"""
    <div class="insights-box">
        <h3>🧠 Key Insights — auto-generated from current filters</h3>
        {bullets}
    </div>""", unsafe_allow_html=True)

render_insights(filtered)


# ============================================================
# KPI STRIP
# ============================================================
def render_kpi_strip(df_f):
    if len(df_f) == 0: return
    total      = len(df_f)
    top_crime  = df_f['Crime_Type'].value_counts().idxmax()
    top_region = df_f['Region_Short'].value_counts().idxmax()
    peak_month = df_f.groupby('Month_Name').size().idxmax()
    rk = ['Offender given','Local resolution','charged','summonsed','Formal action']
    resolved  = df_f['Outcome'].apply(lambda x: any(k.lower() in str(x).lower() for k in rk)).sum()
    res_rate  = round((resolved/total)*100, 1)

    k1,k2,k3,k4,k5 = st.columns(5)
    items = [
        (k1, ACCENT,   'Total Crimes Recorded', f'{total:,}',   f'Across {len(selected_months)} month(s)'),
        (k2, '#7c3aed','Most Common Crime',      top_crime,      'By number of reports'),
        (k3, DANGER,   'Highest Crime Region',   top_region,     'Most reports in period'),
        (k4, WARNING,  'Busiest Month',          peak_month,     'Highest single-month count'),
        (k5, SUCCESS,  'Resolution Rate',        f'{res_rate}%', 'Cases with a recorded outcome'),
    ]
    for col, color, label, value, sub in items:
        val_size = '1.5rem' if len(str(value)) > 12 else '2rem'
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="border-top-color:{color};
                 background:linear-gradient(145deg,#ffffff 60%,{color}0d 100%);">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value" style="color:{color};font-size:{val_size};">{value}</div>
                <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown('')

render_kpi_strip(filtered)


# ============================================================
# TABS  — 7 tabs now including Insights + About
# ============================================================
(tab_overview, tab_trends, tab_types,
 tab_regions, tab_map, tab_outcomes, tab_about) = st.tabs([
    '📊  Overview',
    '📈  Trends',
    '🔒  Crime Types',
    '🏙️  Regional View',
    '🗺️  Crime Map',
    '⚖️  Case Outcomes',
    'ℹ️  About',
])


# ──────────────────────────────────────────────────────────────
# TAB 1 — OVERVIEW
# ──────────────────────────────────────────────────────────────
with tab_overview:
    if len(filtered) == 0:
        no_data()
    else:
        # Month-on-month change badges
        mc = (filtered.groupby(['Month','Region_Short']).size()
              .reset_index(name='Count').sort_values(['Region_Short','Month']))
        mc['Pct_Change'] = (mc.groupby('Region_Short')['Count'].pct_change()*100).round(1)
        latest_mc = mc[mc['Month']==mc['Month'].max()].dropna(subset=['Pct_Change'])

        if len(latest_mc) > 0:
            st.markdown('<div class="section-title" style="margin-bottom:0.25rem;">'
                        'Latest Month — Change vs Previous Month</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-subtitle" style="padding-left:0.6rem;">'
                        'Did crime go up or down last month compared to the month before?</div>',
                        unsafe_allow_html=True)
            cols = st.columns(len(latest_mc))
            for i,(_, row) in enumerate(latest_mc.sort_values('Pct_Change',ascending=False).iterrows()):
                pct   = row['Pct_Change']
                arrow = '▲' if pct>0 else '▼' if pct<0 else '→'
                color = DANGER if pct>0 else SUCCESS if pct<0 else NEUTRAL
                lbl   = 'increase' if pct>0 else 'decrease' if pct<0 else 'no change'
                with cols[i]:
                    st.markdown(f"""
                    <div class="kpi-card" style="border-top-color:{color};text-align:center;
                         background:linear-gradient(145deg,#ffffff 60%,{color}0d 100%);">
                        <div class="kpi-label">{row['Region_Short']}</div>
                        <div class="kpi-value" style="color:{color};font-size:1.75rem;">
                            {arrow} {abs(pct):.1f}%</div>
                        <div class="kpi-sub">{lbl} from previous month</div>
                    </div>""", unsafe_allow_html=True)
            st.markdown('')

        col_l, col_r = st.columns(2)

        # Enhancement #6 — Top Crime Types in Selected Region
        with col_l:
            sc("Top 5 Most Reported Crimes",
               "The five crime types that appear most frequently in the selected data")
            top5 = filtered['Crime_Type'].value_counts().head(5).reset_index()
            top5.columns = ['Crime Type','Reports']
            fig_t5 = px.bar(top5, x='Reports', y='Crime Type', orientation='h',
                            color='Reports', color_continuous_scale=['#bfdbfe','#1d4ed8'],
                            text='Reports', labels={'Reports':'Number of Reports','Crime Type':''})
            fig_t5.update_traces(textposition='outside', textfont_size=11, texttemplate='%{text:,}')
            fig_t5 = style_chart(fig_t5, height=320, legend=False)
            fig_t5.update_layout(coloraxis_showscale=False, yaxis=dict(autorange='reversed'),
                                 xaxis=dict(range=[0, top5['Reports'].max()*1.3]))
            st.plotly_chart(fig_t5, use_container_width=True)
            sc_end()

        # Enhancement #4 — Regional Comparison bar chart
        with col_r:
            sc("Regional Comparison",
               "Total crimes per police force area — toggle population adjustment in sidebar")
            rc_ov = filtered.groupby('Region_Short').size().reset_index(name='Count')
            if show_rate:
                rc_ov['Pop']     = rc_ov['Region_Short'].map(POPULATION)
                rc_ov['Display'] = (rc_ov['Count']/rc_ov['Pop']*100000).round(1)
                rc_ov = rc_ov.sort_values('Display')
                x_c, x_l = 'Display','Crimes per 100,000 residents'
            else:
                rc_ov = rc_ov.sort_values('Count')
                x_c, x_l = 'Count','Total Crimes'
            fig_rv = px.bar(rc_ov, x=x_c, y='Region_Short', orientation='h',
                            color='Region_Short', color_discrete_map=REGION_COLORS,
                            text=x_c, labels={x_c:x_l,'Region_Short':''})
            fig_rv.update_traces(textposition='outside', textfont_size=11, texttemplate='%{text:,.0f}')
            fig_rv = style_chart(fig_rv, height=320, legend=False)
            fig_rv.update_layout(xaxis=dict(range=[0, rc_ov[x_c].max()*1.3]))
            st.plotly_chart(fig_rv, use_container_width=True)
            sc_end()

        top_r  = filtered['Region_Short'].value_counts().idxmax()
        top_rc = filtered['Region_Short'].value_counts().max()
        low_r  = filtered['Region_Short'].value_counts().idxmin()
        low_rc = filtered['Region_Short'].value_counts().min()
        top_c  = filtered['Crime_Type'].value_counts().idxmax()
        rk_s   = ['Offender given','Local resolution','charged','summonsed','Formal action']
        res_s  = filtered['Outcome'].apply(lambda x: any(k.lower() in str(x).lower() for k in rk_s)).sum()
        rr_s   = round((res_s/len(filtered))*100, 1)
        st.markdown(f"""<div class="insight-box">
            <strong>📌 Summary:</strong> <strong>{top_r}</strong> recorded the most crime
            ({top_rc:,} reports); <strong>{low_r}</strong> had the fewest ({low_rc:,}).
            Most common: <strong>{top_c}</strong>.
            Resolution rate: <strong>{rr_s}%</strong>.
        </div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# TAB 2 — TRENDS  (enhancement #3)
# ──────────────────────────────────────────────────────────────
with tab_trends:
    if len(filtered) == 0:
        no_data()
    else:
        monthly = filtered.groupby(['Month','Region_Short']).size().reset_index(name='Count')
        if show_rate:
            monthly['Pop']  = monthly['Region_Short'].map(POPULATION)
            monthly['Rate'] = (monthly['Count']/monthly['Pop']*100000).round(1)
            y_col, y_lbl = 'Rate','Crimes per 100,000 residents'
        else:
            y_col, y_lbl = 'Count','Number of Crimes'

        sc("Crime Trends Over Time",
           "Monthly crime counts for each region — hover any point for exact figures")
        fig_line = px.line(monthly, x='Month', y=y_col, color='Region_Short',
                           markers=True, color_discrete_map=REGION_COLORS,
                           labels={y_col:y_lbl,'Month':'','Region_Short':'Region'})
        fig_line.update_traces(line_width=2.5, marker_size=7)
        fig_line = style_chart(fig_line, height=400)
        fig_line.update_layout(hovermode='x unified')
        st.plotly_chart(fig_line, use_container_width=True)
        if show_rate:
            st.markdown('<div class="insight-box">💡 <strong>Why "per 100,000"?</strong> '
                        'Adjusting for population makes regions fairly comparable — '
                        'a larger city will naturally have more crime in absolute terms.</div>',
                        unsafe_allow_html=True)
        sc_end()

        sc("Month-on-Month Change (%)",
           "Bars above zero = more crime than the previous month · Below zero = less")
        mc2 = (filtered.groupby(['Month','Region_Short']).size()
               .reset_index(name='Count').sort_values(['Region_Short','Month']))
        mc2['Pct_Change'] = (mc2.groupby('Region_Short')['Count'].pct_change()*100).round(1)
        mc2 = mc2.dropna(subset=['Pct_Change'])
        if len(mc2) > 0:
            fig_mom = px.bar(mc2, x='Month', y='Pct_Change', color='Region_Short',
                             barmode='group', color_discrete_map=REGION_COLORS,
                             labels={'Pct_Change':'% Change vs Previous Month',
                                     'Month':'','Region_Short':'Region'})
            fig_mom.add_hline(y=0, line_color='#9ca3af', line_width=1.5,
                              line_dash='dot')
            fig_mom = style_chart(fig_mom, height=330)
            st.plotly_chart(fig_mom, use_container_width=True)
        sc_end()

        # Total crimes all regions combined monthly
        sc("Total Crime Volume — All Selected Regions Combined",
           "Aggregate monthly trend across all selected regions")
        total_monthly = filtered.groupby('Month').size().reset_index(name='Count')
        total_monthly['Month_Label'] = total_monthly['Month'].dt.strftime('%b %Y')
        fig_total = px.area(total_monthly, x='Month', y='Count',
                            labels={'Count':'Total Crimes','Month':''},
                            color_discrete_sequence=[ACCENT])
        fig_total.update_traces(fill='tozeroy', fillcolor='rgba(37,99,235,0.12)',
                                line_color=ACCENT, line_width=2.5)
        fig_total = style_chart(fig_total, height=260, legend=False)
        st.plotly_chart(fig_total, use_container_width=True)
        sc_end()


# ──────────────────────────────────────────────────────────────
# TAB 3 — CRIME TYPES  (enhancements #2 + #6)
# ──────────────────────────────────────────────────────────────
with tab_types:
    if len(filtered) == 0:
        no_data()
    else:
        col_l, col_r = st.columns([3,2])
        with col_l:
            sc("All Crime Types — Ranked by Volume",
               "Every recorded crime category, most to least common")
            tc = filtered['Crime_Type'].value_counts().reset_index()
            tc.columns = ['Crime Type','Count']
            fig_bar = px.bar(tc, x='Count', y='Crime Type', orientation='h',
                             color='Count', color_continuous_scale=['#dbeafe','#1d4ed8'],
                             text='Count', labels={'Count':'Number of Reports','Crime Type':''})
            fig_bar.update_traces(textposition='outside', textfont_size=10,
                                  texttemplate='%{text:,}')
            fig_bar = style_chart(fig_bar, height=420, legend=False)
            fig_bar.update_layout(coloraxis_showscale=False, yaxis=dict(autorange='reversed'),
                                  xaxis=dict(range=[0, tc['Count'].max()*1.3]))
            st.plotly_chart(fig_bar, use_container_width=True)
            sc_end()

        with col_r:
            # Enhancement #2 — Treemap crime type breakdown
            sc("Crime Type Breakdown",
               "Treemap showing proportional share of each crime category")
            fig_tree = px.treemap(
                tc, path=['Crime Type'], values='Count',
                color='Count', color_continuous_scale=['#dbeafe','#1e3a5f'],
                hover_data={'Count':':,'}
            )
            fig_tree.update_traces(textinfo='label+percent root',
                                   textfont_size=12)
            fig_tree.update_layout(
                paper_bgcolor='white', margin=dict(l=5,r=5,t=5,b=5),
                height=260, coloraxis_showscale=False,
                font=dict(family='Inter,Segoe UI,sans-serif'))
            st.plotly_chart(fig_tree, use_container_width=True)
            sc_end()

            sc("Share of All Reports",
               "Percentage breakdown of crime categories")
            top_n = tc.head(6).copy()
            if len(tc) > 6:
                top_n = pd.concat([
                    top_n,
                    pd.DataFrame({'Crime Type':['All Others'],
                                  'Count':[tc.iloc[6:]['Count'].sum()]})
                ], ignore_index=True)
            fig_pie = px.pie(top_n, values='Count', names='Crime Type',
                             color_discrete_sequence=[
                                 '#1e3a5f','#1d4ed8','#2563eb','#3b82f6',
                                 '#60a5fa','#93c5fd','#bfdbfe'],
                             hole=0.45)
            fig_pie.update_traces(textposition='inside', textinfo='percent', textfont_size=11)
            fig_pie.update_layout(paper_bgcolor='white',
                                  font=dict(family='Inter,Segoe UI,sans-serif',
                                            color='#374151',size=10),
                                  margin=dict(l=10,r=10,t=10,b=10), height=260,
                                  legend=dict(font=dict(size=9),y=-0.25,
                                              orientation='h',xanchor='center',x=0.5))
            st.plotly_chart(fig_pie, use_container_width=True)
            sc_end()

        # Enhancement #6 — Top 5 per region
        st.markdown('')
        sc("Top 5 Crime Types per Region",
           "Comparing the most common crimes across each selected police force area")
        top5_region = []
        for reg in filtered['Region_Short'].unique():
            rdf = filtered[filtered['Region_Short']==reg]
            top5r = rdf['Crime_Type'].value_counts().head(5).reset_index()
            top5r.columns = ['Crime Type','Count']
            top5r['Region'] = reg
            top5_region.append(top5r)
        if top5_region:
            top5_all = pd.concat(top5_region, ignore_index=True)
            fig_t5r = px.bar(top5_all, x='Count', y='Crime Type', color='Region',
                             facet_col='Region', facet_col_wrap=3, orientation='h',
                             color_discrete_map=REGION_COLORS,
                             labels={'Count':'Reports','Crime Type':''},
                             height=420)
            fig_t5r.update_layout(paper_bgcolor='white', plot_bgcolor='white',
                                  font=dict(family='Inter,Segoe UI,sans-serif',
                                            color='#374151',size=10),
                                  margin=dict(l=10,r=10,t=40,b=10),
                                  showlegend=False)
            fig_t5r.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
            fig_t5r.update_yaxes(matches=None, showticklabels=True)
            st.plotly_chart(fig_t5r, use_container_width=True)
        sc_end()


# ──────────────────────────────────────────────────────────────
# TAB 4 — REGIONAL VIEW
# ──────────────────────────────────────────────────────────────
with tab_regions:
    if len(filtered) == 0:
        no_data()
    else:
        rc_df = filtered.groupby('Region_Short').size().reset_index(name='Total')
        rc_df['Population'] = rc_df['Region_Short'].map(POPULATION).fillna(0)
        rc_df['Per100k'] = (rc_df['Total']/rc_df['Population'].replace(0,1)*100000).round(1)
        rc_df['Top Crime'] = rc_df['Region_Short'].apply(
            lambda r: filtered[filtered['Region_Short']==r]['Crime_Type']
            .value_counts().idxmax()
            if len(filtered[filtered['Region_Short']==r])>0 else 'N/A')
        rk_r = ['Offender given','Local resolution','charged','summonsed','Formal action']
        rc_df['Res Rate'] = rc_df['Region_Short'].apply(
            lambda r: round(filtered[filtered['Region_Short']==r]['Outcome']
                .apply(lambda x: any(k.lower() in str(x).lower() for k in rk_r)).sum()
                /max(len(filtered[filtered['Region_Short']==r]),1)*100, 1))

        st.markdown('<div class="section-title" style="margin-bottom:0.25rem;">'
                    'Region-by-Region Snapshot</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle" style="margin-bottom:1rem;padding-left:0.6rem;">'
                    'Key figures for each police force area in the selected period</div>',
                    unsafe_allow_html=True)
        cols = st.columns(3)
        for i,(_, row) in enumerate(rc_df.sort_values('Total',ascending=False).iterrows()):
            region = row['Region_Short']
            color  = REGION_COLORS.get(region, ACCENT)
            with cols[i%3]:
                st.markdown(f"""
                <div class="region-card" style="border-top-color:{color};">
                    <div class="rc-name" style="color:{color};">{region}</div>
                    <div class="rc-count">{row['Total']:,}</div>
                    <div class="rc-sub">crimes recorded</div>
                    <div class="rc-detail">
                        📊 {row['Per100k']:,.1f} per 100k residents<br>
                        🔒 Most common: <strong>{row['Top Crime']}</strong><br>
                        ⚖️ Resolution rate: <strong>{row['Res Rate']}%</strong>
                    </div>
                </div>""", unsafe_allow_html=True)

        st.markdown('')
        sc("Side-by-Side Comparison")
        if show_rate:
            rc_s = rc_df.sort_values('Per100k',ascending=False)
            x_c, x_l = 'Per100k','Crimes per 100,000 residents'
        else:
            rc_s = rc_df.sort_values('Total',ascending=False)
            x_c, x_l = 'Total','Total Crimes Recorded'
        fig_cmp = px.bar(rc_s, x='Region_Short', y=x_c,
                         color='Region_Short', color_discrete_map=REGION_COLORS,
                         text=x_c, labels={'Region_Short':'',x_c:x_l})
        fig_cmp.update_traces(textposition='outside', textfont_size=12,
                              texttemplate='%{text:,.0f}')
        fig_cmp = style_chart(fig_cmp, height=360, legend=False)
        fig_cmp.update_layout(yaxis=dict(range=[0, rc_s[x_c].max()*1.2]))
        st.plotly_chart(fig_cmp, use_container_width=True)
        if show_rate:
            hr_r = rc_df.loc[rc_df['Per100k'].idxmax()]
            lr_r = rc_df.loc[rc_df['Per100k'].idxmin()]
            st.markdown(f"""<div class="insight-box">
                <strong>📌 Population-adjusted:</strong>
                <strong>{hr_r['Region_Short']}</strong> has the highest rate
                ({hr_r['Per100k']:,.1f} per 100k),
                <strong>{lr_r['Region_Short']}</strong> the lowest ({lr_r['Per100k']:,.1f}).
            </div>""", unsafe_allow_html=True)
        sc_end()

        sc("Crime Mix by Region",
           "Stacked bar shows the breakdown of crime types per police force area")
        top6_ct = filtered['Crime_Type'].value_counts().head(6).index.tolist()
        reg_type = filtered.copy()
        reg_type['Crime_Type_Group'] = reg_type['Crime_Type'].apply(
            lambda x: x if x in top6_ct else 'Other')
        rt = reg_type.groupby(['Region_Short','Crime_Type_Group']).size().reset_index(name='Count')
        fig_stk = px.bar(rt, x='Region_Short', y='Count', color='Crime_Type_Group',
                         barmode='stack',
                         color_discrete_sequence=[
                             '#1e3a5f','#1d4ed8','#2563eb','#3b82f6','#60a5fa','#93c5fd','#bfdbfe'],
                         labels={'Region_Short':'','Count':'Number of Crimes',
                                 'Crime_Type_Group':'Crime Type'})
        fig_stk = style_chart(fig_stk, height=360)
        st.plotly_chart(fig_stk, use_container_width=True)
        sc_end()


# ──────────────────────────────────────────────────────────────
# TAB 5 — CRIME MAP
# ──────────────────────────────────────────────────────────────
with tab_map:
    if len(filtered) == 0:
        no_data()
    else:
        sc("Crime Locations Across England",
           "Each dot marks a reported crime location. Hover for details.")
        md = filtered.dropna(subset=['Lat','Long']).copy()
        if len(md) == 0:
            no_data("No location data for this selection.")
        else:
            sample_n = min(8000, len(md))
            ms = md.sample(n=sample_n, random_state=42) if len(md)>sample_n else md
            fig_map = px.scatter_mapbox(ms, lat='Lat', lon='Long', color='Crime_Type',
                                        hover_name='Crime_Type',
                                        hover_data={'Region_Short':True,'Month_Name':True,
                                                    'Lat':False,'Long':False},
                                        zoom=5.5, center={'lat':52.5,'lon':-1.5},
                                        height=590, opacity=0.55)
            fig_map.update_layout(mapbox_style='open-street-map', paper_bgcolor='white',
                                  font=dict(family='Inter,Segoe UI,sans-serif',color='#374151'),
                                  margin=dict(l=0,r=0,t=0,b=0),
                                  legend=dict(orientation='h',yanchor='top',y=-0.02,
                                              xanchor='center',x=0.5,font=dict(size=9)))
            st.plotly_chart(fig_map, use_container_width=True)
            if len(md) > sample_n:
                st.markdown(f'<div class="insight-box">📍 Showing {sample_n:,} of '
                            f'{len(md):,} locations for performance. Filter by region '
                            f'for full detail.</div>', unsafe_allow_html=True)
        sc_end()


# ──────────────────────────────────────────────────────────────
# TAB 6 — CASE OUTCOMES  (enhancement #5)
# ──────────────────────────────────────────────────────────────
with tab_outcomes:
    if len(filtered)==0 or 'Outcome' not in filtered.columns:
        no_data("No outcome data available for this selection.")
    else:
        rk_o = ['Offender given','Local resolution','charged','summonsed','Formal action']
        resolved_o = filtered['Outcome'].apply(
            lambda x: any(k.lower() in str(x).lower() for k in rk_o)).sum()
        rr_o = round((resolved_o/len(filtered))*100, 1)

        col_l, col_r = st.columns([3,2])
        with col_l:
            sc("What Happened to Reported Cases?",
               "All outcome categories recorded by police — from prosecution to no further action")
            oc = filtered['Outcome'].value_counts().head(10).reset_index()
            oc.columns = ['Outcome','Count']
            oc['Outcome_Short'] = oc['Outcome'].apply(
                lambda x: x[:52]+'…' if len(str(x))>52 else x)
            fig_out = px.bar(oc, x='Count', y='Outcome_Short', orientation='h',
                             color='Count', color_continuous_scale=['#dbeafe','#1d4ed8'],
                             text='Count', labels={'Count':'Number of Cases','Outcome_Short':''})
            fig_out.update_traces(textposition='outside', textfont_size=10,
                                  texttemplate='%{text:,}')
            fig_out = style_chart(fig_out, height=400, legend=False)
            fig_out.update_layout(coloraxis_showscale=False,
                                  yaxis=dict(autorange='reversed'),
                                  xaxis=dict(range=[0, oc['Count'].max()*1.3]))
            st.plotly_chart(fig_out, use_container_width=True)
            sc_end()

            # Enhancement #5 — Outcome category donut
            sc("Outcome Categories — Resolved vs Unresolved",
               "High-level split between cases with a positive outcome and those without")
            resolved_cnt   = resolved_o
            unresolved_cnt = len(filtered) - resolved_o
            pie_data = pd.DataFrame({
                'Category': ['Resolved (Charge / Caution / Resolution)',
                             'Unresolved / Under Investigation'],
                'Count':    [resolved_cnt, unresolved_cnt]
            })
            fig_donut = px.pie(pie_data, values='Count', names='Category',
                               color_discrete_sequence=[SUCCESS, '#e5e7eb'],
                               hole=0.55)
            fig_donut.update_traces(textposition='inside', textinfo='percent+label',
                                    textfont_size=11)
            fig_donut.update_layout(paper_bgcolor='white',
                                    font=dict(family='Inter,Segoe UI,sans-serif',
                                              color='#374151',size=10),
                                    margin=dict(l=10,r=10,t=10,b=10), height=280,
                                    showlegend=False)
            st.plotly_chart(fig_donut, use_container_width=True)
            sc_end()

        with col_r:
            sc("Overall Resolution Rate",
               "Proportion of crimes resulting in a positive justice outcome")
            fig_g = go.Figure(go.Indicator(
                mode='gauge+number', value=rr_o,
                number={'suffix':'%','font':{'size':48,'color':PRIMARY}},
                gauge={
                    'axis':{'range':[0,100],'tickcolor':'#9ca3af','tickwidth':1},
                    'bar':{'color':ACCENT,'thickness':0.28},
                    'bgcolor':'#f9fafb','borderwidth':0,
                    'steps':[
                        {'range':[0,25],'color':'#fee2e2'},
                        {'range':[25,50],'color':'#fef9c3'},
                        {'range':[50,75],'color':'#dcfce7'},
                        {'range':[75,100],'color':'#bbf7d0'},
                    ],
                    'threshold':{'line':{'color':DANGER,'width':3},
                                 'thickness':0.75,'value':rr_o}
                }
            ))
            fig_g.update_layout(paper_bgcolor='white',
                                font=dict(family='Inter,Segoe UI,sans-serif'),
                                height=260, margin=dict(l=20,r=20,t=20,b=20))
            st.plotly_chart(fig_g, use_container_width=True)
            st.markdown(f"""<div class="insight-box">
                <strong>What does this mean?</strong><br>
                Of <strong>{len(filtered):,}</strong> reported crimes,
                <strong>{resolved_o:,}</strong> ({rr_o}%) resulted in a charge,
                caution, or local resolution. The remaining
                <strong>{100-rr_o:.1f}%</strong> were closed without action
                or remain under investigation.
            </div>""", unsafe_allow_html=True)
            sc_end()

            sc("Resolution Rate by Region",
               "Which areas have the highest proportion of resolved cases?")
            reg_res = []
            for region in filtered['Region_Short'].unique():
                r_df  = filtered[filtered['Region_Short']==region]
                r_res = r_df['Outcome'].apply(
                    lambda x: any(k.lower() in str(x).lower() for k in rk_o)).sum()
                reg_res.append({'Region':region,'Rate':round((r_res/len(r_df))*100,1)})
            reg_res_df = pd.DataFrame(reg_res).sort_values('Rate',ascending=True)
            fig_rr = px.bar(reg_res_df, x='Rate', y='Region', orientation='h',
                            color='Region', color_discrete_map=REGION_COLORS,
                            text='Rate', labels={'Rate':'Resolution Rate (%)','Region':''})
            fig_rr.update_traces(textposition='outside', textfont_size=11,
                                 texttemplate='%{text:.1f}%')
            fig_rr = style_chart(fig_rr, height=240, legend=False)
            fig_rr.update_layout(xaxis=dict(range=[0, reg_res_df['Rate'].max()*1.4]))
            st.plotly_chart(fig_rr, use_container_width=True)
            sc_end()


# ──────────────────────────────────────────────────────────────
# TAB 7 — ABOUT  (enhancement #8)
# ──────────────────────────────────────────────────────────────
with tab_about:
    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown("""
        <div class="about-card">
          <div class="about-section-title">📖 About This Dashboard</div>
          <p style="font-size:0.88rem;color:#374151;line-height:1.75;margin-bottom:1.2rem;">
            This interactive dashboard was built to provide an analytical overview of
            reported crime across six English police force regions. It enables users to
            explore patterns, compare regions, and understand crime trends over a
            six-month window using open data published by UK police forces.
          </p>

          <div class="about-section-title">🗄️ Data Source</div>
          <div class="about-row">
            <span class="about-label">Source</span>
            <span class="about-val"><a href="https://data.police.uk" target="_blank"
              style="color:#2563eb;">data.police.uk</a> — Official UK Police Open Data</span>
          </div>
          <div class="about-row">
            <span class="about-label">Time Period</span>
            <span class="about-val">December 2024 – May 2025 (6 months)</span>
          </div>
          <div class="about-row">
            <span class="about-label">Regions Covered</span>
            <span class="about-val">London (Met) · Manchester · West Midlands ·
              West Yorkshire · Thames Valley · Devon & Cornwall</span>
          </div>
          <div class="about-row">
            <span class="about-label">Records</span>
            <span class="about-val">Over 1 million reported crime incidents</span>
          </div>
          <div class="about-row" style="margin-bottom:1.2rem;">
            <span class="about-label">Population Data</span>
            <span class="about-val">ONS 2023 mid-year estimates (used for per-100k calculations)</span>
          </div>

          <div class="about-section-title">🎯 Purpose</div>
          <p style="font-size:0.88rem;color:#374151;line-height:1.75;margin-bottom:1.2rem;">
            This dashboard was developed as part of a data analytics student project to
            demonstrate skills in data collection, cleaning, exploratory analysis,
            and interactive visualisation. It is intended for educational purposes only.
          </p>

          <div class="about-section-title">⚙️ Technologies Used</div>
          <div style="margin-top:0.5rem;">
            <span class="tech-pill">🐍 Python 3.12</span>
            <span class="tech-pill">📊 Streamlit</span>
            <span class="tech-pill">📈 Plotly</span>
            <span class="tech-pill">🐼 Pandas</span>
            <span class="tech-pill">🗺️ OpenStreetMap</span>
            <span class="tech-pill">☁️ Streamlit Cloud</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="about-card">
          <div class="about-section-title">📊 Dashboard Features</div>
          <ul style="font-size:0.85rem;color:#374151;line-height:2;padding-left:1.2rem;margin-bottom:1.2rem;">
            <li>🧠 Auto-generated Key Insights narrative</li>
            <li>📊 5 KPI metric cards</li>
            <li>📈 Interactive trends over time</li>
            <li>🗺️ Crime location map (up to 8,000 points)</li>
            <li>🔒 Crime type treemap + donut chart</li>
            <li>🏙️ Regional comparison with population adjustment</li>
            <li>⚖️ Case outcomes and resolution rate gauge</li>
            <li>⬇️ Filtered data export (CSV)</li>
            <li>⚡ Smart filter presets</li>
          </ul>

          <div class="about-section-title">⚠️ Limitations</div>
          <ul style="font-size:0.85rem;color:#374151;line-height:2;padding-left:1.2rem;margin-bottom:1.2rem;">
            <li>Data covers only 6 selected police forces</li>
            <li>Location coordinates are approximate (street-level)</li>
            <li>Outcome data may lag — some cases ongoing</li>
            <li>Resolution rate is an estimate based on keyword matching</li>
          </ul>

          <div class="about-section-title">📬 Data Licence</div>
          <p style="font-size:0.83rem;color:#374151;line-height:1.65;">
            Data provided under the
            <a href="https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/"
               target="_blank" style="color:#2563eb;">Open Government Licence v3.0</a>.
            Contains public sector information licensed by the Home Office.
          </p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="dash-footer">
    🔍 UK Regional Crime Dashboard &nbsp;·&nbsp;
    Data: <a href="https://data.police.uk">data.police.uk</a> &nbsp;·&nbsp;
    December 2024 – May 2025 &nbsp;·&nbsp;
    Built with Python · Streamlit · Plotly &nbsp;·&nbsp;
    Population: ONS 2023 &nbsp;·&nbsp;
    For educational purposes only
</div>
""", unsafe_allow_html=True)
