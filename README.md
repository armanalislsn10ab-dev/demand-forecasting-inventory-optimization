# Product Demand Forecasting & Inventory Optimization Hub

An end-to-end Production Engineering decision-support framework integrating relational database management (MySQL), supervised machine learning demand forecasting (Linear Regression & Random Forest), and an interactive Power BI dashboard.

---

## 📌 Project Overview
Static reorder points often lead to capital lockup in excess inventory or revenue loss from stockouts. This system dynamically predicts daily product demand and computes optimized inventory parameters to streamline production planning:

* **Safety Stock ($SS$):** Calculated using $1.65 \times \sigma_d$ to ensure a **95% service level**.
* **Reorder Point ($ROP$):** Dynamically set based on forecasted demand plus safety stock requirements.
* **Replenishment Quantity:** Automatically determined as $\max(0, ROP - \text{Current Inventory})$.

---

## 🛠️ Tech Stack & Tools
* **Database Management:** MySQL, SQLAlchemy, PyMySQL
* **Data Processing & Machine Learning:** Python (Pandas, NumPy, Scikit-Learn)
* **Data Visualization:** Matplotlib, Seaborn, Power BI
* **Version Control & Hosting:** Git, GitHub

---

## 📊 Pipeline Architecture & Script Breakdown

1. **`1_build_mysql_db.py`**: Ingests raw store transactions into a local MySQL database using chunking (`chunksize=10,000`).
2. **`2_eda_trends.py`**: Queries aggregate daily demand trends across store locations.
3. **`3_forecasting_baseline.py`**: Evaluates 7-day and 30-day moving average baselines.
4. **`4_baseline_error.py`**: Computes baseline benchmark error metrics (MAE & RMSE).
5. **`5_ml_forecast.py`**: Engineers lag features, rolling averages, and categorical encodings to train Linear Regression and Random Forest Regressors.
6. **`6_process_supply_chain.py`**: Applies Production Engineering inventory calculations and generates the master dataset (`fact_inventory.csv`).

---

## 🖥️ Power BI Dashboard Preview
![Baseline Forecast](<img width="1057" height="586" alt="Screenshot 2026-09-20 103516" src="https://github.com/user-attachments/assets/fa80d27a-baed-4cad-8d75-349fe3f5cc5e" />
)

### Key Performance Metrics Tracked:
* **Total Volume Sold:** 10 Million Units
* **Active Inventory Snapshot:** 26 Thousand Units
* **Reorder Pipeline Quantity:** 19 Thousand Units
* **Critical Stockouts Avoided:** Dynamic safety stock recalculation across target SKUs

---
