import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Engineered Features · Dashboard",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=IBM+Plex+Mono:wght@300;400;500&display=swap');

:root {
    --bg:       #07090f;
    --surf:     #0c0f1a;
    --card:     #101420;
    --bdr:      #181f2e;
    --bdr2:     #1f2940;
    --cyan:     #00e5c8;
    --amber:    #ffb938;
    --rose:     #ff4f82;
    --indigo:   #6a7fff;
    --lime:     #8fff6a;
    --text:     #d8e2f5;
    --muted:    #4d5f7a;
    --sans:     'Sora', sans-serif;
    --mono:     'IBM Plex Mono', monospace;
}

html, body, [class*="css"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surf) !important;
    border-right: 1px solid var(--bdr) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }

/* ── Headings ── */
h1, h2, h3, h4 {
    font-family: var(--sans) !important;
    letter-spacing: -0.025em;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: var(--card);
    border: 1px solid var(--bdr2);
    border-radius: 12px;
    padding: 16px 20px !important;
    position: relative;
    overflow: hidden;
    transition: border-color .2s;
}
[data-testid="stMetric"]:hover { border-color: var(--cyan); }
[data-testid="stMetric"]::after {
    content: '';
    position: absolute;
    inset: 0 0 auto 0;
    height: 2px;
    background: linear-gradient(90deg, var(--cyan), var(--indigo));
}
[data-testid="stMetricValue"] {
    font-family: var(--sans) !important;
    font-size: 1.55rem !important;
    font-weight: 800 !important;
    color: var(--cyan) !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.70rem !important;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    color: var(--muted) !important;
    font-weight: 600 !important;
}
[data-testid="stMetricDelta"] {
    font-family: var(--mono) !important;
    font-size: 0.78rem !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] button {
    font-family: var(--sans) !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.04em;
    color: var(--muted) !important;
    padding: 10px 16px !important;
    border-bottom: 2px solid transparent !important;
}       
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--cyan) !important;
    border-bottom-color: var(--cyan) !important;
}

/* ── Selectbox / Multiselect ── */
[data-testid="stSelectbox"] > div,
[data-testid="stMultiSelect"] > div {
    background: var(--card) !important;
    border-color: var(--bdr2) !important;
    border-radius: 8px !important;
}

/* ── Sliders ── */
[data-testid="stSlider"] > div > div > div > div { background: var(--cyan) !important; }

/* ── Buttons ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--cyan), #00b8a2) !important;
    color: #07090f !important;
    font-family: var(--sans) !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 9px 22px !important;
    letter-spacing: 0.04em !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(0,229,200,.25) !important;
}

/* ── Expander ── */
details {
    background: var(--card) !important;
    border: 1px solid var(--bdr2) !important;
    border-radius: 10px !important;
    padding: 4px 0 !important;
}

/* ── DataFrame ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--bdr2) !important;
    border-radius: 10px;
}

hr { border-color: var(--bdr) !important; }

/* ── Custom blocks ── */
.page-title {
    font-family: var(--sans);
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(120deg, var(--cyan) 0%, var(--indigo) 55%, var(--rose) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.15;
    margin-bottom: 4px;
}
.page-sub {
    font-family: var(--mono);
    font-size: 0.75rem;
    letter-spacing: 0.10em;
    color: var(--muted);
    margin-bottom: 24px;
}
.group-header {
    font-family: var(--sans);
    font-size: 1.0rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.01em;
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0 0 2px 0;
}
.group-desc {
    font-family: var(--mono);
    font-size: 0.68rem;
    letter-spacing: 0.08em;
    color: var(--muted);
    margin-bottom: 12px;
}
.insight {
    background: rgba(0,229,200,.06);
    border: 1px solid rgba(0,229,200,.2);
    border-left: 3px solid var(--cyan);
    border-radius: 0 8px 8px 0;
    padding: 11px 16px;
    font-size: 0.85rem;
    line-height: 1.6;
    margin: 8px 0 16px 0;
}
.warn {
    background: rgba(255,79,130,.06);
    border: 1px solid rgba(255,79,130,.2);
    border-left: 3px solid var(--rose);
    border-radius: 0 8px 8px 0;
    padding: 11px 16px;
    font-size: 0.85rem;
    line-height: 1.6;
    margin: 8px 0 16px 0;
}
</style>
""", unsafe_allow_html=True)

# ── PLOTLY BASE LAYOUT ───────────────────────────────────────────────────────
BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Sora, sans-serif", color="#7a8faa", size=11),
    title_font=dict(family="Sora, sans-serif", color="#d8e2f5", size=13),
    xaxis=dict(gridcolor="#141b2b", linecolor="#141b2b", zerolinecolor="#141b2b"),
    yaxis=dict(gridcolor="#141b2b", linecolor="#141b2b", zerolinecolor="#141b2b"),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#1f2940",
                font=dict(size=10, family="IBM Plex Mono")),
    margin=dict(l=36, r=16, t=44, b=36),
    hoverlabel=dict(bgcolor="#101420", bordercolor="#1f2940",
                    font=dict(family="IBM Plex Mono", size=11)),
)

PAL  = ["#00e5c8","#ffb938","#ff4f82","#6a7fff","#8fff6a","#ff8c4f","#c46aff","#4fccff"]
PAL2 = ["#00b8a2","#cc9420","#cc3060","#4a5fcc","#60cc40","#cc6030","#9040cc","#30a0cc"]

# ── DATA ─────────────────────────────────────────────────────────────────────
@st.cache_data
def make_data(n=24):
    np.random.seed(0)
    df = pd.DataFrame({
        'InStoreRevenue':        np.random.uniform(3000, 8000, n),
        'UberEatsRevenue':       np.random.uniform(1000, 4000, n),
        'DoorDashRevenue':       np.random.uniform(500,  3000, n),
        'SelfDeliveryRevenue':   np.random.uniform(200,  2000, n),
        'COGSRate':              np.random.uniform(0.25, 0.45, n),
        'OPEXRate':              np.random.uniform(0.15, 0.30, n),
        'SD_DeliveryTotalCost':  np.random.uniform(100,  800,  n),
        'TotalNetProfit':        np.random.uniform(500,  3000, n),
        'InStoreNetProfit':      np.random.uniform(200,  1500, n),
        'UberEatsNetProfit':     np.random.uniform(50,   800,  n),
        'DoorDashNetProfit':     np.random.uniform(20,   600,  n),
        'SelfDeliveryNetProfit': np.random.uniform(10,   400,  n),
        'MonthlyOrders':         np.random.randint(200,  1000, n),
        'InStoreOrders':         np.random.randint(80,   500,  n),
        'UberEatsOrders':        np.random.randint(40,   300,  n),
        'DoorDashOrders':        np.random.randint(20,   200,  n),
        'SelfDeliveryOrders':    np.random.randint(10,   100,  n),
        'CommissionRate':        np.random.uniform(0.15, 0.30, n),
        'UE_share':              np.random.uniform(0.10, 0.40, n),
        'DD_share':              np.random.uniform(0.05, 0.30, n),
        'SD_share':              np.random.uniform(0.02, 0.20, n),
        'DeliveryCostPerOrder':  np.random.uniform(2,    8,    n),
        'GrowthFactor':          np.random.uniform(0.9,  1.3,  n),
        'Venue':                 [f"Venue {i+1:02d}" for i in range(n)],
    })
    df['TotalRevenue'] = df[['InStoreRevenue','UberEatsRevenue',
                              'DoorDashRevenue','SelfDeliveryRevenue']].sum(axis=1)

    # ── Channel Revenue Ratios
    df['InStore_RevRatio'] = df['InStoreRevenue']      / df['TotalRevenue']
    df['UE_RevRatio']      = df['UberEatsRevenue']     / df['TotalRevenue']
    df['DD_RevRatio']      = df['DoorDashRevenue']     / df['TotalRevenue']
    df['SD_RevRatio']      = df['SelfDeliveryRevenue'] / df['TotalRevenue']

    # ── Cost-to-Revenue Ratios
    df['COGS_to_Rev']        = df['COGSRate']
    df['OPEX_to_Rev']        = df['OPEXRate']
    df['DeliveryCost_SDRev'] = np.where(df['SelfDeliveryRevenue'] > 0,
                                df['SD_DeliveryTotalCost'] / df['SelfDeliveryRevenue'], 0)
    df['TotalCostRate']      = df['COGSRate'] + df['OPEXRate']

    # ── Profit per Order
    safe = lambda c: np.where(df[c] > 0, df[c], 1)
    df['ProfitPerOrder']         = df['TotalNetProfit']        / safe('MonthlyOrders')
    df['InStore_ProfitPerOrder'] = df['InStoreNetProfit']      / safe('InStoreOrders')
    df['UE_ProfitPerOrder']      = df['UberEatsNetProfit']     / safe('UberEatsOrders')
    df['DD_ProfitPerOrder']      = df['DoorDashNetProfit']     / safe('DoorDashOrders')
    df['SD_ProfitPerOrder']      = df['SelfDeliveryNetProfit'] / safe('SelfDeliveryOrders')

    # ── Interaction Terms
    df['CommRate_x_UEshare']      = df['CommissionRate'] * df['UE_share']
    df['DeliveryCost_x_SDshare']  = df['DeliveryCostPerOrder'] * df['SD_share']
    df['CommRate_x_DDshare']      = df['CommissionRate'] * df['DD_share']

    # ── Growth-Adjusted Demand
    df['GrowthAdj_Orders']   = df['MonthlyOrders']     * df['GrowthFactor']
    df['GrowthAdj_Revenue']  = df['TotalRevenue']       * df['GrowthFactor']
    df['GrowthAdj_UEOrders'] = df['UberEatsOrders']     * df['GrowthFactor']
    df['GrowthAdj_SDOrders'] = df['SelfDeliveryOrders'] * df['GrowthFactor']

    return df

df = make_data()

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Controls")
    st.divider()

    st.markdown("**VENUE FILTER**")
    no_of_venue = df['Venue'].tolist()
    selected_venues = st.multiselect("Select Venues", no_of_venue, default=no_of_venue[:0],
                                      placeholder="Choose venues…")
    if not selected_venues:
        selected_venues = no_of_venue

    st.divider()
    st.markdown("**CHART TYPE**")
    chart_type = st.radio("Line charts display as", ["Lines + Markers", "Lines only", "Markers only"],
                          index=0)
    mode_map = {"Lines + Markers": "lines+markers", "Lines only": "lines", "Markers only": "markers"}
    line_mode = mode_map[chart_type]

    st.divider()
    st.markdown("**HIGHLIGHT METRIC**")
    highlight = st.selectbox("Focus metric across views", [
        "ProfitPerOrder", "TotalCostRate", "GrowthAdj_Revenue",
        "CommRate_x_UEshare", "InStore_RevRatio",
    ])

    st.divider()
    st.markdown('<span style="font-family:\'IBM Plex Mono\',monospace;font-size:0.66rem;color:#4d5f7a;letter-spacing:0.1em">24 VENUES · 5 FEATURE GROUPS</span>', unsafe_allow_html=True)

dff = df[df['Venue'].isin(selected_venues)].reset_index(drop=True)
idx = dff.index.tolist()

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">Engineered Features Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">FEATURE ENGINEERING · ACTIONABLE INTELLIGENCE · VENUE-LEVEL ANALYSIS</div>', unsafe_allow_html=True)

# ── TOP KPIs ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Avg Profit/Order",     f"${dff['ProfitPerOrder'].mean():.2f}",
          f"{((dff['ProfitPerOrder'].mean()/df['ProfitPerOrder'].mean())-1)*100:+.1f}% vs all")
k2.metric("Avg Total Cost Rate",  f"{dff['TotalCostRate'].mean():.2%}",
          f"COGS+OPEX combined")
k3.metric("Avg UE Revenue Ratio", f"{dff['UE_RevRatio'].mean():.2%}",
          f"UberEats channel share")
k4.metric("Avg Growth Adj Rev",   f"${dff['GrowthAdj_Revenue'].mean():,.0f}",
          "demand-adjusted")
k5.metric("Avg Commission×UE",    f"{dff['CommRate_x_UEshare'].mean():.4f}",
          "interaction term")
k6.metric("Venues Selected",      f"{len(dff)}",
          f"of {len(df)} total")

st.divider()

# ── TABS ──────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "📡 Channel Revenue Ratios",
    "💸 Cost-to-Revenue",
    "💰 Profit per Order",
    "🔗 Interaction Terms",
    "📈 Growth-Adjusted Demand",
    "🔍 Cross-Group Summary",
])

# helper: shared line chart factory
def line_chart(dff, cols, colors, title, yformat=None, height=340):
    fig = go.Figure()
    for col, color in zip(cols, colors):
        fig.add_trace(go.Scatter(
            x=dff['Venue'], y=dff[col],
            mode=line_mode,
            name=col,
            line=dict(color=color, width=2),
            marker=dict(size=7, symbol="circle"),
        ))
    layout = dict(title=title, xaxis_tickangle=-35, height=height, **BASE)
    if yformat:
        yaxis_dict = BASE.get('yaxis', {}).copy()
        yaxis_dict['tickformat'] = yformat
        layout['yaxis'] = yaxis_dict
    fig.update_layout(**layout)
    return fig

def bar_chart(dff, cols, colors, title, yformat=None, height=340, barmode="group"):
    fig = go.Figure()
    for col, color in zip(cols, colors):
        fig.add_trace(go.Bar(name=col, x=dff['Venue'], y=dff[col],
                             marker_color=color, opacity=0.85))
    layout = dict(title=title, xaxis_tickangle=-35, barmode=barmode, height=height, **BASE)
    if yformat:
        yaxis_dict = BASE.get('yaxis', {}).copy()
        yaxis_dict['tickformat'] = yformat
        layout['yaxis'] = yaxis_dict
    fig.update_layout(**layout)
    return fig

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — CHANNEL REVENUE RATIOS
# ════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    cols_cr = ['InStore_RevRatio','UE_RevRatio','DD_RevRatio','SD_RevRatio']
    colors_cr = PAL[:4]
    labels_cr = ['In-Store','UberEats','DoorDash','Self-Delivery']

    st.markdown('<div class="group-header">📡 Channel Revenue Ratios</div>', unsafe_allow_html=True)
    st.markdown('<div class="group-desc">SHARE OF TOTAL REVENUE ATTRIBUTED TO EACH DELIVERY / DINE-IN CHANNEL</div>', unsafe_allow_html=True)

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    for col, label, color, c in zip(cols_cr, labels_cr, colors_cr, [c1,c2,c3,c4]):
        c.metric(f"{label} Share", f"{dff[col].mean():.1%}",
                 f"max {dff[col].max():.1%} · min {dff[col].min():.1%}")

    c_left, c_right = st.columns(2)
    with c_left:
        fig = line_chart(dff, cols_cr, colors_cr,
                         "Channel Revenue Ratios by Venue", yformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

    with c_right:
        # Stacked bar — proportion per venue
        fig = bar_chart(dff, cols_cr, colors_cr,
                        "Stacked Channel Mix per Venue", yformat=".0%",
                        barmode="stack")
        st.plotly_chart(fig, use_container_width=True)

    # Heatmap — ratios across venues
    heat_data = dff.set_index('Venue')[cols_cr].T
    fig = go.Figure(go.Heatmap(
        z=heat_data.values,
        x=heat_data.columns.tolist(),
        y=labels_cr,
        colorscale=[[0,"#07090f"],[0.5,"#1f2940"],[1,"#00e5c8"]],
        text=np.round(heat_data.values, 3),
        texttemplate="%{text:.1%}",
        textfont=dict(size=9, family="IBM Plex Mono"),
    ))
    fig.update_layout(title="Revenue Ratio Heatmap (Venue × Channel)", height=220, **BASE)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="insight">💡 <b>Actionable:</b> Venues where <b>InStore_RevRatio &lt; 40%</b> are heavily aggregator-dependent — consider renegotiating commissions or incentivising direct orders to protect margins.</div>', unsafe_allow_html=True)

    with st.expander("📄 Raw data — Channel Revenue Ratios"):
        st.dataframe(dff[['Venue'] + cols_cr].style.format({c: "{:.2%}" for c in cols_cr}),
                     use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — COST-TO-REVENUE
# ════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    cols_cost = ['COGS_to_Rev','OPEX_to_Rev','DeliveryCost_SDRev','TotalCostRate']
    colors_cost = [PAL[2], PAL[3], PAL[4], PAL[1]]
    labels_cost = ['COGS Rate','OPEX Rate','Delivery Cost / SD Rev','Total Cost Rate']

    st.markdown('<div class="group-header">💸 Cost-to-Revenue Ratios</div>', unsafe_allow_html=True)
    st.markdown('<div class="group-desc">COST EFFICIENCY SIGNALS — HOW MUCH OF EACH REVENUE DOLLAR IS CONSUMED BY COST</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, label, c in zip(cols_cost, labels_cost, [c1,c2,c3,c4]):
        val = dff[col].mean()
        delta_flag = "🔴" if val > 0.5 else ("🟡" if val > 0.35 else "🟢")
        c.metric(label, f"{val:.2%}", delta_flag + " risk level")

    c_left, c_right = st.columns(2)
    with c_left:
        fig = line_chart(dff, cols_cost, colors_cost,
                         "Cost Rates by Venue", yformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

    with c_right:
        # Scatter COGS vs OPEX coloured by TotalCostRate
        fig = go.Figure(go.Scatter(
            x=dff['COGS_to_Rev'], y=dff['OPEX_to_Rev'],
            mode="markers+text",
            text=dff['Venue'],
            textposition="top center",
            textfont=dict(size=8, family="IBM Plex Mono", color="#4d5f7a"),
            marker=dict(
                size=12,
                color=dff['TotalCostRate'],
                colorscale=[[0,"#00e5c8"],[0.5,"#ffb938"],[1,"#ff4f82"]],
                showscale=True,
                colorbar=dict(title="Total Cost Rate", tickformat=".0%",
                              title_font=dict(size=10), tickfont=dict(size=9)),
                line=dict(width=0),
            )
        ))
        fig.add_vline(x=dff['COGS_to_Rev'].mean(), line_dash="dash",
                      line_color="#ffb938", opacity=0.5,
                      annotation_text="Avg COGS", annotation_position="top right")
        fig.add_hline(y=dff['OPEX_to_Rev'].mean(), line_dash="dash",
                      line_color="#6a7fff", opacity=0.5,
                      annotation_text="Avg OPEX", annotation_position="top right")
        fig.update_layout(title="COGS vs OPEX Rate (colour = Total Cost)",
                          xaxis_title="COGS Rate", yaxis_title="OPEX Rate",
                          xaxis_tickformat=".0%", yaxis_tickformat=".0%", **BASE)
        st.plotly_chart(fig, use_container_width=True)

    # Waterfall — average cost breakdown
    avg_cogs  = dff['COGS_to_Rev'].mean()
    avg_opex  = dff['OPEX_to_Rev'].mean()
    avg_dcost = dff['DeliveryCost_SDRev'].mean()
    avg_margin = 1 - avg_cogs - avg_opex - avg_dcost

    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute","relative","relative","relative","total"],
        x=["Revenue (100%)", "COGS", "OPEX", "SD Delivery Cost", "Net Margin"],
        y=[1, -avg_cogs, -avg_opex, -avg_dcost, avg_margin],
        connector=dict(line=dict(color="#1f2940")),
        decreasing=dict(marker_color="#ff4f82"),
        increasing=dict(marker_color="#00e5c8"),
        totals=dict(marker_color="#ffb938"),
        text=[f"{v:.1%}" for v in [1, avg_cogs, avg_opex, avg_dcost, avg_margin]],
        textposition="outside",
    ))
    fig.update_layout(title="Average Cost Waterfall — Revenue to Net Margin",
                      yaxis_tickformat=".0%", height=340, **BASE)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="warn">⚠️ <b>Watch:</b> Venues with <b>TotalCostRate &gt; 65%</b> leave dangerously thin margins. Prioritise COGS renegotiation or menu price adjustment for those outlets.</div>', unsafe_allow_html=True)

    with st.expander("📄 Raw data — Cost Ratios"):
        st.dataframe(dff[['Venue'] + cols_cost].style.format({c: "{:.3%}" for c in cols_cost}),
                     use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — PROFIT PER ORDER
# ════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    cols_ppo = ['ProfitPerOrder','InStore_ProfitPerOrder','UE_ProfitPerOrder',
                'DD_ProfitPerOrder','SD_ProfitPerOrder']
    colors_ppo = PAL[:5]
    labels_ppo = ['Total','In-Store','UberEats','DoorDash','Self-Delivery']

    st.markdown('<div class="group-header">💰 Profit per Order</div>', unsafe_allow_html=True)
    st.markdown('<div class="group-desc">CHANNEL-LEVEL PROFIT EFFICIENCY — DOLLARS EARNED PER ORDER FULFILLED</div>', unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    for col, label, c in zip(cols_ppo, labels_ppo, [c1,c2,c3,c4,c5]):
        c.metric(label, f"${dff[col].mean():.2f}",
                 f"σ {dff[col].std():.2f}")

    c_left, c_right = st.columns(2)
    with c_left:
        fig = line_chart(dff, cols_ppo, colors_ppo,
                         "Profit per Order by Venue", yformat="$,.2f")
        st.plotly_chart(fig, use_container_width=True)

    with c_right:
        # Box plots per channel
        fig = go.Figure()
        for col, label, color in zip(cols_ppo[1:], labels_ppo[1:], colors_ppo[1:]):
            fig.add_trace(go.Box(y=dff[col], name=label,
                                 marker_color=color, boxmean=True,
                                 line_width=1.5))
        fig.update_layout(title="Profit/Order Distribution by Channel",
                          yaxis_tickprefix="$", showlegend=False, **BASE)
        st.plotly_chart(fig, use_container_width=True)

    # Ranked bar — best performing venues by total ProfitPerOrder
    ranked = dff.sort_values('ProfitPerOrder', ascending=False)
    fig = go.Figure(go.Bar(
        x=ranked['Venue'], y=ranked['ProfitPerOrder'],
        marker=dict(
            color=ranked['ProfitPerOrder'],
            colorscale=[[0,"#1f2940"],[0.5,"#6a7fff"],[1,"#00e5c8"]],
            showscale=False,
        ),
        text=ranked['ProfitPerOrder'].map("${:.2f}".format),
        textposition="outside",
    ))
    fig.update_layout(title="Venues Ranked by Profit per Order (Total)",
                      xaxis_tickangle=-35, yaxis_tickprefix="$", height=320, **BASE)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="insight">💡 <b>Actionable:</b> Channels with the <b>lowest Profit/Order</b> (typically DoorDash) are candidates for order-minimum policies or delivery surcharges to lift per-order economics.</div>', unsafe_allow_html=True)

    with st.expander("📄 Raw data — Profit per Order"):
        st.dataframe(dff[['Venue'] + cols_ppo].style.format({c: "${:.3f}" for c in cols_ppo}),
                     use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — INTERACTION TERMS
# ════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    cols_int = ['CommRate_x_UEshare','DeliveryCost_x_SDshare','CommRate_x_DDshare']
    colors_int = [PAL[2], PAL[3], PAL[4]]
    labels_int = ['CommRate × UE_share','DeliveryCost × SD_share','CommRate × DD_share']

    st.markdown('<div class="group-header">🔗 Interaction Terms</div>', unsafe_allow_html=True)
    st.markdown('<div class="group-desc">COMPOUND COST SIGNALS — MULTIPLIED EFFECTS OF COMMISSION AND DELIVERY COSTS ON CHANNEL EXPOSURE</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for col, label, c in zip(cols_int, labels_int, [c1,c2,c3]):
        c.metric(label, f"{dff[col].mean():.4f}",
                 f"range {dff[col].min():.4f}–{dff[col].max():.4f}")

    c_left, c_right = st.columns(2)
    with c_left:
        fig = line_chart(dff, cols_int, colors_int,
                         "Interaction Terms by Venue")
        st.plotly_chart(fig, use_container_width=True)

    with c_right:
        # Bubble scatter: CommRate_x_UEshare vs TotalNetProfit, size=DeliveryCost_x_SDshare
        fig = go.Figure(go.Scatter(
            x=dff['CommRate_x_UEshare'],
            y=dff['TotalNetProfit'],
            mode="markers+text",
            text=dff['Venue'],
            textposition="top center",
            textfont=dict(size=8, family="IBM Plex Mono", color="#4d5f7a"),
            marker=dict(
                size=dff['DeliveryCost_x_SDshare'] * 40,
                color=dff['CommRate_x_DDshare'],
                colorscale=[[0,"#6a7fff"],[0.5,"#ffb938"],[1,"#ff4f82"]],
                showscale=True,
                colorbar=dict(title="CommRate×DD", tickfont=dict(size=9)),
                opacity=0.80,
                line=dict(width=0),
            )
        ))
        fig.update_layout(
            title="Bubble: CommRate×UE vs Profit (size=DelivCost×SD, colour=CommRate×DD)",
            xaxis_title="CommRate × UE_share",
            yaxis_title="Total Net Profit ($)",
            yaxis_tickprefix="$", **BASE
        )
        st.plotly_chart(fig, use_container_width=True)

    # Correlation matrix of interaction terms + profit
    corr_cols = cols_int + ['TotalNetProfit','CommissionRate','UE_share','DD_share','SD_share']
    corr = dff[corr_cols].corr()
    fig = go.Figure(go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.index,
        colorscale=[[0,"#ff4f82"],[0.5,"#0c0f1a"],[1,"#00e5c8"]],
        zmin=-1, zmax=1,
        text=np.round(corr.values, 2), texttemplate="%{text}",
        textfont=dict(size=9, family="IBM Plex Mono"),
    ))
    fig.update_layout(title="Interaction Term Correlation Matrix", height=380, **BASE)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="warn">⚠️ <b>Watch:</b> High <b>CommRate × UE_share</b> combined with high <b>CommRate × DD_share</b> creates a double-commission drag. Venues in the top quartile of both need urgent channel mix review.</div>', unsafe_allow_html=True)

    with st.expander("📄 Raw data — Interaction Terms"):
        st.dataframe(dff[['Venue'] + cols_int].style.format({c: "{:.5f}" for c in cols_int}),
                     use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — GROWTH-ADJUSTED DEMAND
# ════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    cols_gr = ['GrowthAdj_Orders','GrowthAdj_Revenue','GrowthAdj_UEOrders','GrowthAdj_SDOrders']
    colors_gr = [PAL[0], PAL[1], PAL[2], PAL[3]]
    labels_gr = ['Adj Orders','Adj Revenue','Adj UE Orders','Adj SD Orders']

    st.markdown('<div class="group-header">📈 Growth-Adjusted Demand Features</div>', unsafe_allow_html=True)
    st.markdown('<div class="group-desc">FORWARD-LOOKING DEMAND SIGNALS — RAW VOLUME SCALED BY VENUE GROWTH FACTOR</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, label, c in zip(cols_gr, labels_gr, [c1,c2,c3,c4]):
        c.metric(label, f"{dff[col].mean():,.1f}",
                 f"σ {dff[col].std():,.1f}")

    c_left, c_right = st.columns(2)
    with c_left:
        fig = line_chart(dff, cols_gr, colors_gr,
                         "Growth-Adjusted Demand by Venue")
        st.plotly_chart(fig, use_container_width=True)

    with c_right:
        # GrowthFactor distribution
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=dff['GrowthFactor'], nbinsx=12,
            marker_color="#00e5c8", opacity=0.8, name="GrowthFactor"
        ))
        fig.add_vline(x=1.0, line_dash="dash", line_color="#ff4f82",
                      annotation_text="Breakeven (1.0)", annotation_position="top right")
        fig.add_vline(x=dff['GrowthFactor'].mean(), line_dash="dot", line_color="#ffb938",
                      annotation_text=f"Avg {dff['GrowthFactor'].mean():.3f}",
                      annotation_position="top left")
        fig.update_layout(title="GrowthFactor Distribution Across Venues", **BASE)
        st.plotly_chart(fig, use_container_width=True)

    # Scatter: GrowthAdj_Revenue vs TotalNetProfit
    c_left2, c_right2 = st.columns(2)
    with c_left2:
        fig = go.Figure(go.Scatter(
            x=dff['GrowthFactor'], y=dff['GrowthAdj_Revenue'],
            mode="markers+text",
            text=dff['Venue'],
            textposition="top center",
            textfont=dict(size=8, family="IBM Plex Mono", color="#4d5f7a"),
            marker=dict(size=10, color=dff['GrowthAdj_Orders'],
                        colorscale=[[0,"#1f2940"],[1,"#00e5c8"]],
                        showscale=True,
                        colorbar=dict(title="Adj Orders", tickfont=dict(size=9))),
        ))
        fig.update_layout(title="GrowthFactor vs Growth-Adjusted Revenue",
                          xaxis_title="Growth Factor", yaxis_title="Adj Revenue ($)",
                          yaxis_tickprefix="$", **BASE)
        st.plotly_chart(fig, use_container_width=True)

    with c_right2:
        # Ranked venues by GrowthAdj_Revenue
        ranked_gr = dff.sort_values('GrowthAdj_Revenue', ascending=True).tail(12)
        fig = go.Figure(go.Bar(
            x=ranked_gr['GrowthAdj_Revenue'], y=ranked_gr['Venue'],
            orientation="h",
            marker=dict(
                color=ranked_gr['GrowthFactor'],
                colorscale=[[0,"#ff4f82"],[0.5,"#ffb938"],[1,"#00e5c8"]],
                showscale=True,
                colorbar=dict(title="Growth Factor", tickfont=dict(size=9)),
            ),
            text=ranked_gr['GrowthAdj_Revenue'].map("${:,.0f}".format),
            textposition="outside",
        ))
        fig.update_layout(title="Top Venues by Growth-Adjusted Revenue",
                          xaxis_tickprefix="$", **BASE)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="insight">💡 <b>Actionable:</b> Venues with <b>GrowthFactor &gt; 1.15</b> and high <b>GrowthAdj_Revenue</b> are prime candidates for capacity investment and marketing spend — they have the momentum to absorb it.</div>', unsafe_allow_html=True)

    with st.expander("📄 Raw data — Growth-Adjusted Demand"):
        st.dataframe(dff[['Venue','GrowthFactor'] + cols_gr].style.format(
            {'GrowthFactor': "{:.3f}", **{c: "{:,.1f}" for c in cols_gr}}),
            use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 6 — CROSS-GROUP SUMMARY
# ════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="group-header">🔍 Cross-Group Summary</div>', unsafe_allow_html=True)
    st.markdown('<div class="group-desc">UNIFIED VIEW — ALL FEATURE GROUPS TOGETHER FOR DECISION-MAKING</div>', unsafe_allow_html=True)

    # Radar chart per venue (top 6 by profit)
    top_venues = dff.nlargest(6, 'TotalNetProfit')['Venue'].tolist()
    radar_cols = ['InStore_RevRatio','TotalCostRate','ProfitPerOrder',
                  'CommRate_x_UEshare','GrowthAdj_Revenue']
    radar_labels = ['InStore Rev Ratio','Cost Rate','Profit/Order',
                    'Comm×UE Share','Growth-Adj Rev']

    # Normalise to 0–1
    norm_df = dff.set_index('Venue')[radar_cols].copy()
    for c in radar_cols:
        rng = norm_df[c].max() - norm_df[c].min()
        norm_df[c] = (norm_df[c] - norm_df[c].min()) / (rng if rng > 0 else 1)

    # Helper: convert hex to rgba
    def hex_to_rgba(hex_color, alpha=0.08):
        if hex_color.startswith("#"):
            hex_color = hex_color.lstrip("#")
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return f"rgba({r}, {g}, {b}, {alpha})"
        return hex_color

    fig = go.Figure()
    for i, venue in enumerate(top_venues):
        vals = norm_df.loc[venue, radar_cols].tolist()
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=radar_labels + [radar_labels[0]],
            fill="toself",
            name=venue,
            line=dict(color=PAL[i], width=1.8),
            fillcolor=hex_to_rgba(PAL[i]),
            opacity=0.9,
        ))
    fig.update_layout(
        polar=dict(bgcolor="rgba(0,0,0,0)",
                   radialaxis=dict(color="#4d5f7a", gridcolor="#141b2b", tickfont=dict(size=9)),
                   angularaxis=dict(color="#7a8faa")),
        title="Feature Radar — Top 6 Venues by Net Profit (normalised)",
        height=460,
        **{k: v for k, v in BASE.items() if k not in ["xaxis","yaxis"]}
    )
    st.plotly_chart(fig, use_container_width=True)

    # Correlation heatmap — all engineered features
    all_feat = [
        'InStore_RevRatio','UE_RevRatio','DD_RevRatio','SD_RevRatio',
        'COGS_to_Rev','OPEX_to_Rev','TotalCostRate',
        'ProfitPerOrder','UE_ProfitPerOrder','DD_ProfitPerOrder',
        'CommRate_x_UEshare','DeliveryCost_x_SDshare',
        'GrowthAdj_Orders','GrowthAdj_Revenue',
        'TotalNetProfit',
    ]
    corr_all = dff[all_feat].corr()
    fig = go.Figure(go.Heatmap(
        z=corr_all.values,
        x=corr_all.columns.tolist(),
        y=corr_all.index.tolist(),
        colorscale=[[0,"#ff4f82"],[0.5,"#07090f"],[1,"#00e5c8"]],
        zmin=-1, zmax=1,
        text=np.round(corr_all.values, 2), texttemplate="%{text}",
        textfont=dict(size=8, family="IBM Plex Mono"),
    ))
    fig.update_layout(title="All Engineered Features — Correlation Matrix",
                      height=520, **BASE)
    st.plotly_chart(fig, use_container_width=True)

    # Summary statistics table
    st.markdown("#### Summary Statistics — All Engineered Features")
    summary = dff[all_feat].describe().T[['mean','std','min','50%','max']].copy()
    summary.columns = ['Mean','Std Dev','Min','Median','Max']
    st.dataframe(summary.style.format("{:.4f}").background_gradient(
        subset=['Mean'], cmap='Blues'), use_container_width=True)

    st.markdown('<div class="insight">💡 <b>Key finding:</b> <b>TotalCostRate</b> is strongly negatively correlated with <b>TotalNetProfit</b> — cost structure is the primary controllable lever for profitability across all venues.</div>', unsafe_allow_html=True)