#!/usr/bin/env python3
"""Generate LOCAD Cabuyao June 2026 P&L Dashboard HTML — Financial view."""
from datetime import datetime

t43 = {
    '2026-06-01': 10523, '2026-06-02': 10171, '2026-06-03': 10173,
    '2026-06-04': 9464,  '2026-06-05': 14936, '2026-06-06': 24975,
    '2026-06-07': 10008, '2026-06-08': 8651,  '2026-06-09': 7959,
    '2026-06-10': 7587,  '2026-06-11': 7864,  '2026-06-12': 9546,
    '2026-06-13': 8623,  '2026-06-14': 9054,  '2026-06-15': 10755,
    '2026-06-16': 9778,  '2026-06-17': 7132,
    '2026-06-18': 7102,  '2026-06-19': 6628,  '2026-06-20': 6496,
    '2026-06-21': 6224,  '2026-06-22': 6971,  '2026-06-23': 0,
}

headcounts = {
    '2026-06-01': 137, '2026-06-02': 143, '2026-06-03': 151,
    '2026-06-04': 185, '2026-06-05': 192, '2026-06-06': 187,
    '2026-06-07': 161, '2026-06-08': 147, '2026-06-09': 127,
    '2026-06-10': 141, '2026-06-11': 130, '2026-06-12': 78,
    '2026-06-13': 137, '2026-06-14': 109, '2026-06-15': 120,
    '2026-06-16': 107, '2026-06-17': 116,
    '2026-06-18': 110, '2026-06-19': 87,  '2026-06-20': 101,
    '2026-06-21': 61,  '2026-06-22': 112, '2026-06-23': 111,
}

# Source: Weekly PNL spreadsheet — packaging = Total Cost − (HC × 1,167)
packaging = {
    '2026-06-01': 0.00,
    '2026-06-02': 65624.29,
    '2026-06-03': 78159.44,
    '2026-06-04': 102288.06,
    '2026-06-05': 107795.75,
    '2026-06-06': 107181.08,
    '2026-06-07': 97286.70,
    '2026-06-08': 59946.18,
    '2026-06-09': 64787.13,
    '2026-06-10': 52510.16,
    '2026-06-11': 51738.81,
    '2026-06-12': 36119.99,
    '2026-06-13': 45171.23,
    '2026-06-14': 30871.02,
    '2026-06-15': 87560.56,
    '2026-06-16': 35206.37,
    '2026-06-17': 54615.52,
    '2026-06-18': 51140.62,
    '2026-06-19': 31421.83,
    '2026-06-20': 35663.89,
    '2026-06-21': 40679.04,
    '2026-06-22': 18670.27,
}

# Source: Weekly PNL spreadsheet — per-material daily breakdown
# Columns: BW13, BW20, BW40, SF_Blk, SF_Clr, BoxXS, BoxS, BoxM, BoxL, BoxXL, BoxXXL, PkgTape, FragTape, FragSticker, WhseSupplies
pkg_materials = {
    # fmt: (BW13, BW20, BW40, SF_Blk, SF_Clr, BoxXS, BoxS, BoxM, BoxL, BoxXL, BoxXXL, PkgTape, FragTape, FragSticker, WhseSupplies)
    '2026-06-01': (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    '2026-06-02': (0,30331.44,0,2905,900,2156,2875,1845.25,2280,362.70,39.90,19050,1015,864,1000),
    '2026-06-03': (0,31214.88,12368.16,4150,1800,1655.50,3197,2989,4272,1255.50,39.90,12192,1377.50,648,1000),
    '2026-06-04': (0,52711.92,8245.44,4980,4800,1397,2415,1647,3120,362.70,0,18605.50,2247.50,756,1000),
    '2026-06-05': (4290,43288.56,17079.84,1660,2400,1265,2449.50,1967.25,3792,864.90,319.20,20828,5727.50,864,1000),
    '2026-06-06': (5070,34454.16,12957.12,10790,900,2865.50,4450.50,3751.50,10584,1618.20,159.60,16192.50,1740,648,1000),
    '2026-06-07': (2925,0,47116.80,1660,1800,3503.50,8153.50,3690.50,10176,2371.50,39.90,11049,3045,756,1000),
    '2026-06-08': (11115,0,22380.48,3320,1200,1111,2679.50,3538,3552,2036.70,0,6096,1377.50,540,1000),
    '2026-06-09': (4290,0,28270.08,7055,2700,1100,4703.50,2485.75,2688,530.10,1915.20,5842,1667.50,540,1000),
    '2026-06-10': (3900,0,24147.36,1245,900,962.50,7245,2714.50,2688,725.40,39.90,5207,1087.50,648,1000),
    '2026-06-11': (2925,24147.36,0,1245,1200,1375,3530.50,3217.75,5928,502.20,0,4826,870,972,1000),
    '2026-06-12': (5850,8245.44,0,1245,0,1534.50,3576.50,2973.75,7512,976.50,79.80,1460.50,1450,216,1000),
    '2026-06-13': (2340,22380.48,0,1245,300,1303.50,1713.50,1692.75,6864,390.60,39.90,4127.50,1450,324,1000),
    '2026-06-14': (3510,9717.84,1766.88,1660,300,940.50,770.50,183,4488,55.80,0,4127.50,1595,756,1000),
    '2026-06-15': (4485,45644.40,15312.96,1245,300,1221,2173.50,3965,3432,725.40,79.80,5334,2102.50,540,1000),
    '2026-06-16': (4875,9423.36,2061.36,4150,300,940.50,1874.50,1753.75,2208,446.40,0,4254.50,1595,324,1000),
    '2026-06-17': (5265,20613.60,1177.92,6640,4565,962.50,2265.50,1525,2304,418.50,0,5524.50,2030,324,1000),
    '2026-06-18': (4875,15901.92,0,6640,0,1111,4128.50,2440,7176,1450.80,39.90,3810,1667.50,900,1000),
    '2026-06-19': (3705,10601.28,0,2490,300,1424.50,2530,2089.25,3072,892.80,0,1651,1450,216,1000),
    '2026-06-20': (4290,14135.04,0,3320,600,555.50,920,1570.75,2688,251.10,0,4127.50,1450,756,1000),
    '2026-06-21': (7020,19435.68,588.96,2075,300,792,1000.50,274.50,2976,0,39.90,3365.50,1595,216,1000),
    '2026-06-22': (585,2355.84,1766.88,3320,1200,808.50,1138.50,838.75,1824,0,79.80,2667,870,216,1000),
    '2026-06-23': (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
}
MAT_NAMES = ['BW 13"','BW 20"','BW 40"','Stretch Film (Blk)','Stretch Film (Clr)',
             'Box XS','Box S','Box M','Box L','Box XL','Box XXL',
             'Packing Tape','Fragile Tape','Fragile Sticker','Whse. Supplies']
MAT_COLORS = ['#818cf8','#6366f1','#4f46e5','#f472b6','#ec4899',
              '#34d399','#10b981','#059669','#047857','#065f46','#064e3b',
              '#fb923c','#f97316','#fbbf24','#94a3b8']

# Source: Weekly PNL spreadsheet — Fulfillment Revenue column
fulfillment_revenue = {
    '2026-06-01': 195385.39,
    '2026-06-02': 232135.92,
    '2026-06-03': 193767.46,
    '2026-06-04': 209101.93,
    '2026-06-05': 247256.74,
    '2026-06-06': 210136.79,
    '2026-06-07': 386173.11,
    '2026-06-08': 333558.19,
    '2026-06-09': 216918.29,
    '2026-06-10': 157723.54,
    '2026-06-11': 151565.74,
    '2026-06-12': 122797.01,
    '2026-06-13': 213662.10,
    '2026-06-14': 143477.96,
    '2026-06-15': 219626.68,
    '2026-06-16': 192453.68,
    '2026-06-17': 192453.68,
    '2026-06-18': 130244.64,
    '2026-06-19': 127879.66,
    '2026-06-20': 118121.49,
    '2026-06-21': 90291.17,
    '2026-06-22': 141456.46,
}

DAILY_RATE   = 1167
DAILY_BUDGET = 145900
today_str    = '2026-06-23'

rows = []
for d in sorted(t43.keys()):
    vol   = t43[d]
    hc    = headcounts.get(d, 0)
    labor = hc * DAILY_RATE
    pkg   = packaging.get(d, None)
    rev   = fulfillment_revenue.get(d, None)
    total = labor + (pkg if pkg is not None else 0)
    margin = round(rev - total, 2) if rev is not None and pkg is not None else None
    cpo    = round(total / vol, 2) if vol > 0 else None
    rows.append({
        'date': d,
        'label': datetime.strptime(d, '%Y-%m-%d').strftime('%a, %-d %b'),
        'hc': hc, 'vol': vol,
        'labor': labor, 'pkg': pkg, 'rev': rev,
        'total': total, 'margin': margin, 'cpo': cpo,
        'vs_budget': total - DAILY_BUDGET,
        'is_today': d == today_str,
    })

mtd_vol    = sum(r['vol'] for r in rows)
mtd_labor  = sum(r['labor'] for r in rows)
mtd_pkg    = sum(r['pkg'] for r in rows if r['pkg'] is not None)
mtd_cost   = mtd_labor + mtd_pkg
mtd_rev    = sum(r['rev'] for r in rows if r['rev'] is not None)
mtd_budget = DAILY_BUDGET * len(rows)
budget_var = mtd_cost - mtd_budget
avg_hc     = round(sum(r['hc'] for r in rows) / len(rows), 1)
mtd_cpo    = round(mtd_cost / mtd_vol, 2) if mtd_vol > 0 else 0

def php(n): return f"₱{n:,.0f}"
def pct(n): return f"{n:.1f}%"

# ── Trend & Forecast ───────────────────────────────────────────────────────
JUNE_DAYS     = 30
MONTHLY_BUDGET = DAILY_BUDGET * JUNE_DAYS

complete = [r for r in rows if r['pkg'] is not None]  # days with full data
DAYS_WITH_DATA = len(complete)
DAYS_REMAINING = JUNE_DAYS - DAYS_WITH_DATA
last_complete_lbl = complete[-1]['label'] if complete else ''  # e.g. "Sun, 22 Jun"

def linreg(y_vals):
    """Returns (slope, intercept) via ordinary least squares."""
    n = len(y_vals)
    x = list(range(1, n + 1))
    mx, my = sum(x) / n, sum(y_vals) / n
    denom = sum((xi - mx) ** 2 for xi in x)
    slope = sum((x[i] - mx) * (y_vals[i] - my) for i in range(n)) / denom if denom else 0
    return slope, my - slope * mx

def stddev(vals):
    n = len(vals); m = sum(vals) / n
    return (sum((v - m) ** 2 for v in vals) / n) ** 0.5

# Regression on total daily cost (Jun 1-16)
cost_vals = [r['total'] for r in complete]
rev_vals  = [r['rev']   for r in complete]
hc_vals   = [r['hc']    for r in complete]
vol_vals  = [r['vol']   for r in complete]

cost_slope, cost_int = linreg(cost_vals)
rev_slope,  rev_int  = linreg(rev_vals)
hc_slope,   hc_int   = linreg(hc_vals)

# 7-day averages (Jun 10-16) — recent trend baseline
last7_cost = cost_vals[-7:]
last7_rev  = rev_vals[-7:]
last7_hc   = hc_vals[-7:]
last7_vol  = vol_vals[-7:]
avg7_cost  = round(sum(last7_cost) / 7)
avg7_rev   = round(sum(last7_rev)  / 7)
avg7_hc    = round(sum(last7_hc)   / 7)
avg7_vol   = round(sum(last7_vol)  / 7)
avg7_pkg   = round(avg7_cost - avg7_hc * DAILY_RATE)

cost_std   = stddev(last7_cost)

# Forecast days 17-30 using regression extrapolation + 7d average blend
# Regression forecast per day
fc_cost_reg = [round(cost_int + cost_slope * (DAYS_WITH_DATA + i)) for i in range(1, DAYS_REMAINING + 1)]
fc_rev_reg  = [round(rev_int  + rev_slope  * (DAYS_WITH_DATA + i)) for i in range(1, DAYS_REMAINING + 1)]
# 7-day average forecast (flat)
fc_cost_avg = [avg7_cost] * DAYS_REMAINING
fc_rev_avg  = [avg7_rev]  * DAYS_REMAINING
# Blended (60% regression, 40% 7d avg)
fc_cost = [round(0.6 * r + 0.4 * a) for r, a in zip(fc_cost_reg, fc_cost_avg)]
fc_rev  = [round(0.6 * r + 0.4 * a) for r, a in zip(fc_rev_reg,  fc_rev_avg)]
# Upper/lower band (±1 stdev of last 7 days)
fc_cost_hi = [c + round(cost_std) for c in fc_cost]
fc_cost_lo = [max(0, c - round(cost_std)) for c in fc_cost]

# Month-end projections
proj_cost_total  = mtd_cost  + sum(fc_cost)
proj_rev_total   = mtd_rev   + sum(fc_rev)
proj_bvar        = proj_cost_total - MONTHLY_BUDGET
proj_margin      = proj_rev_total  - proj_cost_total

# Remaining budget & recommended HC
remaining_budget       = MONTHLY_BUDGET - mtd_cost
daily_budget_remaining = round(remaining_budget / DAYS_REMAINING)
rec_hc                 = max(0, round((daily_budget_remaining - avg7_pkg) / DAILY_RATE))
rec_hc_cost            = rec_hc * DAILY_RATE + avg7_pkg

# Decision flags
def flag(val, lo, hi):
    if val <= lo: return '🟢'
    if val <= hi: return '🟡'
    return '🔴'

cost_pace_pct  = round(mtd_cost / (MONTHLY_BUDGET * DAYS_WITH_DATA / JUNE_DAYS) * 100, 1)
cost_flag      = flag(cost_pace_pct, 100, 115)
rev_cover_pct  = round(mtd_rev / mtd_cost * 100, 1) if mtd_cost else 0
rev_flag       = flag(100 - rev_cover_pct, 0, 20)  # inverted: low gap = good
cost_trend_dir = '📈 Rising' if cost_slope > 1000 else ('📉 Falling' if cost_slope < -1000 else '➡ Stable')
rev_trend_dir  = '📈 Rising' if rev_slope  > 1000 else ('📉 Falling' if rev_slope  < -1000 else '➡ Stable')
budget_flag    = flag(proj_cost_total, MONTHLY_BUDGET, MONTHLY_BUDGET * 1.1)

# Forecast date labels — dynamic start (day after last complete data day)
from datetime import date, timedelta
fc_dates = [date(2026, 6, 1) + timedelta(days=DAYS_WITH_DATA + i) for i in range(DAYS_REMAINING)]
fc_labels = [d.strftime('%-d %b') for d in fc_dates]

# Full month chart data (actual Jun 1-16 + forecast Jun 17-30)
all_labels     = [r['label'].split(', ')[1] if ', ' in r['label'] else r['label'] for r in complete] + fc_labels
actual_cost_js = [r['total'] for r in complete]
actual_rev_js  = [r['rev']   for r in complete]

# Forecast row HTML
def fc_row_html(i):
    d    = fc_dates[i]
    fc_c = fc_cost[i]; fc_r = fc_rev[i]
    fc_m = fc_r - fc_c
    mc   = '#16a34a' if fc_m >= 0 else '#dc2626'
    vs   = fc_c - DAILY_BUDGET
    vc   = '#dc2626' if vs > 0 else '#16a34a'
    vs_s = ('+' if vs > 0 else '') + php(vs)
    weekday = d.strftime('%a')
    return f'''<tr style="background:#f8f7ff;color:#475569;font-style:italic">
      <td>{weekday}, {fc_labels[i]} <span style="font-size:10px;background:#6366f1;color:#fff;padding:1px 6px;border-radius:3px">FORECAST</span></td>
      <td style="text-align:right">{avg7_hc}</td>
      <td style="text-align:right">{avg7_vol:,}</td>
      <td style="text-align:right">{php(avg7_hc*DAILY_RATE)}</td>
      <td style="text-align:right">{php(avg7_pkg)}</td>
      <td style="text-align:right;font-weight:600">{php(fc_c)}</td>
      <td style="text-align:right;color:{vc};font-size:12px">{vs_s}</td>
      <td style="text-align:right">{php(fc_r)}</td>
      <td style="text-align:right;color:{mc}">{php(fc_m)}</td>
      <td style="text-align:right;color:#94a3b8">{php(round(fc_c/avg7_vol,2)) if avg7_vol else "—"}</td>
    </tr>'''

def row_html(r):
    bg = 'background:#fefce8;' if r['is_today'] else ''
    today_b = ' <span style="font-size:10px;background:#f59e0b;color:#fff;padding:1px 6px;border-radius:3px">TODAY</span>' if r['is_today'] else ''
    var = r['vs_budget']
    var_c = '#dc2626' if var > 0 else '#16a34a'
    var_s = ('+' if var > 0 else '') + php(var)
    pkg_s = php(r['pkg']) if r['pkg'] is not None else '<span style="color:#94a3b8;font-size:12px">pending</span>'
    rev_s = php(r['rev']) if r['rev'] is not None else '<span style="color:#94a3b8;font-size:12px">pending</span>'
    if r['margin'] is not None:
        mc = '#16a34a' if r['margin'] >= 0 else '#dc2626'
        margin_s = f'<span style="color:{mc}">{php(r["margin"])}</span>'
    else:
        margin_s = '<span style="color:#94a3b8;font-size:12px">pending</span>'
    cpo_s = f'₱{r["cpo"]:,.1f}' if r['cpo'] else '—'
    return f'''<tr style="{bg}">
      <td>{r["label"]}{today_b}</td>
      <td style="text-align:right">{r["hc"]}</td>
      <td style="text-align:right">{r["vol"]:,}</td>
      <td style="text-align:right">{php(r["labor"])}</td>
      <td style="text-align:right">{pkg_s}</td>
      <td style="text-align:right;font-weight:600">{php(r["total"])}</td>
      <td style="text-align:right;color:{var_c};font-size:12px">{var_s}</td>
      <td style="text-align:right">{rev_s}</td>
      <td style="text-align:right">{margin_s}</td>
      <td style="text-align:right;color:#64748b">{cpo_s}</td>
    </tr>'''

def pkg_row_html(r):
    if r['pkg'] is None: return ''
    pkg_pct_cost = round(r['pkg']/r['total']*100,1) if r['total']>0 else 0
    pkg_pct_rev  = round(r['pkg']/r['rev']*100,1)   if r['rev']  else None
    ppo          = round(r['pkg']/r['vol'],2)        if r['vol']>0 else None
    bar_w        = int(min(r['pkg'],200000)/200000*120)
    return f'''<tr>
      <td>{r["label"]}</td>
      <td style="text-align:right">{php(r["pkg"])}</td>
      <td style="text-align:right;color:#64748b">{pkg_pct_cost}%</td>
      <td style="text-align:right;color:#64748b">{"—" if pkg_pct_rev is None else str(pkg_pct_rev)+"%"}</td>
      <td style="text-align:right;color:#64748b">{"—" if ppo is None else "₱"+str(ppo)}</td>
      <td><div style="background:#ddd6fe;height:10px;border-radius:4px;width:{bar_w}px;margin-top:2px"></div></td>
    </tr>'''

import json as _j
lbl  = _j.dumps([r['label'] for r in rows])
lab  = _j.dumps([r['labor'] for r in rows])
pkg_ = _j.dumps([r['pkg'] if r['pkg'] is not None else 0 for r in rows])
bud_ = _j.dumps([DAILY_BUDGET]*len(rows))
rev_ = _j.dumps([r['rev'] for r in rows])
tc_  = _j.dumps([r['labor'] + (r['pkg'] or 0) for r in rows])

# Forecast chart data
fc_all_lbl_js   = _j.dumps(all_labels)
fc_act_cost_js  = _j.dumps(actual_cost_js + [None]*DAYS_REMAINING)
fc_act_rev_js   = _j.dumps(actual_rev_js  + [None]*DAYS_REMAINING)
fc_proj_cost_js = _j.dumps([None]*DAYS_WITH_DATA + fc_cost)
fc_proj_rev_js  = _j.dumps([None]*DAYS_WITH_DATA + fc_rev)
fc_proj_hi_js   = _j.dumps([None]*DAYS_WITH_DATA + fc_cost_hi)
fc_proj_lo_js   = _j.dumps([None]*DAYS_WITH_DATA + fc_cost_lo)
fc_budget_js    = _j.dumps([DAILY_BUDGET]*JUNE_DAYS)

# Packaging detail chart — only days with data (Jun 1-16)
pkg_detail_rows = [r for r in rows if r['pkg'] is not None]
pkg_lbl  = _j.dumps([r['label'] for r in pkg_detail_rows])
pkg_vals = _j.dumps([r['pkg'] for r in pkg_detail_rows])
pkg_pct  = _j.dumps([round(r['pkg']/r['total']*100,1) if r['total']>0 else 0 for r in pkg_detail_rows])

# Per-material datasets for stacked chart (16 days that have data)
mat_dates = [d for d in sorted(pkg_materials.keys())]
mat_datasets = []
for i, name in enumerate(MAT_NAMES):
    vals = [pkg_materials[d][i] for d in mat_dates if d in pkg_materials]
    if sum(vals) > 0:  # skip zero-usage materials
        mat_datasets.append({'name': name, 'color': MAT_COLORS[i], 'vals': vals})
mat_lbl_js  = _j.dumps([datetime.strptime(d,'%Y-%m-%d').strftime('%-d %b') for d in mat_dates])
mat_datasets_js = _j.dumps([{'label':m['name'],'data':m['vals'],
    'backgroundColor':m['color'],'stack':'m'} for m in mat_datasets])

# MTD totals per material
mat_totals = [(MAT_NAMES[i], sum(pkg_materials[d][i] for d in mat_dates)) for i in range(len(MAT_NAMES))]
mat_totals_sorted = sorted([(n,v) for n,v in mat_totals if v>0], key=lambda x:-x[1])
mtd_pkg_check = sum(v for _,v in mat_totals)

def mat_summary_rows():
    rows_html = ''
    for name, val in mat_totals_sorted:
        pct = round(val/mtd_pkg*100,1) if mtd_pkg>0 else 0
        bar = int(min(val,max(v for _,v in mat_totals_sorted))/max(v for _,v in mat_totals_sorted)*100)
        rows_html += f'''<tr>
          <td>{name}</td>
          <td style="text-align:right;font-weight:600">{php(val)}</td>
          <td style="text-align:right;color:#64748b">{pct}%</td>
          <td><div style="background:#ddd6fe;height:8px;border-radius:3px;width:{bar}%"></div></td>
        </tr>'''
    return rows_html

gen = datetime.now().strftime('%b %-d, %Y %H:%M')

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="300">
<title>LOCAD Cabuyao — June 2026 P&L</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f1f5f9;color:#1e293b;font-size:14px}}
.header{{background:#0f172a;color:#fff;padding:20px 32px;display:flex;justify-content:space-between;align-items:flex-end}}
.header h1{{font-size:20px;font-weight:700;letter-spacing:-.3px}}
.header .sub{{font-size:13px;color:#94a3b8;margin-top:4px}}
.header .ts{{font-size:11px;color:#475569}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(195px,1fr));gap:14px;padding:24px 32px 8px}}
.kpi{{background:#fff;border-radius:10px;padding:16px 18px;box-shadow:0 1px 2px rgba(0,0,0,.05)}}
.kpi .lbl{{font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:#64748b;margin-bottom:5px}}
.kpi .val{{font-size:26px;font-weight:700;line-height:1.1}}
.kpi .hint{{font-size:11px;color:#94a3b8;margin-top:5px}}
.section{{padding:16px 32px 32px}}
.section h2{{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#94a3b8;margin-bottom:14px}}
.charts{{display:grid;grid-template-columns:3fr 2fr;gap:16px;margin-bottom:24px}}
.card{{background:#fff;border-radius:10px;padding:20px;box-shadow:0 1px 2px rgba(0,0,0,.05)}}
.card h3{{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.07em;color:#94a3b8;margin-bottom:14px}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 1px 2px rgba(0,0,0,.05)}}
th{{background:#f8fafc;padding:10px 12px;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:#64748b;font-weight:600;white-space:nowrap}}
td{{padding:9px 12px;border-bottom:1px solid #f1f5f9;white-space:nowrap}}
tr:last-child td{{border-bottom:none}}
tr:hover td{{background:#f8fafc}}
tfoot td{{background:#0f172a;color:#fff;font-weight:600;padding:10px 12px}}
@media(max-width:900px){{.charts{{grid-template-columns:1fr}}.kpis{{grid-template-columns:repeat(2,1fr)}}.section,.header{{padding-left:16px;padding-right:16px}}}}
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>LOCAD Cabuyao (LISP) FC &mdash; June 2026 P&amp;L</h1>
    <div class="sub">{len(rows)} days MTD</div>
  </div>
  <div style="display:flex;align-items:center;gap:16px">
    <div class="ts" id="tsLabel">Updated {gen}</div>
  </div>
</div>

<div class="kpis">
  <div class="kpi">
    <div class="lbl">MTD Total Cost</div>
    <div class="val">{php(mtd_cost)}</div>
    <div class="hint">Budget: {php(mtd_budget)}</div>
  </div>
  <div class="kpi">
    <div class="lbl">Budget Variance</div>
    <div class="val" style="color:{'#dc2626' if budget_var>0 else '#16a34a'}">{('+' if budget_var>0 else '')}{php(budget_var)}</div>
    <div class="hint">{round(mtd_cost/mtd_budget*100,1)}% of MTD budget used</div>
  </div>
  <div class="kpi">
    <div class="lbl">MTD Labor</div>
    <div class="val">{php(mtd_labor)}</div>
    <div class="hint">Avg {avg_hc:.0f} HC/day · ₱{DAILY_RATE:,}/head</div>
  </div>
  <div class="kpi" style="cursor:pointer" onclick="togglePkg()" title="Click to view packaging detail">
    <div class="lbl">MTD Packaging (Jun 1–{complete[-1]['date'][8:]}) <span id="pkgArrow" style="float:right;font-size:13px;color:#6366f1">▼ Details</span></div>
    <div class="val">{php(mtd_pkg)}</div>
    <div class="hint">{today_str} pending entry</div>
  </div>
  <div class="kpi">
    <div class="lbl">MTD Revenue (Jun 1–{complete[-1]['date'][8:]})</div>
    <div class="val">{php(mtd_rev)}</div>
    <div class="hint">Fulfillment billing · {today_str} pending</div>
  </div>
  <div class="kpi">
    <div class="lbl">MTD Volume</div>
    <div class="val">{mtd_vol:,}</div>
    <div class="hint">Avg CPO: {php(mtd_cpo)}</div>
  </div>
</div>

<div class="section">
  <h2>Cost vs Budget</h2>
  <div class="charts">
    <div class="card">
      <h3>Daily Cost Breakdown vs Budget (₱)</h3>
      <canvas id="costChart" height="160"></canvas>
    </div>
    <div class="card">
      <h3>Revenue vs Cost — Jun 1–{complete[-1]['date'][8:]}</h3>
      <canvas id="revChart" height="160"></canvas>
    </div>
  </div>

  <h2>Daily Detail</h2>
  <table>
    <thead>
      <tr>
        <th>Date</th>
        <th style="text-align:right">HC</th>
        <th style="text-align:right">Orders</th>
        <th style="text-align:right">Labor</th>
        <th style="text-align:right">Packaging</th>
        <th style="text-align:right">Total Cost</th>
        <th style="text-align:right">vs Budget</th>
        <th style="text-align:right">Revenue</th>
        <th style="text-align:right">Gross Margin</th>
        <th style="text-align:right">CPO</th>
      </tr>
    </thead>
    <tbody>
{''.join(row_html(r) for r in rows)}
    </tbody>
    <tfoot>
      <tr>
        <td>MTD TOTAL ({len(rows)}d)</td>
        <td style="text-align:right">{avg_hc:.0f} avg</td>
        <td style="text-align:right">{mtd_vol:,}</td>
        <td style="text-align:right">{php(mtd_labor)}</td>
        <td style="text-align:right">{php(mtd_pkg)}</td>
        <td style="text-align:right">{php(mtd_cost)}</td>
        <td style="text-align:right;color:{'#fca5a5' if budget_var>0 else '#86efac'}">{('+' if budget_var>0 else '')}{php(budget_var)}</td>
        <td style="text-align:right">{php(mtd_rev)}</td>
        <td style="text-align:right;color:#94a3b8">partial</td>
        <td style="text-align:right">{php(mtd_cpo)}</td>
      </tr>
    </tfoot>
  </table>
  <p style="margin-top:10px;font-size:11px;color:#94a3b8">
    * {today_str} is today (partial). Packaging &amp; Revenue for {today_str} pending. Source: Weekly PNL spreadsheet. | Labor = HC × ₱1,167/day | Budget = ₱145,900/day
  </p>

  <!-- ── Trend & Forecast Section ─────────────────────────────────────── -->
  <div style="margin-top:32px">
    <h2 style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#0f172a;margin-bottom:16px">
      📊 Trend Analysis &amp; June Forecast
    </h2>

    <!-- Decision KPIs -->
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin-bottom:20px">
      <div class="kpi" style="border-left:4px solid {'#dc2626' if proj_bvar>0 else '#16a34a'}">
        <div class="lbl">Projected Month-End Cost</div>
        <div class="val" style="font-size:22px">{php(proj_cost_total)}</div>
        <div class="hint">{budget_flag} {'Over' if proj_bvar>0 else 'Under'} budget by {php(abs(proj_bvar))}</div>
      </div>
      <div class="kpi" style="border-left:4px solid #6366f1">
        <div class="lbl">Projected Month-End Revenue</div>
        <div class="val" style="font-size:22px">{php(proj_rev_total)}</div>
        <div class="hint">{'🟢' if proj_margin>=0 else '🔴'} Gross margin {php(proj_margin)}</div>
      </div>
      <div class="kpi" style="border-left:4px solid #f59e0b">
        <div class="lbl">Monthly Budget</div>
        <div class="val" style="font-size:22px">{php(MONTHLY_BUDGET)}</div>
        <div class="hint">{cost_flag} Pace: {cost_pace_pct}% of pro-rated budget</div>
      </div>
      <div class="kpi" style="border-left:4px solid #10b981">
        <div class="lbl">Recommended HC (Jun {int(today_str[8:])+1}–30)</div>
        <div class="val" style="font-size:22px">{rec_hc}</div>
        <div class="hint">To stay within budget · est. {php(rec_hc_cost)}/day</div>
      </div>
      <div class="kpi" style="border-left:4px solid #8b5cf6">
        <div class="lbl">Remaining Budget (Jun {today_str[8:]}–30)</div>
        <div class="val" style="font-size:22px">{php(remaining_budget)}</div>
        <div class="hint">{php(daily_budget_remaining)}/day available · {DAYS_REMAINING} days left</div>
      </div>
      <div class="kpi" style="border-left:4px solid #64748b">
        <div class="lbl">Revenue Coverage</div>
        <div class="val" style="font-size:22px">{rev_cover_pct}%</div>
        <div class="hint">{rev_flag} Cost covered by fulfillment rev</div>
      </div>
    </div>

    <!-- Trend signals -->
    <div class="card" style="margin-bottom:20px;padding:16px 24px">
      <h3 style="margin-bottom:12px">Trend Signals (Jun 1–{complete[-1]['date'][8:]} linear regression)</h3>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;font-size:13px">
        <div><strong>Daily Cost trend:</strong> {cost_trend_dir} &nbsp; <span style="color:#64748b">(slope ₱{cost_slope:+,.0f}/day)</span></div>
        <div><strong>Revenue trend:</strong> {rev_trend_dir} &nbsp; <span style="color:#64748b">(slope ₱{rev_slope:+,.0f}/day)</span></div>
        <div><strong>7-day avg daily cost:</strong> {php(avg7_cost)} &nbsp; <span style="color:#64748b">vs budget ₱{DAILY_BUDGET:,}</span></div>
        <div><strong>7-day avg HC:</strong> {avg7_hc} heads &nbsp; <span style="color:#64748b">avg pkg {php(avg7_pkg)}/day</span></div>
      </div>
    </div>

    <!-- Forecast chart -->
    <div class="card" style="margin-bottom:20px">
      <h3>Full June — Actual vs Forecast Cost &amp; Revenue (₱)</h3>
      <canvas id="forecastChart" height="130"></canvas>
      <p style="font-size:11px;color:#94a3b8;margin-top:8px">
        Forecast = 60% linear regression + 40% 7-day average. Shaded band = ±1 std dev of last 7 days.
        Dashed = forecast period (Jun {int(today_str[8:])+1}–30).
      </p>
    </div>

    <!-- Extended table: actual + forecast rows -->
    <h3 style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#94a3b8;margin-bottom:10px">
      Forecast Detail — Jun {int(today_str[8:])+1}–30
    </h3>
    <table>
      <thead>
        <tr>
          <th>Date</th>
          <th style="text-align:right">HC</th>
          <th style="text-align:right">Orders</th>
          <th style="text-align:right">Labor</th>
          <th style="text-align:right">Packaging</th>
          <th style="text-align:right">Total Cost</th>
          <th style="text-align:right">vs Budget</th>
          <th style="text-align:right">Revenue</th>
          <th style="text-align:right">Gross Margin</th>
          <th style="text-align:right">CPO</th>
        </tr>
      </thead>
      <tbody>
{''.join(fc_row_html(i) for i in range(DAYS_REMAINING))}
      </tbody>
      <tfoot>
        <tr>
          <td>FORECAST TOTAL (14d)</td>
          <td style="text-align:right">{avg7_hc} avg</td>
          <td style="text-align:right">{avg7_vol*DAYS_REMAINING:,}</td>
          <td style="text-align:right">{php(avg7_hc*DAILY_RATE*DAYS_REMAINING)}</td>
          <td style="text-align:right">{php(avg7_pkg*DAYS_REMAINING)}</td>
          <td style="text-align:right">{php(sum(fc_cost))}</td>
          <td style="text-align:right;color:{'#fca5a5' if sum(fc_cost)>DAILY_BUDGET*DAYS_REMAINING else '#86efac'}">{('+' if sum(fc_cost)>DAILY_BUDGET*DAYS_REMAINING else '')}{php(sum(fc_cost)-DAILY_BUDGET*DAYS_REMAINING)}</td>
          <td style="text-align:right">{php(sum(fc_rev))}</td>
          <td style="text-align:right;color:{'#16a34a' if sum(fc_rev)>sum(fc_cost) else '#dc2626'}">{php(sum(fc_rev)-sum(fc_cost))}</td>
          <td style="text-align:right;color:#94a3b8">—</td>
        </tr>
        <tr style="background:#1e293b;color:#fff;font-weight:700">
          <td>JUNE TOTAL (30d)</td>
          <td style="text-align:right">—</td>
          <td style="text-align:right">{mtd_vol + avg7_vol*DAYS_REMAINING:,}</td>
          <td style="text-align:right">—</td>
          <td style="text-align:right">—</td>
          <td style="text-align:right">{php(proj_cost_total)}</td>
          <td style="text-align:right;color:{'#fca5a5' if proj_bvar>0 else '#86efac'}">{('+' if proj_bvar>0 else '')}{php(proj_bvar)}</td>
          <td style="text-align:right">{php(proj_rev_total)}</td>
          <td style="text-align:right;color:{'#86efac' if proj_margin>=0 else '#fca5a5'}">{php(proj_margin)}</td>
          <td style="text-align:right;color:#94a3b8">—</td>
        </tr>
      </tfoot>
    </table>
    <p style="margin-top:8px;font-size:11px;color:#94a3b8">
      * Forecast uses blended model (60% regression + 40% 7-day avg) · HC based on last 7-day average ({avg7_hc}) ·
      Recommended HC to stay within budget: <strong>{rec_hc}</strong> heads/day
    </p>
  </div>

  <!-- Packaging Detail Panel -->
  <div id="pkgPanel" style="display:none;margin-top:28px">
    <h2 style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#6366f1;margin-bottom:14px">
      📦 Packaging Cost — Daily Breakdown by Material
    </h2>

    <!-- Row 1: stacked material chart + MTD totals by material -->
    <div style="display:grid;grid-template-columns:3fr 2fr;gap:16px;margin-bottom:20px">
      <div class="card">
        <h3>Daily Packaging by Material (₱ stacked)</h3>
        <canvas id="pkgMatChart" height="180"></canvas>
      </div>
      <div class="card" style="overflow:auto">
        <h3>MTD Total by Material</h3>
        <table style="box-shadow:none;border-radius:0;margin-top:4px">
          <thead>
            <tr>
              <th>Material</th>
              <th style="text-align:right">MTD Cost</th>
              <th style="text-align:right">Share</th>
              <th style="min-width:80px">Bar</th>
            </tr>
          </thead>
          <tbody>
{mat_summary_rows()}
          </tbody>
          <tfoot>
            <tr>
              <td>TOTAL</td>
              <td style="text-align:right">{php(mtd_pkg)}</td>
              <td style="text-align:right">100%</td>
              <td></td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>

    <!-- Row 2: daily totals table -->
    <h3 style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#94a3b8;margin-bottom:10px">Daily Summary</h3>
    <table>
      <thead>
        <tr>
          <th>Date</th>
          <th style="text-align:right">Packaging Cost</th>
          <th style="text-align:right">% of Total Cost</th>
          <th style="text-align:right">% of Revenue</th>
          <th style="text-align:right">Pkg/Order</th>
          <th>Relative Size</th>
        </tr>
      </thead>
      <tbody>
{''.join(pkg_row_html(r) for r in rows if r["pkg"] is not None)}
      </tbody>
      <tfoot>
        <tr>
          <td>TOTAL (Jun 1–{complete[-1]['date'][8:]})</td>
          <td style="text-align:right">{php(mtd_pkg)}</td>
          <td style="text-align:right">{round(mtd_pkg/mtd_cost*100,1)}%</td>
          <td style="text-align:right">{round(mtd_pkg/mtd_rev*100,1) if mtd_rev>0 else "—"}%</td>
          <td style="text-align:right">—</td>
          <td></td>
        </tr>
      </tfoot>
    </table>
  </div>
</div>

<script>
Chart.defaults.font.family='-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif';
const lbl={lbl}, lab={lab}, pkg_={pkg_}, bud_={bud_}, rev_={rev_}, tc_={tc_};
const pkg_lbl={pkg_lbl}, pkg_vals={pkg_vals}, pkg_pct={pkg_pct};
const mat_lbl={mat_lbl_js}, mat_ds={mat_datasets_js};

// ── Forecast chart ─────────────────────────────────────────────────────────
const fc_lbl={fc_all_lbl_js},
      fc_act_c={fc_act_cost_js}, fc_act_r={fc_act_rev_js},
      fc_proj_c={fc_proj_cost_js}, fc_proj_r={fc_proj_rev_js},
      fc_hi={fc_proj_hi_js}, fc_lo={fc_proj_lo_js},
      fc_bud={fc_budget_js};

new Chart(document.getElementById('forecastChart'),{{
  type:'line',
  data:{{labels:fc_lbl,datasets:[
    {{label:'Actual Cost',data:fc_act_c,borderColor:'rgba(239,68,68,.9)',backgroundColor:'rgba(239,68,68,.12)',
      borderWidth:2.5,pointRadius:3,fill:false,tension:.3,order:2}},
    {{label:'Actual Revenue',data:fc_act_r,borderColor:'rgba(16,185,129,.9)',backgroundColor:'rgba(16,185,129,.08)',
      borderWidth:2.5,pointRadius:3,fill:false,tension:.3,order:3}},
    {{label:'Forecast Cost',data:fc_proj_c,borderColor:'rgba(239,68,68,.6)',borderDash:[6,4],
      borderWidth:2,pointRadius:2,fill:false,tension:.3,order:4}},
    {{label:'Forecast Revenue',data:fc_proj_r,borderColor:'rgba(16,185,129,.6)',borderDash:[6,4],
      borderWidth:2,pointRadius:2,fill:false,tension:.3,order:5}},
    {{label:'Upper band',data:fc_hi,borderColor:'transparent',backgroundColor:'rgba(99,102,241,.08)',
      pointRadius:0,fill:'+1',tension:.3,order:6}},
    {{label:'Lower band',data:fc_lo,borderColor:'transparent',backgroundColor:'rgba(99,102,241,.08)',
      pointRadius:0,fill:false,tension:.3,order:7}},
    {{label:'Daily Budget',data:fc_bud,borderColor:'#f59e0b',borderDash:[4,3],
      borderWidth:1.5,pointRadius:0,fill:false,order:1}},
  ]}},
  options:{{
    responsive:true,
    interaction:{{mode:'index',intersect:false}},
    scales:{{
      y:{{ticks:{{callback:v=>'₱'+(v/1000).toFixed(0)+'k',font:{{size:10}}}}}},
      x:{{ticks:{{font:{{size:9}},maxRotation:45}}}}
    }},
    plugins:{{
      legend:{{position:'top',labels:{{font:{{size:10}},boxWidth:12,filter:i=>i.text!=='Upper band'&&i.text!=='Lower band'}}}},
      tooltip:{{callbacks:{{label:ctx=>ctx.dataset.label+': ₱'+Math.round(ctx.raw||0).toLocaleString()}}}}
    }}
  }}
}});

let pkgMatChartInst=null;
function togglePkg(){{
  const panel=document.getElementById('pkgPanel');
  const arrow=document.getElementById('pkgArrow');
  const open=panel.style.display==='none';
  panel.style.display=open?'block':'none';
  arrow.textContent=open?'▲ Hide':'▼ Details';
  if(open && !pkgMatChartInst){{
    pkgMatChartInst=new Chart(document.getElementById('pkgMatChart'),{{
      type:'bar',
      data:{{labels:mat_lbl,datasets:mat_ds}},
      options:{{
        responsive:true,
        scales:{{
          y:{{stacked:true,ticks:{{callback:v=>'₱'+(v/1000).toFixed(0)+'k',font:{{size:10}}}}}},
          x:{{stacked:true,ticks:{{font:{{size:9}},maxRotation:45}}}}
        }},
        plugins:{{
          legend:{{position:'top',labels:{{font:{{size:10}},boxWidth:10,padding:6}}}},
          tooltip:{{callbacks:{{label:ctx=>' '+ctx.dataset.label+': ₱'+ctx.raw.toLocaleString('en-PH',{{minimumFractionDigits:2}})}}}}
        }}
      }}
    }});
  }}
  if(open) panel.scrollIntoView({{behavior:'smooth',block:'start'}});
}}


new Chart(document.getElementById('costChart'),{{
  type:'bar',
  data:{{labels:lbl,datasets:[
    {{label:'Labor',data:lab,backgroundColor:'rgba(59,130,246,.75)',stack:'c'}},
    {{label:'Packaging',data:pkg_,backgroundColor:'rgba(139,92,246,.75)',stack:'c'}},
    {{label:'Budget',data:bud_,type:'line',borderColor:'#f59e0b',borderWidth:2,pointRadius:0,fill:false,order:0}},
  ]}},
  options:{{
    responsive:true,
    scales:{{
      y:{{stacked:true,ticks:{{callback:v=>'₱'+(v/1000).toFixed(0)+'k',font:{{size:10}}}}}},
      x:{{ticks:{{font:{{size:9}},maxRotation:45}}}}
    }},
    plugins:{{legend:{{position:'top',labels:{{font:{{size:11}},boxWidth:10}}}}}}
  }}
}});

const rev16=rev_.slice(0,{DAYS_WITH_DATA}), tc16=tc_.slice(0,{DAYS_WITH_DATA}), lbl16=lbl.slice(0,{DAYS_WITH_DATA});
new Chart(document.getElementById('revChart'),{{
  type:'bar',
  data:{{labels:lbl16,datasets:[
    {{label:'Revenue',data:rev16,backgroundColor:'rgba(16,185,129,.75)'}},
    {{label:'Total Cost',data:tc16,backgroundColor:'rgba(239,68,68,.65)'}},
  ]}},
  options:{{
    responsive:true,
    scales:{{
      y:{{ticks:{{callback:v=>'₱'+(v/1000).toFixed(0)+'k',font:{{size:10}}}}}},
      x:{{ticks:{{font:{{size:9}},maxRotation:45}}}}
    }},
    plugins:{{legend:{{position:'top',labels:{{font:{{size:11}},boxWidth:10}}}}}}
  }}
}});
</script>
</body>
</html>"""

import pathlib as _pl
with open(_pl.Path(__file__).parent / 'locad-dashboard-latest.html','w') as f:
    f.write(html)
print("Done.")
