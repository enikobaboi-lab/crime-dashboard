import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

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
# GLOBAL CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter','Segoe UI',sans-serif; }
.stApp { background-color: #f0f2f6; }

/* ═══════════════════════════════════════════════════════════
   SIDEBAR — solid, zero-transparency, every element explicit
   ═══════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background-color: #0f2035 !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
[data-testid="stSidebar"] .block-container  { padding: 0 !important; }
[data-testid="stSidebar"] .element-container,
[data-testid="stSidebar"] .stMarkdown {
    margin: 0 !important; padding: 0 !important;
}

/* ── Sidebar Streamlit multiselects (hidden — we use custom UI) ── */
[data-testid="stSidebar"] .stMultiSelect,
[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] .stButton,
[data-testid="stSidebar"] .stToggle,
[data-testid="stSidebar"] .stDownloadButton { display: none !important; }

/* ── Custom sidebar shell ── */
.sb-shell {
    background-color: #0f2035;
    min-height: 100vh;
    font-family: 'Inter','Segoe UI',sans-serif;
    font-size: 13px;
    color: #f1f5f9;
    padding: 0;
}

/* ── Header band ── */
.sb-header {
    background-color: #081526;
    padding: 20px 18px 16px;
    border-bottom: 1px solid #1a3a5c;
}
.sb-header-title {
    font-size: 1.1rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.01em;
    line-height: 1.2;
    margin: 0;
}
.sb-header-sub {
    font-size: 0.69rem;
    color: #64748b;
    margin-top: 4px;
}

/* ── Section wrapper ── */
.sb-section {
    padding: 14px 18px;
    border-bottom: 1px solid #1a3a5c;
}

/* ── Section heading ── */
.sb-sec-hdr {
    font-size: 0.6rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #475569;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* ── Preset grid ── */
.sb-preset-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
}
.sb-preset-btn {
    display: block;
    background-color: #1a3a5c;
    color: #e2e8f0 !important;
    border: 1px solid #2d5a8a;
    border-radius: 8px;
    padding: 9px 8px;
    font-family: 'Inter','Segoe UI',sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    cursor: pointer;
    text-align: center;
    line-height: 1.35;
    width: 100%;
    text-decoration: none;
    transition: background-color 0.12s, border-color 0.12s;
}
.sb-preset-btn:hover {
    background-color: #1e4a7a;
    border-color: #3b82f6;
    color: #ffffff !important;
}
.sb-preset-btn small {
    display: block;
    font-size: 0.62rem;
    color: #60a5fa;
    font-weight: 400;
    margin-top: 2px;
}

/* ── Filter block ── */
.sb-filter-hdr {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 9px;
}
.sb-filter-icon { font-size: 0.9rem; flex-shrink: 0; }
.sb-filter-label {
    font-size: 0.75rem;
    font-weight: 700;
    color: #e2e8f0 !important;
    flex: 1;
    letter-spacing: 0.01em;
}
.sb-badge {
    background-color: #1a3a5c;
    color: #60a5fa !important;
    border: 1px solid #2d5a8a;
    border-radius: 20px;
    padding: 2px 9px;
    font-size: 0.61rem;
    font-weight: 700;
    white-space: nowrap;
    flex-shrink: 0;
}

/* ── Pill chips ── */
.sb-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-bottom: 9px;
    min-height: 4px;
}
.sb-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.67rem;
    font-weight: 600;
    color: #ffffff !important;
    white-space: nowrap;
    cursor: default;
}
.sb-chip-r  { background-color: #1d4ed8; border: 1px solid #3b82f6; }
.sb-chip-c  { background-color: #6d28d9; border: 1px solid #a78bfa; }
.sb-chip-m  { background-color: #0e7490; border: 1px solid #22d3ee; }
.sb-chip-x  { background-color: #1e293b; border: 1px solid #334155; color: #94a3b8 !important; }

/* ── Action buttons (Select All / Clear All) ── */
.sb-action-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
    margin-bottom: 8px;
}
.sb-act-btn {
    background-color: #1a3a5c;
    color: #e2e8f0 !important;
    border: 1px solid #2d5a8a;
    border-radius: 7px;
    padding: 6px 8px;
    font-family: 'Inter','Segoe UI',sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    cursor: pointer;
    text-align: center;
    width: 100%;
    transition: background-color 0.12s;
    text-decoration: none;
    display: block;
}
.sb-act-btn:hover {
    background-color: #1e4a7a;
    color: #ffffff !important;
    border-color: #3b82f6;
}
.sb-act-btn.clr {
    background-color: #2d1414;
    border-color: #7f1d1d;
    color: #fca5a5 !important;
}
.sb-act-btn.clr:hover {
    background-color: #7f1d1d;
    color: #ffffff !important;
    border-color: #ef4444;
}

/* ── Search input ── */
.sb-search-wrap { position: relative; margin-bottom: 7px; }
.sb-search-wrap input {
    width: 100%;
    background-color: #132030;
    border: 1px solid #2d5a8a;
    border-radius: 8px;
    padding: 7px 10px 7px 30px;
    color: #f1f5f9 !important;
    font-family: 'Inter','Segoe UI',sans-serif;
    font-size: 0.73rem;
    outline: none;
    caret-color: #60a5fa;
    transition: border-color 0.13s, background-color 0.13s;
}
.sb-search-wrap input::placeholder { color: #475569; }
.sb-search-wrap input:focus {
    border-color: #3b82f6;
    background-color: #1a3a5c;
    color: #ffffff !important;
}
.sb-search-icon {
    position: absolute;
    left: 9px; top: 50%;
    transform: translateY(-50%);
    font-size: 0.72rem;
    color: #475569;
    pointer-events: none;
}

/* ── Expand/collapse toggle ── */
.sb-expand-btn {
    background: none;
    border: none;
    font-family: 'Inter','Segoe UI',sans-serif;
    font-size: 0.68rem;
    font-weight: 600;
    color: #3b82f6 !important;
    cursor: pointer;
    padding: 2px 0 5px;
    display: block;
    width: 100%;
    text-align: left;
}
.sb-expand-btn:hover { color: #60a5fa !important; }

/* ── Options list ── */
.sb-opts {
    display: none;
    max-height: 200px;
    overflow-y: auto;
    margin-top: 2px;
}
.sb-opts.open { display: block; }
.sb-opts::-webkit-scrollbar { width: 3px; }
.sb-opts::-webkit-scrollbar-track { background: #0f2035; }
.sb-opts::-webkit-scrollbar-thumb { background: #2d5a8a; border-radius: 3px; }
.sb-opt {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 6px 4px;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.1s;
}
.sb-opt:hover { background-color: #1a3a5c; }
.sb-opt input[type=checkbox] {
    width: 14px; height: 14px;
    accent-color: #3b82f6;
    flex-shrink: 0;
    cursor: pointer;
    margin: 0;
}
.sb-opt-name {
    font-size: 0.76rem;
    color: #cbd5e1 !important;
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.sb-opt-cnt {
    font-size: 0.62rem;
    color: #475569 !important;
    white-space: nowrap;
    flex-shrink: 0;
}

/* ── Population toggle ── */
.sb-toggle-row {
    display: flex;
    align-items: center;
    gap: 12px;
    background-color: #132030;
    border: 1px solid #2d5a8a;
    border-radius: 9px;
    padding: 10px 12px;
    cursor: pointer;
    transition: background-color 0.13s;
}
.sb-toggle-row:hover { background-color: #1a3a5c; }
.sb-toggle-main {
    font-size: 0.76rem;
    font-weight: 600;
    color: #e2e8f0 !important;
    display: block;
}
.sb-toggle-hint {
    font-size: 0.62rem;
    color: #475569 !important;
    display: block;
    margin-top: 2px;
}
.sb-sw { position: relative; width: 36px; height: 20px; flex-shrink: 0; }
.sb-sw input { opacity: 0; width: 0; height: 0; position: absolute; }
.sb-sw-track {
    position: absolute; inset: 0;
    background-color: #1e293b;
    border-radius: 20px;
    border: 1px solid #334155;
    cursor: pointer;
    transition: background-color 0.18s, border-color 0.18s;
}
.sb-sw-track::after {
    content: '';
    position: absolute;
    width: 14px; height: 14px;
    background-color: #475569;
    border-radius: 50%;
    top: 2px; left: 2px;
    transition: transform 0.18s, background-color 0.18s;
    box-shadow: 0 1px 3px rgba(0,0,0,0.5);
}
.sb-sw input:checked ~ .sb-sw-track {
    background-color: #1d4ed8;
    border-color: #3b82f6;
}
.sb-sw input:checked ~ .sb-sw-track::after {
    transform: translateX(16px);
    background-color: #ffffff;
}

/* ── Summary box ── */
.sb-summary {
    background-color: #081526;
    border: 1px solid #1a3a5c;
    border-radius: 10px;
    padding: 12px 14px;
}
.sb-sum-title {
    font-size: 0.59rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    color: #334155 !important;
    margin-bottom: 7px;
}
.sb-sum-count {
    font-size: 1.4rem;
    font-weight: 800;
    color: #3b82f6 !important;
    line-height: 1;
    display: block;
    margin-bottom: 8px;
}
.sb-sum-row {
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 0.7rem;
    color: #64748b !important;
    padding: 2px 0;
}
.sb-sum-row .n {
    color: #cbd5e1 !important;
    font-weight: 600;
}

/* ── Reset button ── */
.sb-reset-btn {
    display: block;
    background-color: #450a0a;
    color: #fca5a5 !important;
    border: 1px solid #7f1d1d;
    border-radius: 9px;
    padding: 11px 14px;
    font-family: 'Inter','Segoe UI',sans-serif;
    font-size: 0.76rem;
    font-weight: 700;
    cursor: pointer;
    width: 100%;
    text-align: center;
    text-decoration: none;
    transition: background-color 0.13s, color 0.13s;
    letter-spacing: 0.01em;
}
.sb-reset-btn:hover {
    background-color: #991b1b;
    color: #ffffff !important;
    border-color: #ef4444;
}

/* ── Footer note ── */
.sb-foot {
    padding: 10px 18px 22px;
    font-size: 0.62rem;
    color: #334155 !important;
    text-align: center;
    line-height: 1.7;
}
.sb-foot a { color: #3b82f6 !important; text-decoration: none; }
.sb-foot a:hover { text-decoration: underline; }

/* ═══════════════════════════════════════════════════════════
   MAIN CONTENT
   ═══════════════════════════════════════════════════════════ */
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
.dash-header-text h1 {
    color:#fff; font-size:1.85rem; font-weight:800;
    margin:0; line-height:1.2; letter-spacing:-0.02em;
}
.dash-header-text p { color:rgba(255,255,255,0.65); margin:0.4rem 0 0; font-size:0.88rem; }
.dash-header-badge {
    background:rgba(255,255,255,0.15); backdrop-filter:blur(12px);
    border:1px solid rgba(255,255,255,0.25); color:#fff;
    padding:0.5rem 1.3rem; border-radius:50px;
    font-size:0.82rem; font-weight:600; white-space:nowrap;
    flex-shrink:0; position:relative; z-index:1;
}
.kpi-card {
    background:#fff; border-radius:16px; padding:1.3rem 1.2rem 1rem;
    box-shadow:0 1px 3px rgba(0,0,0,0.06),0 4px 16px rgba(0,0,0,0.05);
    border-top:4px solid; height:100%;
    transition:transform .2s,box-shadow .2s; overflow:hidden;
}
.kpi-card:hover { transform:translateY(-4px); box-shadow:0 12px 32px rgba(0,0,0,0.1); }
.kpi-label { font-size:0.69rem; font-weight:700; text-transform:uppercase;
             letter-spacing:0.09em; color:#6b7280; margin-bottom:0.5rem; }
.kpi-value { font-size:2rem; font-weight:800; line-height:1.05;
             margin-bottom:0.3rem; letter-spacing:-0.02em; }
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
.section-subtitle { font-size:0.82rem; color:#6b7280; margin-bottom:1rem;
                    line-height:1.5; padding-left:0.6rem; }
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
.region-card .rc-name  { font-size:0.72rem; font-weight:700; text-transform:uppercase;
                         letter-spacing:0.07em; margin-bottom:0.4rem; }
.region-card .rc-count { font-size:1.9rem; font-weight:800; color:#1e3a5f;
                         line-height:1; letter-spacing:-0.02em; }
.region-card .rc-sub   { font-size:0.74rem; color:#9ca3af; margin-bottom:0.6rem; }
.region-card .rc-detail { font-size:0.8rem; color:#374151; line-height:1.75;
                           background:#f9fafb; border-radius:8px;
                           padding:0.6rem 0.75rem; margin-top:0.5rem; }
.stTabs [data-baseweb="tab-list"] {
    background:#fff; border-radius:14px; padding:0.35rem 0.4rem;
    gap:0.2rem; box-shadow:0 1px 4px rgba(0,0,0,0.07); margin-bottom:1.3rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius:10px; padding:0.5rem 1.1rem; font-size:0.85rem;
    font-weight:500; color:#6b7280;
}
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
        df['Region_Short'] = df['Region'].map(region_map).fillna(df.get('Region_Short', df['Region']))
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
for k, v in [('sel_regions', all_regions.copy()),
             ('sel_crimes',  all_crimes.copy()),
             ('sel_months',  all_months.copy()),
             ('show_rate',   False)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Handle actions from query params ──
params = st.query_params
if 'action' in params:
    a = params['action']
    if   a == 'reset':        st.session_state.update({'sel_regions':all_regions.copy(),'sel_crimes':all_crimes.copy(),'sel_months':all_months.copy()})
    elif a == 'sug_active':   st.session_state['sel_regions'] = top3_regions
    elif a == 'sug_res':      st.session_state['sel_regions'] = top3_res_regions
    elif a == 'sug_trending': st.session_state['sel_crimes']  = top3_crimes
    elif a == 'sug_recent':   st.session_state['sel_months']  = all_months[-3:]
    elif a == 'toggle_rate':  st.session_state['show_rate']   = not st.session_state['show_rate']
    elif a == 'set_regions':
        v = params.get('v','')
        st.session_state['sel_regions'] = [x for x in v.split('||') if x in all_regions] or all_regions
    elif a == 'set_crimes':
        v = params.get('v','')
        st.session_state['sel_crimes'] = [x for x in v.split('||') if x in all_crimes] or all_crimes
    elif a == 'set_months':
        v = params.get('v','')
        st.session_state['sel_months'] = [x for x in v.split('||') if x in all_months] or all_months
    st.query_params.clear()
    st.rerun()

sel_r      = st.session_state['sel_regions']
sel_c      = st.session_state['sel_crimes']
sel_m      = st.session_state['sel_months']
show_rate  = st.session_state['show_rate']

# ============================================================
# SIDEBAR — pure st.markdown, no components.html, no iframe
# ============================================================
def chips_html(items, cls, max_show=3):
    out = ''
    for v in items[:max_show]:
        short = v[:14]+'…' if len(v) > 15 else v
        out += f'<span class="sb-chip {cls}" title="{v}">{short}</span>'
    extra = len(items) - max_show
    if extra > 0:
        out += f'<span class="sb-chip sb-chip-x">+{extra} more</span>'
    return out or '<span style="font-size:0.65rem;color:#334155;">None selected</span>'

def opts_html(key, items, sel_set, counts, id_prefix):
    out = ''
    for v in items:
        checked = 'checked' if v in sel_set else ''
        cnt = fmt_count(counts.get(v, 0))
        short = v[:26]+'…' if len(v) > 27 else v
        out += f'''<label class="sb-opt">
            <input type="checkbox" {checked} onchange="toggleOpt('{key}','{v.replace("'","\\'")}',this.checked)">
            <span class="sb-opt-name" title="{v}">{short}</span>
            <span class="sb-opt-cnt">{cnt}</span>
        </label>'''
    return out

# Build spike/recent button
if spike_month:
    sn = spike_month.strftime('%B %Y')
    spike_preset = f'''<button class="sb-preset-btn" onclick="doAction('sug_spike')">
        🚨 Crime Spike <small>{sn}</small></button>'''
else:
    spike_preset = '''<button class="sb-preset-btn" onclick="doAction('sug_recent')">
        📅 Latest Months <small>Most recent 3</small></button>'''

r_data_js = json.dumps([{"v":r,"c":fmt_count(region_counts.get(r,0))} for r in all_regions])
c_data_js = json.dumps([{"v":c,"c":fmt_count(crime_counts.get(c,0))} for c in all_crimes])
m_data_js = json.dumps([{"v":m,"c":fmt_count(month_counts.get(m,0))} for m in all_months])
sel_r_js  = json.dumps(sel_r)
sel_c_js  = json.dumps(sel_c)
sel_m_js  = json.dumps(sel_m)

rate_checked = 'checked' if show_rate else ''
nr, nc, nm = len(sel_r), len(sel_c), len(sel_m)

sidebar_html = f"""
<div class="sb-shell">

<!-- ══ HEADER ══════════════════════════════════════ -->
<div class="sb-header">
  <div class="sb-header-title">🔍 Crime Dashboard</div>
  <div class="sb-header-sub">UK Regional Overview · 2024–2025</div>
</div>

<!-- ══ QUICK APPLY ══════════════════════════════════ -->
<div class="sb-section">
  <div class="sb-sec-hdr">⚡ Quick Apply Presets</div>
  <div class="sb-preset-grid">
    <button class="sb-preset-btn" onclick="doAction('sug_active')">🏙️ Most Active <small>Top 3 regions</small></button>
    {spike_preset}
    <button class="sb-preset-btn" onclick="doAction('sug_trending')">📈 Trending Types <small>Top 3 crime types</small></button>
    <button class="sb-preset-btn" onclick="doAction('sug_res')">⚖️ Best Resolution <small>Top 3 regions</small></button>
  </div>
</div>

<!-- ══ REGION FILTER ════════════════════════════════ -->
<div class="sb-section">
  <div class="sb-filter-hdr">
    <span class="sb-filter-icon">🗺️</span>
    <span class="sb-filter-label">Region</span>
    <span class="sb-badge" id="r-badge">{nr}/{len(all_regions)}</span>
  </div>
  <div class="sb-pills" id="r-pills">{chips_html(sel_r,'sb-chip-r')}</div>
  <div class="sb-action-row">
    <button class="sb-act-btn" onclick="selAll('r')">✓ Select All</button>
    <button class="sb-act-btn clr" onclick="clrAll('r')">✕ Clear All</button>
  </div>
  <div class="sb-search-wrap">
    <span class="sb-search-icon">⌕</span>
    <input type="text" id="r-search" placeholder="Search regions…" oninput="filterOpts('r',this.value)" autocomplete="off">
  </div>
  <button class="sb-expand-btn" id="r-tog" onclick="togOpts('r')">▼ Show all options</button>
  <div class="sb-opts" id="r-opts">{opts_html('r', all_regions, set(sel_r), region_counts, 'r')}</div>
</div>

<!-- ══ CRIME TYPE FILTER ════════════════════════════ -->
<div class="sb-section">
  <div class="sb-filter-hdr">
    <span class="sb-filter-icon">🚨</span>
    <span class="sb-filter-label">Crime Type</span>
    <span class="sb-badge" id="c-badge">{nc}/{len(all_crimes)}</span>
  </div>
  <div class="sb-pills" id="c-pills">{chips_html(sel_c,'sb-chip-c',2)}</div>
  <div class="sb-action-row">
    <button class="sb-act-btn" onclick="selAll('c')">✓ Select All</button>
    <button class="sb-act-btn clr" onclick="clrAll('c')">✕ Clear All</button>
  </div>
  <div class="sb-search-wrap">
    <span class="sb-search-icon">⌕</span>
    <input type="text" id="c-search" placeholder="Search crime types…" oninput="filterOpts('c',this.value)" autocomplete="off">
  </div>
  <button class="sb-expand-btn" id="c-tog" onclick="togOpts('c')">▼ Show all options</button>
  <div class="sb-opts" id="c-opts">{opts_html('c', all_crimes, set(sel_c), crime_counts, 'c')}</div>
</div>

<!-- ══ MONTH FILTER ═════════════════════════════════ -->
<div class="sb-section">
  <div class="sb-filter-hdr">
    <span class="sb-filter-icon">📅</span>
    <span class="sb-filter-label">Month</span>
    <span class="sb-badge" id="m-badge">{nm}/{len(all_months)}</span>
  </div>
  <div class="sb-pills" id="m-pills">{chips_html(sel_m,'sb-chip-m')}</div>
  <div class="sb-action-row">
    <button class="sb-act-btn" onclick="selAll('m')">✓ Select All</button>
    <button class="sb-act-btn clr" onclick="clrAll('m')">✕ Clear All</button>
  </div>
  <div class="sb-search-wrap">
    <span class="sb-search-icon">⌕</span>
    <input type="text" id="m-search" placeholder="Search months…" oninput="filterOpts('m',this.value)" autocomplete="off">
  </div>
  <button class="sb-expand-btn" id="m-tog" onclick="togOpts('m')">▼ Show all options</button>
  <div class="sb-opts" id="m-opts">{opts_html('m', all_months, set(sel_m), month_counts, 'm')}</div>
</div>

<!-- ══ POPULATION TOGGLE ════════════════════════════ -->
<div class="sb-section">
  <div class="sb-sec-hdr">📊 Display Mode</div>
  <div class="sb-toggle-row" onclick="doAction('toggle_rate')">
    <div style="flex:1">
      <span class="sb-toggle-main">Adjust for Population</span>
      <span class="sb-toggle-hint">Show crimes per 100k residents</span>
    </div>
    <label class="sb-sw" onclick="event.stopPropagation()">
      <input type="checkbox" id="rate-chk" {rate_checked} onchange="doAction('toggle_rate')">
      <span class="sb-sw-track"></span>
    </label>
  </div>
</div>

<!-- ══ SUMMARY ══════════════════════════════════════ -->
<div class="sb-section">
  <div class="sb-sec-hdr">📋 Active Filters</div>
  <div class="sb-summary">
    <div class="sb-sum-title">Records Matched</div>
    <span class="sb-sum-count" id="rec-count">{len(df[df['Region_Short'].isin(sel_r)&df['Crime_Type'].isin(sel_c)&df['Month_Name'].isin(sel_m)]):,}</span>
    <div class="sb-sum-row">🗺️ &nbsp;<span id="sum-r"><span class="n">{nr}</span> of {len(all_regions)} regions</span></div>
    <div class="sb-sum-row">🚨 &nbsp;<span id="sum-c"><span class="n">{nc}</span> of {len(all_crimes)} crime types</span></div>
    <div class="sb-sum-row">📅 &nbsp;<span id="sum-m"><span class="n">{nm}</span> of {len(all_months)} months</span></div>
  </div>
</div>

<!-- ══ RESET ═════════════════════════════════════════ -->
<div class="sb-section">
  <button class="sb-reset-btn" onclick="doAction('reset')">🔄 Reset All Filters</button>
</div>

<!-- ══ FOOTER ════════════════════════════════════════ -->
<div class="sb-foot">
  Data: <a href="https://data.police.uk">data.police.uk</a> · Dec 2024 – May 2025
</div>
</div>

<script>
// ── Data ────────────────────────────────────────────
const ALL = {{ r:{r_data_js}, c:{c_data_js}, m:{m_data_js} }};
const SEL = {{ r:new Set({sel_r_js}), c:new Set({sel_c_js}), m:new Set({sel_m_js}) }};
const OPEN = {{ r:false, c:false, m:false }};
const MAX  = {{ r:3, c:2, m:3 }};
const CLS  = {{ r:'sb-chip-r', c:'sb-chip-c', m:'sb-chip-m' }};

// ── Navigate to trigger Python rerun ────────────────
function doAction(action, extra) {{
  const url = new URL(window.location.href);
  url.searchParams.set('action', action);
  if (extra) url.searchParams.set('v', extra);
  window.location.href = url.toString();
}}

// ── Toggle a single option ───────────────────────────
function toggleOpt(key, val, checked) {{
  if (checked) SEL[key].add(val); else SEL[key].delete(val);
  refreshPills(key);
  refreshBadge(key);
  refreshSummary();
  const joined = [...SEL[key]].join('||');
  doAction('set_' + (key==='r'?'regions':key==='c'?'crimes':'months'), joined);
}}

// ── Select All / Clear All ───────────────────────────
function selAll(key) {{
  ALL[key].forEach(d => SEL[key].add(d.v));
  const joined = [...SEL[key]].join('||');
  doAction('set_' + (key==='r'?'regions':key==='c'?'crimes':'months'), joined);
}}
function clrAll(key) {{
  SEL[key].clear();
  doAction('set_' + (key==='r'?'regions':key==='c'?'crimes':'months'), '');
}}

// ── Refresh pill display ─────────────────────────────
function refreshPills(key) {{
  const wrap = document.getElementById(key+'-pills');
  if (!wrap) return;
  const items = [...SEL[key]];
  const show  = items.slice(0, MAX[key]);
  const extra = items.length - show.length;
  let html = show.map(v => {{
    const short = v.length>15 ? v.slice(0,14)+'…' : v;
    return `<span class="sb-chip ${{CLS[key]}}" title="${{v}}">${{short}}</span>`;
  }}).join('');
  if (extra>0) html += `<span class="sb-chip sb-chip-x">+${{extra}} more</span>`;
  if (!html) html = '<span style="font-size:0.65rem;color:#334155;">None selected</span>';
  wrap.innerHTML = html;
}}

// ── Refresh badge ────────────────────────────────────
function refreshBadge(key) {{
  const el = document.getElementById(key+'-badge');
  if (el) el.textContent = SEL[key].size+'/'+ALL[key].length;
}}

// ── Refresh summary ──────────────────────────────────
function refreshSummary() {{
  const labels = {{ r:'regions', c:'crime types', m:'months' }};
  ['r','c','m'].forEach(k => {{
    const el = document.getElementById('sum-'+k);
    if (el) el.innerHTML = `<span class="n">${{SEL[k].size}}</span> of ${{ALL[k].length}} ${{labels[k]}}`;
  }});
}}

// ── Expand/collapse options panel ────────────────────
function togOpts(key) {{
  OPEN[key] = !OPEN[key];
  const panel = document.getElementById(key+'-opts');
  const btn   = document.getElementById(key+'-tog');
  if (panel) panel.classList.toggle('open', OPEN[key]);
  if (btn)   btn.textContent = OPEN[key] ? '▲ Hide options' : '▼ Show all options';
}}

// ── Live search filter ───────────────────────────────
function filterOpts(key, q) {{
  if (!OPEN[key]) togOpts(key);
  const panel = document.getElementById(key+'-opts');
  if (!panel) return;
  const ql = q.toLowerCase();
  panel.querySelectorAll('.sb-opt').forEach(row => {{
    const name = row.querySelector('.sb-opt-name');
    row.style.display = name && name.title.toLowerCase().includes(ql) ? '' : 'none';
  }});
}}
</script>
"""

with st.sidebar:
    st.markdown(sidebar_html, unsafe_allow_html=True)


# ============================================================
# APPLY FILTERS
# ============================================================
filtered = df[
    df['Region_Short'].isin(sel_r) &
    df['Crime_Type'].isin(sel_c) &
    df['Month_Name'].isin(sel_m)
]


# ============================================================
# CHART STYLE HELPER
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


# ============================================================
# HEADER
# ============================================================
active_count = (
    (len(sel_r) < len(all_regions)) +
    (len(sel_c) < len(all_crimes))  +
    (len(sel_m) < len(all_months))
)
badge_text = (f'📡 {active_count} Filter{"s" if active_count!=1 else ""} Active'
              if active_count else '📡 All Data Shown')

st.markdown(f"""
<div class="dash-header">
    <div class="dash-header-text">
        <h1>🔍 UK Regional Crime Dashboard</h1>
        <p>Interactive overview of reported crime across England &nbsp;·&nbsp;
           December 2024 – May 2025 &nbsp;·&nbsp; Source: data.police.uk</p>
    </div>
    <div class="dash-header-badge">{badge_text}</div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# KPI STRIP
# ============================================================
def render_kpi_strip(df_f):
    if len(df_f) == 0:
        return
    total     = len(df_f)
    top_crime  = df_f['Crime_Type'].value_counts().idxmax()
    top_region = df_f['Region_Short'].value_counts().idxmax()
    peak_month = df_f.groupby('Month_Name').size().idxmax()
    rk = ['Offender given','Local resolution','charged','summonsed','Formal action']
    resolved  = df_f['Outcome'].apply(lambda x: any(k.lower() in str(x).lower() for k in rk)).sum()
    res_rate  = round((resolved/total)*100, 1)

    k1,k2,k3,k4,k5 = st.columns(5)
    items = [
        (k1, ACCENT,   'Total Crimes Recorded', f'{total:,}',   f'Across {len(sel_m)} month(s)'),
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
# TABS
# ============================================================
tab_overview, tab_trends, tab_types, tab_regions, tab_map, tab_outcomes = st.tabs([
    '📊  Overview','📈  Trends Over Time','🔒  Crime Types',
    '🏙️  Regional View','🗺️  Crime Map','⚖️  Case Outcomes',
])


# ── TAB 1 — OVERVIEW ──────────────────────────────────────
with tab_overview:
    if len(filtered) == 0:
        st.markdown('<div class="empty-state"><h3>No data matches your current filters.</h3>'
                    '<p>Try adjusting your selections in the sidebar.</p></div>',
                    unsafe_allow_html=True)
    else:
        mc = (filtered.groupby(['Month','Region_Short']).size()
              .reset_index(name='Count').sort_values(['Region_Short','Month']))
        mc['Pct_Change'] = (mc.groupby('Region_Short')['Count'].pct_change()*100).round(1)
        latest_mc = mc[mc['Month']==mc['Month'].max()].dropna(subset=['Pct_Change'])

        if len(latest_mc) > 0:
            st.markdown('<div class="section-title" style="margin-bottom:0.25rem;">Latest Month — Change vs Previous Month</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-subtitle" style="padding-left:0.6rem;">Did crime go up or down last month compared to the month before?</div>', unsafe_allow_html=True)
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
                        <div class="kpi-value" style="color:{color};font-size:1.75rem;">{arrow} {abs(pct):.1f}%</div>
                        <div class="kpi-sub">{lbl} from previous month</div>
                    </div>""", unsafe_allow_html=True)
            st.markdown('')

        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Top 5 Most Reported Crimes</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-subtitle">The five crime types that appear most frequently in the selected data</div>', unsafe_allow_html=True)
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
            st.markdown('</div>', unsafe_allow_html=True)

        with col_r:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Crimes by Region</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-subtitle">Total reported crimes per police force area</div>', unsafe_allow_html=True)
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
            st.markdown('</div>', unsafe_allow_html=True)

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
            Most common crime: <strong>{top_c}</strong>. Resolution rate: <strong>{rr_s}%</strong>.
        </div>""", unsafe_allow_html=True)


# ── TAB 2 — TRENDS ────────────────────────────────────────
with tab_trends:
    if len(filtered) == 0:
        st.markdown('<div class="empty-state"><h3>No data to display.</h3></div>', unsafe_allow_html=True)
    else:
        monthly = filtered.groupby(['Month','Region_Short']).size().reset_index(name='Count')
        if show_rate:
            monthly['Pop']  = monthly['Region_Short'].map(POPULATION)
            monthly['Rate'] = (monthly['Count']/monthly['Pop']*100000).round(1)
            y_col, y_lbl = 'Rate','Crimes per 100,000 residents'
        else:
            y_col, y_lbl = 'Count','Number of Crimes'

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Monthly Crime Figures by Region</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">How the number of recorded crimes has changed each month</div>', unsafe_allow_html=True)
        fig_line = px.line(monthly, x='Month', y=y_col, color='Region_Short',
                           markers=True, color_discrete_map=REGION_COLORS,
                           labels={y_col:y_lbl,'Month':'','Region_Short':'Region'})
        fig_line.update_traces(line_width=2.5, marker_size=7)
        fig_line = style_chart(fig_line, height=390)
        fig_line.update_layout(hovermode='x unified')
        st.plotly_chart(fig_line, use_container_width=True)
        if show_rate:
            st.markdown('<div class="insight-box">💡 <strong>Why "per 100,000"?</strong> Adjusts for population so regions are fairly comparable.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Month-on-Month Change (%)</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Bars above zero = more crime than last month · Bars below zero = less</div>', unsafe_allow_html=True)
        mc2 = (filtered.groupby(['Month','Region_Short']).size()
               .reset_index(name='Count').sort_values(['Region_Short','Month']))
        mc2['Pct_Change'] = (mc2.groupby('Region_Short')['Count'].pct_change()*100).round(1)
        mc2 = mc2.dropna(subset=['Pct_Change'])
        if len(mc2) > 0:
            fig_mom = px.bar(mc2, x='Month', y='Pct_Change', color='Region_Short',
                             barmode='group', color_discrete_map=REGION_COLORS,
                             labels={'Pct_Change':'% Change','Month':'','Region_Short':'Region'})
            fig_mom.add_hline(y=0, line_color='#9ca3af', line_width=1)
            fig_mom = style_chart(fig_mom, height=330)
            st.plotly_chart(fig_mom, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ── TAB 3 — CRIME TYPES ───────────────────────────────────
with tab_types:
    if len(filtered) == 0:
        st.markdown('<div class="empty-state"><h3>No data to display.</h3></div>', unsafe_allow_html=True)
    else:
        col_l, col_r = st.columns([3,2])
        with col_l:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">All Crime Types — Ranked by Volume</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-subtitle">Every recorded crime category, most to least common</div>', unsafe_allow_html=True)
            tc = filtered['Crime_Type'].value_counts().reset_index()
            tc.columns = ['Crime Type','Count']
            fig_bar = px.bar(tc, x='Count', y='Crime Type', orientation='h',
                             color='Count', color_continuous_scale=['#dbeafe','#1d4ed8'],
                             text='Count', labels={'Count':'Number of Reports','Crime Type':''})
            fig_bar.update_traces(textposition='outside', textfont_size=10, texttemplate='%{text:,}')
            fig_bar = style_chart(fig_bar, height=420, legend=False)
            fig_bar.update_layout(coloraxis_showscale=False, yaxis=dict(autorange='reversed'),
                                  xaxis=dict(range=[0, tc['Count'].max()*1.3]))
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_r:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Share of All Reports</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-subtitle">Percentage breakdown by crime category</div>', unsafe_allow_html=True)
            top_n = tc.head(6).copy()
            if len(tc) > 6:
                top_n = pd.concat([top_n,
                    pd.DataFrame({'Crime Type':['All Others'],'Count':[tc.iloc[6:]['Count'].sum()]})
                ], ignore_index=True)
            fig_pie = px.pie(top_n, values='Count', names='Crime Type',
                             color_discrete_sequence=['#1e3a5f','#1d4ed8','#2563eb','#3b82f6','#60a5fa','#93c5fd','#bfdbfe'],
                             hole=0.45)
            fig_pie.update_traces(textposition='inside', textinfo='percent', textfont_size=11)
            fig_pie.update_layout(paper_bgcolor='white',
                                  font=dict(family='Inter,Segoe UI,sans-serif',color='#374151',size=10),
                                  margin=dict(l=10,r=10,t=10,b=10), height=270,
                                  legend=dict(font=dict(size=9),y=-0.25,orientation='h',xanchor='center',x=0.5))
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Crime Type Activity Over Time</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-subtitle">Darker = more crimes of that type that month</div>', unsafe_allow_html=True)
            heat = filtered.groupby(['Month','Crime_Type']).size().reset_index(name='Count')
            if len(heat) > 0:
                hp = heat.pivot(index='Crime_Type',columns='Month',values='Count').fillna(0)
                hp.columns = [c.strftime('%b %Y') if hasattr(c,'strftime') else c for c in hp.columns]
                fig_heat = px.imshow(hp, color_continuous_scale='Blues', aspect='auto',
                                     labels={'x':'','y':'','color':'Crimes'})
                fig_heat.update_layout(paper_bgcolor='white', plot_bgcolor='white',
                                       font=dict(family='Inter,Segoe UI,sans-serif',color='#374151',size=9),
                                       margin=dict(l=10,r=10,t=10,b=10), height=270,
                                       coloraxis_showscale=False)
                st.plotly_chart(fig_heat, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)


# ── TAB 4 — REGIONAL VIEW ─────────────────────────────────
with tab_regions:
    if len(filtered) == 0:
        st.markdown('<div class="empty-state"><h3>No data to display.</h3></div>', unsafe_allow_html=True)
    else:
        rc_df = filtered.groupby('Region_Short').size().reset_index(name='Total')
        rc_df['Population'] = rc_df['Region_Short'].map(POPULATION).fillna(0)
        rc_df['Per100k']    = (rc_df['Total']/rc_df['Population'].replace(0,1)*100000).round(1)
        rc_df['Top Crime']  = rc_df['Region_Short'].apply(
            lambda r: filtered[filtered['Region_Short']==r]['Crime_Type'].value_counts().idxmax()
            if len(filtered[filtered['Region_Short']==r])>0 else 'N/A')
        rk_r = ['Offender given','Local resolution','charged','summonsed','Formal action']
        rc_df['Res Rate'] = rc_df['Region_Short'].apply(
            lambda r: round(filtered[filtered['Region_Short']==r]['Outcome']
                .apply(lambda x: any(k.lower() in str(x).lower() for k in rk_r)).sum()
                /max(len(filtered[filtered['Region_Short']==r]),1)*100, 1))

        st.markdown('<div class="section-title" style="margin-bottom:0.25rem;">Region-by-Region Snapshot</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle" style="margin-bottom:1rem;padding-left:0.6rem;">Key figures for each police force area</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i,(_,row) in enumerate(rc_df.sort_values('Total',ascending=False).iterrows()):
            region = row['Region_Short']
            color  = REGION_COLORS.get(region, ACCENT)
            with cols[i%3]:
                st.markdown(f"""<div class="region-card" style="border-top-color:{color};">
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
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Side-by-Side Comparison</div>', unsafe_allow_html=True)
        if show_rate:
            rc_s = rc_df.sort_values('Per100k',ascending=False)
            x_c, x_l = 'Per100k','Crimes per 100,000 residents'
        else:
            rc_s = rc_df.sort_values('Total',ascending=False)
            x_c, x_l = 'Total','Total Crimes Recorded'
        fig_cmp = px.bar(rc_s, x='Region_Short', y=x_c,
                         color='Region_Short', color_discrete_map=REGION_COLORS,
                         text=x_c, labels={'Region_Short':'',x_c:x_l})
        fig_cmp.update_traces(textposition='outside', textfont_size=12, texttemplate='%{text:,.0f}')
        fig_cmp = style_chart(fig_cmp, height=360, legend=False)
        fig_cmp.update_layout(yaxis=dict(range=[0, rc_s[x_c].max()*1.2]))
        st.plotly_chart(fig_cmp, use_container_width=True)
        if show_rate:
            hr_r = rc_df.loc[rc_df['Per100k'].idxmax()]
            lr_r = rc_df.loc[rc_df['Per100k'].idxmin()]
            st.markdown(f"""<div class="insight-box"><strong>📌 Population-adjusted:</strong>
                <strong>{hr_r['Region_Short']}</strong> has the highest rate ({hr_r['Per100k']:,.1f} per 100k),
                <strong>{lr_r['Region_Short']}</strong> the lowest ({lr_r['Per100k']:,.1f}).</div>""",
                unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">What Types of Crime Happen in Each Region?</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Stacked bar shows crime mix per area</div>', unsafe_allow_html=True)
        top6_ct = filtered['Crime_Type'].value_counts().head(6).index.tolist()
        reg_type = filtered.copy()
        reg_type['Crime_Type_Group'] = reg_type['Crime_Type'].apply(lambda x: x if x in top6_ct else 'Other')
        rt = reg_type.groupby(['Region_Short','Crime_Type_Group']).size().reset_index(name='Count')
        fig_stk = px.bar(rt, x='Region_Short', y='Count', color='Crime_Type_Group', barmode='stack',
                         color_discrete_sequence=['#1e3a5f','#1d4ed8','#2563eb','#3b82f6','#60a5fa','#93c5fd','#bfdbfe'],
                         labels={'Region_Short':'','Count':'Number of Crimes','Crime_Type_Group':'Crime Type'})
        fig_stk = style_chart(fig_stk, height=360)
        st.plotly_chart(fig_stk, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ── TAB 5 — CRIME MAP ─────────────────────────────────────
with tab_map:
    if len(filtered) == 0:
        st.markdown('<div class="empty-state"><h3>No data to display.</h3></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Crime Locations Across England</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Each dot marks a reported crime location. Hover for details.</div>', unsafe_allow_html=True)
        md = filtered.dropna(subset=['Lat','Long']).copy()
        sample_n = min(8000, len(md))
        ms = md.sample(n=sample_n, random_state=42) if len(md)>sample_n else md
        fig_map = px.scatter_mapbox(ms, lat='Lat', lon='Long', color='Crime_Type',
                                    hover_name='Crime_Type',
                                    hover_data={'Region_Short':True,'Month_Name':True,'Lat':False,'Long':False},
                                    zoom=5.5, center={'lat':52.5,'lon':-1.5}, height=590, opacity=0.55)
        fig_map.update_layout(mapbox_style='open-street-map', paper_bgcolor='white',
                              font=dict(family='Inter,Segoe UI,sans-serif',color='#374151'),
                              margin=dict(l=0,r=0,t=0,b=0),
                              legend=dict(orientation='h',yanchor='top',y=-0.02,xanchor='center',x=0.5,font=dict(size=9)))
        st.plotly_chart(fig_map, use_container_width=True)
        if len(md) > sample_n:
            st.markdown(f'<div class="insight-box">📍 Showing {sample_n:,} of {len(md):,} locations for performance.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ── TAB 6 — CASE OUTCOMES ─────────────────────────────────
with tab_outcomes:
    if len(filtered)==0 or 'Outcome' not in filtered.columns:
        st.markdown('<div class="empty-state"><h3>No outcome data available.</h3></div>', unsafe_allow_html=True)
    else:
        rk_o = ['Offender given','Local resolution','charged','summonsed','Formal action']
        resolved_o = filtered['Outcome'].apply(lambda x: any(k.lower() in str(x).lower() for k in rk_o)).sum()
        rr_o = round((resolved_o/len(filtered))*100, 1)

        col_l, col_r = st.columns([3,2])
        with col_l:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">What Happened to Reported Cases?</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-subtitle">The most common outcomes recorded by police</div>', unsafe_allow_html=True)
            oc = filtered['Outcome'].value_counts().head(10).reset_index()
            oc.columns = ['Outcome','Count']
            oc['Outcome_Short'] = oc['Outcome'].apply(lambda x: x[:55]+'…' if len(str(x))>55 else x)
            fig_out = px.bar(oc, x='Count', y='Outcome_Short', orientation='h',
                             color='Count', color_continuous_scale=['#dbeafe','#1d4ed8'],
                             text='Count', labels={'Count':'Number of Cases','Outcome_Short':''})
            fig_out.update_traces(textposition='outside', textfont_size=10, texttemplate='%{text:,}')
            fig_out = style_chart(fig_out, height=400, legend=False)
            fig_out.update_layout(coloraxis_showscale=False, yaxis=dict(autorange='reversed'),
                                  xaxis=dict(range=[0, oc['Count'].max()*1.3]))
            st.plotly_chart(fig_out, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_r:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Overall Resolution Rate</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-subtitle">Proportion resulting in a positive justice outcome</div>', unsafe_allow_html=True)
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
                    'threshold':{'line':{'color':DANGER,'width':3},'thickness':0.75,'value':rr_o}
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
                caution, or local resolution.
                The remaining <strong>{100-rr_o:.1f}%</strong> were closed or remain open.
            </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Resolution Rate by Region</div>', unsafe_allow_html=True)
            reg_res = []
            for region in filtered['Region_Short'].unique():
                r_df  = filtered[filtered['Region_Short']==region]
                r_res = r_df['Outcome'].apply(lambda x: any(k.lower() in str(x).lower() for k in rk_o)).sum()
                reg_res.append({'Region':region,'Rate':round((r_res/len(r_df))*100,1)})
            reg_res_df = pd.DataFrame(reg_res).sort_values('Rate',ascending=True)
            fig_rr = px.bar(reg_res_df, x='Rate', y='Region', orientation='h',
                            color='Region', color_discrete_map=REGION_COLORS,
                            text='Rate', labels={'Rate':'Resolution Rate (%)','Region':''})
            fig_rr.update_traces(textposition='outside', textfont_size=11, texttemplate='%{text:.1f}%')
            fig_rr = style_chart(fig_rr, height=230, legend=False)
            fig_rr.update_layout(xaxis=dict(range=[0, reg_res_df['Rate'].max()*1.4]))
            st.plotly_chart(fig_rr, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="dash-footer">
    UK Regional Crime Dashboard &nbsp;·&nbsp;
    Data source: <a href="https://data.police.uk">data.police.uk</a> &nbsp;·&nbsp;
    December 2024 – May 2025<br>
    Built with Python · Streamlit · Plotly &nbsp;·&nbsp; Population estimates: ONS 2023
</div>
""", unsafe_allow_html=True)
