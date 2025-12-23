"""
Vietnam Job Market Dashboard
Design System: Clean Professional (Notion/Stripe inspired)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os
import re

# ============================================================================
# 1. PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Vietnam Job Market Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# 2. DESIGN SYSTEM & CSS TOKENS
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        /* Colors */
        --bg-color: #F8FAFC;
        --card-bg: #FFFFFF;
        --border-color: #E6EAF2;
        --text-primary: #0F172A;
        --text-secondary: #475569;
        --text-muted: #94A3B8;
        --accent-color: #2563EB;
        --accent-bg: #EFF6FF;
        --success-color: #16A34A;
        --success-bg: #DCFCE7;
        --warning-color: #D97706;
        --warning-bg: #FFEDD5;
        --danger-color: #DC2626;
        --danger-bg: #FEE2E2;
    }

    /* Global Reset */
    * {
        font-family: 'Inter', sans-serif;
        color: var(--text-primary);
    }
    
    .stApp {
        background-color: var(--bg-color);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #F1F5F9;
        border-right: 1px solid var(--border-color);
    }
    
    [data-testid="stSidebar"] .stMarkdown h1, 
    [data-testid="stSidebar"] .stMarkdown h2, 
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--text-primary) !important;
    }
    
    /* Typography */
    h1, h2, h3 {
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    /* Card Component */
    .dashboard-card {
        background-color: var(--card-bg);
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        padding: 24px;
        margin-bottom: 24px;
        height: 100%;
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 1px solid #F1F5F9;
    }
    
    .card-title {
        font-size: 15px;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* KPI Card */
    .kpi-card {
        background-color: var(--card-bg);
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        padding: 20px 24px;
        height: 140px;
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.05);
        border-color: var(--accent-color);
    }
    
    .kpi-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }
    
    .kpi-label {
        font-size: 12px;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    
    .kpi-icon {
        width: 36px;
        height: 36px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    
    .kpi-value {
        font-size: 32px;
        font-weight: 700;
        color: var(--text-primary);
        margin: 4px 0;
        letter-spacing: -1px;
    }
    
    .kpi-note {
        font-size: 12px;
        color: var(--text-muted);
        display: flex;
        align-items: center;
        gap: 6px;
        font-weight: 500;
    }
    
    /* Icon Tints */
    .icon-blue { background-color: var(--accent-bg); color: var(--accent-color); }
    .icon-green { background-color: var(--success-bg); color: var(--success-color); }
    .icon-orange { background-color: var(--warning-bg); color: var(--warning-color); }
    .icon-red { background-color: var(--danger-bg); color: var(--danger-color); }
    
    /* Header */
    .main-header {
        background-color: var(--bg-color);
        padding: 0 0 24px 0;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 32px;
    }
    
    .breadcrumb {
        font-size: 12px;
        color: var(--text-muted);
        margin-bottom: 8px;
        font-weight: 500;
    }
    
    .page-title {
        font-size: 28px;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    /* Filters */
    .filter-chip {
        display: inline-flex;
        align-items: center;
        background-color: #FFFFFF;
        border: 1px solid var(--accent-color);
        color: var(--accent-color);
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
        box-shadow: 0 1px 2px rgba(37, 99, 235, 0.1);
    }
    
    /* Streamlit Overrides */
    .stDataFrame {
        border: 1px solid var(--border-color);
        border-radius: 8px;
        box-shadow: none;
    }
    
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 3. DATA LOADING
# ============================================================================
@st.cache_data
def load_data():
    paths = [
        'data/clean/dataset_final.csv',
        'datasets/dataset_final.csv',
        '../data/clean/dataset_final.csv'
    ]
    
    df = None
    for path in paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            break
            
    if df is None:
        # Fallback data
        return pd.DataFrame({
            'job_title': ['Software Engineer', 'Data Analyst', 'Marketing Manager'],
            'city': ['Hồ Chí Minh', 'Hà Nội', 'Đà Nẵng'],
            'salary_min': [10, 15, 20],
            'salary_max': [20, 25, 30],
            'salary_median': [15, 20, 25],
            'experience': ['1 năm', '2 năm', '3 năm'],
            'exp_years': [1, 2, 3],
            'position_simple': ['Nhân viên', 'Nhân viên', 'Quản lý'],
            'region': ['Miền Nam', 'Miền Bắc', 'Miền Trung']
        })

    # Preprocessing
    if 'region' not in df.columns:
        df['region'] = df['city'].apply(classify_region)
    if 'position_simple' not in df.columns:
        df['position_simple'] = df['position_level'].apply(simplify_position)
    if 'exp_years' not in df.columns:
        df['exp_years'] = df['experience'].apply(parse_experience)
    if 'salary_median' not in df.columns:
        df['salary_median'] = (df['salary_min'] + df['salary_max']) / 2
        
    return df

def classify_region(city):
    if pd.isna(city): return 'Khác'
    city = str(city).lower()
    if any(x in city for x in ['hà nội', 'hải phòng', 'bắc ninh', 'quảng ninh']): return 'Miền Bắc'
    if any(x in city for x in ['hồ chí minh', 'bình dương', 'đồng nai', 'cần thơ']): return 'Miền Nam'
    if any(x in city for x in ['đà nẵng', 'huế', 'khánh hòa', 'nghệ an']): return 'Miền Trung'
    return 'Khác'

def simplify_position(pos):
    pos = str(pos).lower()
    if any(x in pos for x in ['giám đốc', 'director']): return 'Giám đốc'
    if any(x in pos for x in ['quản lý', 'manager']): return 'Quản lý'
    if any(x in pos for x in ['trưởng nhóm', 'lead']): return 'Trưởng nhóm'
    if any(x in pos for x in ['thực tập', 'intern']): return 'Thực tập'
    return 'Nhân viên'

def parse_experience(exp):
    if pd.isna(exp): return np.nan
    exp = str(exp).lower()
    match = re.search(r'(\d+)', exp)
    if match: return int(match.group(1))
    return 0 if 'không' in exp else np.nan

df = load_data()

# ============================================================================
# 4. SIDEBAR FILTERS
# ============================================================================
with st.sidebar:
    st.markdown("### Filters")
    
    if st.button("Reset Filters", type="secondary", use_container_width=True):
        st.session_state.region = 'All Regions'
        st.session_state.position = 'All Levels'
    
    st.markdown("---")
    
    # Region
    region_opts = ['All Regions'] + sorted(df['region'].dropna().unique().tolist())
    region = st.selectbox("Region", region_opts, key='region')
    
    # Position
    pos_opts = ['All Levels'] + sorted(df['position_simple'].dropna().unique().tolist())
    position = st.selectbox("Position Level", pos_opts, key='position')
    
    # Salary
    max_sal = int(df['salary_max'].max()) if df['salary_max'].notna().any() else 100
    salary_range = st.slider("Salary Range (Million VND)", 0, 200, (0, 200))
    
    # Experience
    exp_range = st.slider("Experience (Years)", 0, 15, (0, 15))
    
    st.markdown("---")
    st.caption("v2.1.0 | Professional Edition")

# Filter Logic
fdf = df.copy()
if region != 'All Regions':
    fdf = fdf[fdf['region'] == region]
if position != 'All Levels':
    fdf = fdf[fdf['position_simple'] == position]

fdf = fdf[
    (fdf['salary_median'].fillna(0) >= salary_range[0]) & 
    (fdf['salary_median'].fillna(999) <= salary_range[1])
]
fdf = fdf[
    (fdf['exp_years'].fillna(0) >= exp_range[0]) & 
    (fdf['exp_years'].fillna(999) <= exp_range[1])
]

# ============================================================================
# 5. MAIN CONTENT
# ============================================================================

# 5.1 Header
st.markdown("""
<div class="main-header">
    <div class="breadcrumb">Home / Analytics / Job Market</div>
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h1 class="page-title">Dashboard Overview</h1>
        <div style="font-size: 12px; color: #64748B; background: #F1F5F9; padding: 4px 12px; border-radius: 20px;">
            Last updated: Dec 23, 2025
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 5.2 Active Filters
active_filters_html = ""
if region != 'All Regions':
    active_filters_html += f'<span class="filter-chip">Region: {region}</span>'
if position != 'All Levels':
    active_filters_html += f'<span class="filter-chip">Position: {position}</span>'
if salary_range != (0, 200):
    active_filters_html += f'<span class="filter-chip">Salary: {salary_range[0]}-{salary_range[1]}M</span>'

if active_filters_html:
    st.markdown(f'<div style="margin-bottom: 24px;">{active_filters_html}</div>', unsafe_allow_html=True)

# 5.3 KPI Row (4 cols)
k1, k2, k3, k4 = st.columns(4, gap="medium")

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-top">
            <span class="kpi-label">Total Jobs</span>
            <div class="kpi-icon icon-blue">💼</div>
        </div>
        <div class="kpi-value">{len(fdf):,}</div>
        <div class="kpi-note">
            <span style="color: #16A34A; font-weight: 600;">● Active</span> &nbsp;postings
        </div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    median_sal = fdf['salary_median'].median() if len(fdf) > 0 else 0
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-top">
            <span class="kpi-label">Median Salary</span>
            <div class="kpi-icon icon-green">💰</div>
        </div>
        <div class="kpi-value">{median_sal:.1f}M</div>
        <div class="kpi-note">
            <span style="color: #64748B;">VND / Month</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    top_city = fdf['city'].mode()[0] if len(fdf) > 0 else "N/A"
    if len(top_city) > 15: top_city = top_city[:12] + "..."
    
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-top">
            <span class="kpi-label">Top Location</span>
            <div class="kpi-icon icon-orange">📍</div>
        </div>
        <div class="kpi-value" style="font-size: 24px; margin-top: 8px; margin-bottom: 8px;">{top_city}</div>
        <div class="kpi-note">
            Most active region
        </div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    avg_exp = fdf['exp_years'].mean() if len(fdf) > 0 else 0
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-top">
            <span class="kpi-label">Avg Experience</span>
            <div class="kpi-icon icon-red">🎓</div>
        </div>
        <div class="kpi-value">{avg_exp:.1f} <span style="font-size: 16px; color: #64748B; font-weight: 500;">Years</span></div>
        <div class="kpi-note">
            Required on average
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5.4 Charts Row 1 (8 cols + 4 cols)
c1, c2 = st.columns([8, 4], gap="medium")

# Chart Config
chart_config = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#64748B', size=11),
)
plotly_config = {'displayModeBar': False, 'staticPlot': False}

with c1:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header"><h3 class="card-title">Salary Distribution by Position</h3></div>', unsafe_allow_html=True)
    
    if len(fdf) > 0:
        pos_sal = fdf.groupby('position_simple')['salary_median'].median().sort_values(ascending=True)
        
        fig = go.Figure(go.Bar(
            x=pos_sal.values,
            y=pos_sal.index,
            orientation='h',
            marker_color='#2563EB',
            text=[f'{v:.1f}M' for v in pos_sal.values],
            textposition='auto',
            opacity=0.9
        ))
        
        fig.update_layout(
            **chart_config,
            height=320,
            xaxis=dict(showgrid=True, gridcolor='#F1F5F9', title="Median Salary (Million VND)"),
            yaxis=dict(showgrid=False),
            margin=dict(l=0, r=20, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    else:
        st.info("No data available")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header"><h3 class="card-title">Regional Share</h3></div>', unsafe_allow_html=True)
    
    if len(fdf) > 0:
        reg_counts = fdf['region'].value_counts()
        colors = ['#2563EB', '#60A5FA', '#93C5FD', '#BFDBFE']
        
        fig = go.Figure(go.Pie(
            labels=reg_counts.index,
            values=reg_counts.values,
            hole=0.7,
            marker=dict(colors=colors),
            textinfo='percent',
            textfont=dict(color='white')
        ))
        
        fig.update_layout(
            **chart_config,
            height=320,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    else:
        st.info("No data available")
    st.markdown('</div>', unsafe_allow_html=True)

# 5.5 Charts Row 2 (6 cols + 6 cols)
c3, c4 = st.columns(2, gap="medium")

with c3:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header"><h3 class="card-title">Salary Trend by Experience</h3></div>', unsafe_allow_html=True)
    
    if len(fdf) > 0:
        exp_sal = fdf.groupby('exp_years')['salary_median'].median().reset_index()
        exp_sal = exp_sal[exp_sal['exp_years'] <= 15]
        
        fig = go.Figure(go.Scatter(
            x=exp_sal['exp_years'],
            y=exp_sal['salary_median'],
            mode='lines+markers',
            line=dict(color='#2563EB', width=3, shape='spline'),
            marker=dict(size=8, color='white', line=dict(width=2, color='#2563EB'))
        ))
        
        fig.update_layout(
            **chart_config,
            height=300,
            xaxis=dict(showgrid=True, gridcolor='#F1F5F9', title="Years of Experience"),
            yaxis=dict(showgrid=True, gridcolor='#F1F5F9', title="Salary (Million VND)"),
            hovermode="x unified",
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    else:
        st.info("No data available")
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header"><h3 class="card-title">Top Industries</h3></div>', unsafe_allow_html=True)
    
    if 'job_fields' in fdf.columns and len(fdf) > 0:
        fields = fdf['job_fields'].dropna().value_counts().head(7)
        
        fig = go.Figure(go.Bar(
            x=fields.values,
            y=fields.index,
            orientation='h',
            marker_color='#94A3B8'
        ))
        
        fig.update_layout(
            **chart_config,
            height=300,
            yaxis={'categoryorder': 'total ascending'},
            xaxis=dict(showgrid=True, gridcolor='#F1F5F9', title="Number of Jobs"),
            margin=dict(l=150, r=20, t=20, b=20) # Increased left margin for labels
        )
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    else:
        st.info("No data available")
    st.markdown('</div>', unsafe_allow_html=True)

# 5.6 Data Table
st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
st.markdown('<div class="card-header"><h3 class="card-title">Recent Job Postings</h3></div>', unsafe_allow_html=True)

cols = ['job_title', 'city', 'position_simple', 'salary_min', 'salary_max', 'experience']
display_cols = [c for c in cols if c in fdf.columns]

st.dataframe(
    fdf[display_cols].head(100),
    use_container_width=True,
    height=400,
    hide_index=True
)
st.markdown('</div>', unsafe_allow_html=True)
