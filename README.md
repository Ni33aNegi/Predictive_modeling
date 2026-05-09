# ⚙️ Engineered Features Dashboard

A dark-themed, interactive **Streamlit dashboard** for venue-level feature engineering analysis across restaurant delivery channels (In-Store, UberEats, DoorDash, Self-Delivery).

---

## 📸 Overview

This dashboard transforms raw revenue, cost, and order data into **actionable engineered features** across 5 analytical groups — giving operators a unified view of channel performance, cost efficiency, and growth potential across 24 venues.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+

### Installation

```bash
git clone https://github.com/your-username/engineered-features-dashboard.git
cd engineered-features-dashboard
pip install -r requirements.txt
streamlit run app.py
```

### Requirements

```
streamlit
plotly
pandas
numpy
scikit-learn
```

---

## 📊 Features

The dashboard is organised into **6 tabs**:

| Tab | Description |
|-----|-------------|
| 📡 **Channel Revenue Ratios** | Share of total revenue per delivery/dine-in channel with heatmap & stacked bar |
| 💸 **Cost-to-Revenue** | COGS, OPEX, and delivery cost efficiency with waterfall chart |
| 💰 **Profit per Order** | Channel-level profit efficiency — dollars earned per order fulfilled |
| 🔗 **Interaction Terms** | Compound commission × channel-share signals with correlation matrix |
| 📈 **Growth-Adjusted Demand** | Forward-looking demand scaled by venue growth factor |
| 🔍 **Cross-Group Summary** | Radar chart + full correlation heatmap across all engineered features |

---

## 🧮 Engineered Features

**Channel Revenue Ratios** — `InStore_RevRatio`, `UE_RevRatio`, `DD_RevRatio`, `SD_RevRatio`

**Cost Ratios** — `COGS_to_Rev`, `OPEX_to_Rev`, `TotalCostRate`, `DeliveryCost_SDRev`

**Profit per Order** — `ProfitPerOrder`, `InStore_ProfitPerOrder`, `UE_ProfitPerOrder`, `DD_ProfitPerOrder`, `SD_ProfitPerOrder`

**Interaction Terms** — `CommRate_x_UEshare`, `CommRate_x_DDshare`, `DeliveryCost_x_SDshare`

**Growth-Adjusted Demand** — `GrowthAdj_Orders`, `GrowthAdj_Revenue`, `GrowthAdj_UEOrders`, `GrowthAdj_SDOrders`

---

## 🎛️ Sidebar Controls

- **Venue Filter** — multi-select to focus on specific venues
- **Chart Type** — toggle between Lines + Markers, Lines only, or Markers only
- **Highlight Metric** — surface a focus metric across all views

---

## 🎨 Design

- Dark UI with custom CSS (`#07090f` background, cyan/amber/rose accent palette)
- Fonts: **Sora** (headings/body) + **IBM Plex Mono** (data/labels)
- All charts built with **Plotly** — fully interactive and hover-enabled

---

## 📁 Project Structure

```
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
└── README.md
```

---

## 📄 License

MIT License — free to use and modify.
