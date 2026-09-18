# analyze.py
# SUMMARY: The two factors that genuinely predict breakdown are km_since_service
# (r=+0.40; 85 % of cars that broke down had above-median km since their last service)
# and load_factor (r=+0.22; 77 % of cars that broke down ran above-median load).
# Total mileage and age have near-zero correlation (r~=0.002 and r~=-0.001) and split
# broken vs healthy cars 50/50 -- they do not predict breakdown at all.
#
# Risk score: a 0-100 composite built from the two separating columns only.
# Each column is min-max normalised, then combined 70 % km_since_service + 30 % load_factor
# (weights match their relative correlation strengths).

import pandas as pd

# ── 1. Load data ─────────────────────────────────────────────────────────────

df = pd.read_csv("fleet_history.csv")

print("Fleet history loaded.")
print(f"  Total cars    : {len(df)}")
print(f"  Broke down    : {df['broke_down'].sum()}")
print(f"  Did not break : {(df['broke_down'] == 0).sum()}")
print()

# ── 2. Compare broke vs healthy groups, column by column ─────────────────────

broke = df[df.broke_down == 1]
ok    = df[df.broke_down == 0]

feature_cols = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]

print("Column-by-column group comparison")
print(f"  {'column':<22}  {'corr':>6}  {'broke>ok-median':>16}  {'verdict'}")
print("  " + "-" * 64)
for col in feature_cols:
    r = df[col].corr(df["broke_down"])
    ok_med = ok[col].median()
    sep = (broke[col] > ok_med).mean() * 100
    if abs(r) >= 0.20 and sep >= 65:
        verdict = "SEPARATES"
    else:
        verdict = "no signal"
    print(f"  {col:<22}  {r:>+6.3f}  {sep:>15.0f}%  {verdict}")

print()
print("Key finding: odometer_km and age_years are coin-flips (r ~= 0).")
print("The two real predictors are km_since_service and load_factor.")
print()

# ── 3. Build a simple 0–100 risk score ───────────────────────────────────────
#
# Method: min-max normalise each separating column to [0, 1], then weight and
# scale to [0, 100].  No machine learning needed.
#
# Weights reflect relative correlation strength:
#   km_since_service : 0.70  (r=+0.40, 85 % separation)
#   load_factor      : 0.30  (r=+0.22, 77 % separation)

def minmax(series: pd.Series) -> pd.Series:
    """Scale a series to the [0, 1] range."""
    lo, hi = series.min(), series.max()
    return (series - lo) / (hi - lo)

df["score_kms"]  = minmax(df["km_since_service"])
df["score_load"] = minmax(df["load_factor"])

df["risk_score"] = ((df["score_kms"] * 0.70 + df["score_load"] * 0.30) * 100).round(1)

# ── 4. Rank and print ─────────────────────────────────────────────────────────

ranked = df[["car_id", "km_since_service", "load_factor", "risk_score", "broke_down"]].sort_values(
    "risk_score", ascending=False
).reset_index(drop=True)

print("Top 10 highest-risk cars (fix these BEFORE the 80 % rule flags them)")
print(f"  {'rank':<5}  {'car_id':<10}  {'km_since_svc':>13}  {'load':>6}  {'risk_score':>10}  {'actually_broke':>14}")
print("  " + "-" * 68)
for i, row in ranked.head(10).iterrows():
    broke_marker = "YES" if row["broke_down"] == 1 else "-"
    print(
        f"  {i+1:<5}  {row['car_id']:<10}  "
        f"{row['km_since_service']:>13,.0f}  "
        f"{row['load_factor']:>6.2f}  "
        f"{row['risk_score']:>10.1f}  "
        f"{broke_marker:>14}"
    )

print()
print("Validation: breakdown rate in top-30 vs bottom-30 by risk score")
top30  = ranked.head(30)
bot30  = ranked.tail(30)
print(f"  Top 30  breakdown rate: {top30['broke_down'].mean()*100:.0f}%")
print(f"  Bottom 30 breakdown rate: {bot30['broke_down'].mean()*100:.0f}%")
