from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from energy_analytics.config import load_config
from energy_analytics.metadata import log_metadata


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _metric_map(rows: list[dict[str, str]]) -> dict[str, float]:
    out: dict[str, float] = {}
    for row in rows:
        out[row["metric"]] = float(row["value"])
    return out


def _scenario_index(rows: list[dict[str, str]]) -> dict[str, dict[str, float]]:
    idx: dict[str, dict[str, float]] = {}
    for row in rows:
        contract_type = row.get("contract_type", "contracted")
        key = f"{contract_type}|{row['price_case']}|{row['capex_case']}"
        idx[key] = {
            "npv_musd": float(row["npv_musd"]),
            "after_tax_npv_musd": float(row.get("after_tax_npv_musd", row["npv_musd"])),
            "irr": float(row["irr"]),
            "min_dscr": float(row["min_dscr"]),
            "avg_dscr": float(row["avg_dscr"]),
            "lcoe_usd_mwh": float(row["lcoe_usd_mwh"]),
            "year1_revenue_musd": float(row["year1_revenue_musd"]),
        }
    return idx


def _build_summary_report(cfg: dict[str, Any], metrics: dict[str, float], base_fin: dict[str, float]) -> Path:
    report_path = Path("reports/dashboard/summary_report.html")
    report_path.parent.mkdir(parents=True, exist_ok=True)

    html = f"""<!doctype html>
<html lang='en'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width,initial-scale=1'>
  <title>Energy Analytics Summary Report</title>
  <style>
    body {{ font-family: 'IBM Plex Sans','Segoe UI',sans-serif; margin: 24px; color:#102027; }}
    h1,h2 {{ margin: 0 0 10px; }}
    .meta {{ color:#425a65; margin-bottom: 18px; }}
    .card {{ border:1px solid #d8e1e5; border-radius:10px; padding:12px 14px; margin:10px 0; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th,td {{ border:1px solid #d8e1e5; padding:8px; text-align:left; }}
    th {{ background:#eef3f5; }}
  </style>
</head>
<body>
  <h1>Energy Analytics Portfolio Summary</h1>
  <div class='meta'>Region: {cfg['region']} | Hub: {cfg['hub']} | Generated from processed artifacts only.</div>

  <h2>Market Highlights</h2>
  <div class='card'>Average hub price: <b>{metrics.get('avg_price_usd_mwh', 0.0):.2f} USD/MWh</b></div>
  <div class='card'>Solar capture price: <b>{metrics.get('solar_capture_price_usd_mwh', 0.0):.2f} USD/MWh</b> | Wind capture price: <b>{metrics.get('wind_capture_price_usd_mwh', 0.0):.2f} USD/MWh</b></div>
  <div class='card'>Congestion proxy mean: <b>{metrics.get('congestion_proxy_mean', 0.0):.2f} USD/MWh</b> | Negative price share: <b>{100*metrics.get('negative_price_share', 0.0):.1f}%</b></div>

  <h2>Base Solar Finance Case</h2>
  <table>
    <tr><th>Metric</th><th>Value</th></tr>
    <tr><td>NPV (MUSD)</td><td>{base_fin['npv_musd']:.2f}</td></tr>
    <tr><td>After-tax NPV (MUSD)</td><td>{base_fin.get('after_tax_npv_musd', base_fin['npv_musd']):.2f}</td></tr>
    <tr><td>IRR</td><td>{base_fin['irr']:.3f}</td></tr>
    <tr><td>Min DSCR</td><td>{base_fin['min_dscr']:.3f}</td></tr>
    <tr><td>LCOE (USD/MWh)</td><td>{base_fin['lcoe_usd_mwh']:.2f}</td></tr>
    <tr><td>Year 1 Revenue (MUSD)</td><td>{base_fin['year1_revenue_musd']:.2f}</td></tr>
  </table>

  <h2>Limitations</h2>
  <ul>
    <li>Uses sample data and stylized renewable generation profiles.</li>
    <li>Congestion is proxy-based, not a transmission power-flow model.</li>
    <li>Finance assumptions are centralized and scenario-based, not an investment recommendation.</li>
  </ul>
</body>
</html>
"""
    report_path.write_text(html, encoding="utf-8")
    return report_path


def run_dashboard() -> None:
    cfg = load_config()
    panel_rows = _read_csv(Path(cfg["curated_output"]["panel_csv"]))
    queue_rows = _read_csv(Path(cfg["curated_output"]["queue_outlook_csv"]))
    market_metrics = _metric_map(_read_csv(Path(cfg["markets_output"]["metrics_csv"])))
    finance_rows = _read_csv(Path(cfg["finance_output"]["scenarios_csv"]))
    scenario_idx = _scenario_index(finance_rows)

    out_dir = Path("reports/dashboard")
    out_dir.mkdir(parents=True, exist_ok=True)
    dashboard_path = out_dir / "index.html"

    load_points = [float(r["load_mw"]) for r in panel_rows]
    price_points = [float(r["price_usd_mwh"]) for r in panel_rows]
    temp_points = [float(r["temperature_f"]) for r in panel_rows]

    queue_by_year: dict[str, dict[str, float]] = {}
    for r in queue_rows:
        y = r["year"]
        if y not in queue_by_year:
            queue_by_year[y] = {"p50": 0.0, "p90": 0.0}
        queue_by_year[y]["p50"] += float(r["expected_online_mw_p50"])
        queue_by_year[y]["p90"] += float(r["expected_online_mw_p90"])

    years = sorted(queue_by_year.keys())
    queue_p50 = [queue_by_year[y]["p50"] for y in years]
    queue_p90 = [queue_by_year[y]["p90"] for y in years]

    base_fin = scenario_idx["contracted|base|base"]
    summary_report_path = _build_summary_report(cfg, market_metrics, base_fin)

    embedded = {
        "region": cfg["region"],
        "hub": cfg["hub"],
        "kpis": {
            "avg_price": market_metrics.get("avg_price_usd_mwh", 0.0),
            "solar_capture": market_metrics.get("solar_capture_price_usd_mwh", 0.0),
            "wind_capture": market_metrics.get("wind_capture_price_usd_mwh", 0.0),
            "congestion_mean": market_metrics.get("congestion_proxy_mean", 0.0),
            "negative_share": market_metrics.get("negative_price_share", 0.0),
            "base_npv": base_fin["npv_musd"],
            "base_irr": base_fin["irr"],
        },
        "series": {
            "load": load_points,
            "price": price_points,
            "temperature": temp_points,
            "years": years,
            "queue_p50": queue_p50,
            "queue_p90": queue_p90,
        },
        "finance_scenarios": scenario_idx,
    }

    html = f"""<!doctype html>
<html lang='en'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width,initial-scale=1'>
  <title>Energy Analytics Dashboard</title>
  <style>
    :root {{
      --ink:#0f1f24;
      --muted:#5b727c;
      --accent:#0b5f83;
      --accent2:#b55000;
      --bg:#f5f8f9;
      --card:#ffffff;
      --line:#d9e2e7;
    }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:linear-gradient(130deg,#eef4f7,#f8fbfc); color:var(--ink); font-family:'IBM Plex Sans','Segoe UI',sans-serif; }}
    header {{ padding:16px 20px; border-bottom:1px solid var(--line); background:rgba(255,255,255,.9); position:sticky; top:0; z-index:10; backdrop-filter: blur(4px); }}
    h1 {{ margin:0; font-size:20px; }}
    .sub {{ color:var(--muted); font-size:13px; margin-top:4px; }}
    .layout {{ display:grid; grid-template-columns:280px 1fr; min-height:calc(100vh - 74px); }}
    .side {{ border-right:1px solid var(--line); padding:14px; background:#fbfdfe; }}
    .main {{ padding:18px; }}
    .card {{ background:var(--card); border:1px solid var(--line); border-radius:12px; padding:12px; margin-bottom:12px; }}
    label {{ display:block; font-size:12px; color:var(--muted); margin:8px 0 4px; }}
    select,input {{ width:100%; padding:8px; border:1px solid #c9d6dd; border-radius:8px; }}
    .tabs {{ display:flex; flex-wrap:wrap; gap:6px; margin-bottom:10px; }}
    .tab-btn {{ border:1px solid #c8d5dd; background:#fff; padding:7px 10px; border-radius:999px; font-size:12px; cursor:pointer; }}
    .tab-btn.active {{ background:var(--accent); color:#fff; border-color:var(--accent); }}
    .tab {{ display:none; }}
    .tab.active {{ display:block; }}
    .grid3 {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px; }}
    .kpi {{ background:#fff; border:1px solid var(--line); border-radius:12px; padding:12px; }}
    .kpi .v {{ font-size:22px; font-weight:700; margin:6px 0 2px; }}
    .m {{ color:var(--muted); font-size:12px; }}
    .chart {{ width:100%; border:1px solid var(--line); border-radius:10px; background:#fff; padding:6px; }}
    details {{ margin-top:6px; }}
    .foot {{ color:var(--muted); font-size:12px; margin-top:12px; }}
    .dl a {{ display:block; margin:4px 0; color:#0a4f6f; text-decoration:none; }}
    @media (max-width:900px) {{ .layout{{grid-template-columns:1fr;}} .side{{border-right:0;border-bottom:1px solid var(--line);}} .grid3{{grid-template-columns:1fr;}} }}
  </style>
</head>
<body>
<header>
  <h1>Energy Analytics Dashboard</h1>
  <div class='sub'>Processed-data dashboard for {cfg['region']} ({cfg['hub']}) covering milestones 1-5.</div>
</header>
<div class='layout'>
  <aside class='side'>
    <div class='card'>
      <b>Scenario Controls</b>
      <label title='Select market region/zone for all pages.'>Region selector</label>
      <select id='region'><option>{cfg['region']}</option></select>
      <label title='Load scenario multiplier for KPI projections.'>Load scenario</label>
      <select id='load_scn'><option value='0.95'>Low</option><option value='1.0' selected>Base</option><option value='1.07'>High</option></select>
      <label title='Queue completion assumption used in supply KPIs.'>Queue completion</label>
      <select id='queue_scn'><option value='p50' selected>P50</option><option value='p90'>P90</option></select>
      <label title='Market tightness modifies implied congestion assumptions.'>Market tightness</label>
      <select id='tight_scn'><option value='0.85'>Low congestion</option><option value='1.0' selected>Base</option><option value='1.25'>High congestion</option></select>
    </div>
    <div class='card'>
      <b>Finance Knobs</b>
      <label title='Installed cost per kW.'>Capex (USD/kW)</label>
      <input id='capex' type='number' value='{cfg['finance_assumptions']['capex_per_kw']}' step='25'>
      <label title='Fixed annual operating cost per kW.'>Opex (USD/kW-yr)</label>
      <input id='opex' type='number' value='{cfg['finance_assumptions']['fixed_opex_per_kw_year']}' step='1'>
      <label title='Discount rate proxy for weighted average cost of capital.'>WACC</label>
      <input id='wacc' type='number' value='{cfg['finance_assumptions']['equity_discount_rate']}' step='0.005'>
      <label title='Debt interest rate assumption.'>Debt rate</label>
      <input id='debt' type='number' value='{cfg['finance_assumptions']['debt_rate']}' step='0.005'>
      <label title='Revenue structure for the project case.'>Contract type</label>
      <select id='contract_type'><option value='contracted' selected>Contracted</option><option value='merchant'>Merchant</option></select>
      <label title='Power purchase agreement proxy price.'>PPA price (USD/MWh)</label>
      <input id='ppa' type='number' value='{market_metrics.get('solar_capture_price_usd_mwh',0.0):.2f}' step='0.5'>
      <label title='Annual energy degradation assumption.'>Degradation</label>
      <input id='degrade' type='number' value='{cfg['finance_assumptions']['degradation_rate']}' step='0.001'>
    </div>
  </aside>
  <main class='main'>
    <div class='tabs'>
      <button class='tab-btn active' data-tab='overview'>Overview</button>
      <button class='tab-btn' data-tab='load'>Load</button>
      <button class='tab-btn' data-tab='supply'>Supply</button>
      <button class='tab-btn' data-tab='markets'>Markets</button>
      <button class='tab-btn' data-tab='finance'>Finance</button>
      <button class='tab-btn' data-tab='downloads'>Downloads</button>
    </div>

    <section id='overview' class='tab active'>
      <div class='grid3'>
        <div class='kpi'><div class='m'>Average Price (USD/MWh)</div><div class='v' id='k_avg_price'>-</div></div>
        <div class='kpi'><div class='m'>Solar Capture (USD/MWh)</div><div class='v' id='k_solar'>-</div></div>
        <div class='kpi'><div class='m'>Base NPV (MUSD)</div><div class='v' id='k_npv'>-</div></div>
      </div>
      <div class='foot'>Definitions: capture price = profile-weighted average price; congestion proxy = absolute deviation from 24h moving-average price.</div>
    </section>

    <section id='load' class='tab'>
      <h3>Load and Weather</h3>
      <img class='chart' src='../charts/ercot_load.svg' alt='Hourly load chart (MW)'>
      <img class='chart' src='../charts/ercot_temperature.svg' alt='Hourly temperature chart (F)'>
      <img class='chart' src='../charts/ercot_load_forecast_scenarios.svg' alt='Load forecast scenarios chart (avg MW)'>
      <div class='foot'>Units: MW for load, F for temperature.</div>
    </section>

    <section id='supply' class='tab'>
      <h3>Supply Queue Outlook</h3>
      <img class='chart' src='../charts/ercot_queue_expected_online_mw.svg' alt='Queue expected online MW by year'>
      <div class='kpi'><div class='m'>Selected Queue Scenario Total (MW)</div><div class='v' id='k_queue_total'>-</div></div>
      <div class='foot'>P50/P90 represent expected online capacity under different completion assumptions.</div>
    </section>

    <section id='markets' class='tab'>
      <h3>Market Metrics</h3>
      <img class='chart' src='../charts/ercot_price.svg' alt='Hub price chart (USD/MWh)'>
      <div class='grid3'>
        <div class='kpi'><div class='m'>Wind Capture (USD/MWh)</div><div class='v' id='k_wind'>-</div></div>
        <div class='kpi'><div class='m'>Congestion Mean (USD/MWh)</div><div class='v' id='k_cong'>-</div></div>
        <div class='kpi'><div class='m'>Negative Price Share (%)</div><div class='v' id='k_neg'>-</div></div>
      </div>
      <details><summary>Metric Notes</summary><div class='foot'>Negative price share = hours with price < 0 divided by total hours in modeled period.</div></details>
    </section>

    <section id='finance' class='tab'>
      <h3>Project Finance</h3>
      <div class='grid3'>
        <div class='kpi'><div class='m'>Scenario IRR</div><div class='v' id='k_irr'>-</div></div>
        <div class='kpi'><div class='m'>Min DSCR</div><div class='v' id='k_dscr'>-</div></div>
        <div class='kpi'><div class='m'>LCOE (USD/MWh)</div><div class='v' id='k_lcoe'>-</div></div>
      </div>
      <img class='chart' src='../charts/ercot_finance_sensitivity.svg' alt='Finance sensitivity chart'>
      <div class='foot'>Finance KPIs are scenario-linked to price/capex controls and provide directional screening outputs.</div>
    </section>

    <section id='downloads' class='tab'>
      <h3>Downloads and Report</h3>
      <div class='dl'>
        <a href='../../data/marts/ercot_market_metrics.csv' download>Download market metrics CSV</a>
        <a href='../../data/marts/ercot_load_backtest.csv' download>Download load backtest CSV</a>
        <a href='../../data/marts/ercot_load_forecast_scenarios.csv' download>Download load scenarios CSV</a>
        <a href='../../data/marts/ercot_finance_scenarios.csv' download>Download finance scenarios CSV</a>
        <a href='../../data/marts/ercot_finance_sensitivity.csv' download>Download finance sensitivity CSV</a>
        <a href='../../data/marts/ercot_queue_calibration.csv' download>Download queue calibration CSV</a>
        <a href='../../data/curated/ercot_queue_expected_online_mw.csv' download>Download queue outlook CSV</a>
        <a href='summary_report.html' target='_blank'>Open auto-generated summary report</a>
      </div>
      <div class='foot'>Dashboard runtime uses processed tables only and does not fetch external data.</div>
    </section>
  </main>
</div>

<script>
const DATA = {json.dumps(embedded)};

function fmt(n, d=2) {{ return Number(n).toFixed(d); }}
function scenarioKeyFromControls() {{
  const price = document.getElementById('tight_scn').value;
  const contractType = document.getElementById('contract_type').value;
  const capex = Number(document.getElementById('capex').value);
  const baseCapex = {cfg['finance_assumptions']['capex_per_kw']};
  let priceCase = 'base';
  if (Number(price) < 1) priceCase = 'low';
  if (Number(price) > 1) priceCase = 'high';
  let capexCase = 'base';
  if (capex < baseCapex) capexCase = 'low';
  if (capex > baseCapex) capexCase = 'high';
  return contractType + '|' + priceCase + '|' + capexCase;
}}

function refresh() {{
  const loadMult = Number(document.getElementById('load_scn').value);
  const tightMult = Number(document.getElementById('tight_scn').value);
  const queueMode = document.getElementById('queue_scn').value;

  const avgPrice = DATA.kpis.avg_price * tightMult;
  const solar = DATA.kpis.solar_capture * tightMult;
  const wind = DATA.kpis.wind_capture * tightMult;
  const cong = DATA.kpis.congestion_mean * tightMult;
  const neg = Math.min(DATA.kpis.negative_share * tightMult, 1);

  document.getElementById('k_avg_price').textContent = fmt(avgPrice);
  document.getElementById('k_solar').textContent = fmt(solar);
  document.getElementById('k_wind').textContent = fmt(wind);
  document.getElementById('k_cong').textContent = fmt(cong);
  document.getElementById('k_neg').textContent = fmt(neg * 100, 1);

  const qArr = queueMode === 'p50' ? DATA.series.queue_p50 : DATA.series.queue_p90;
  const qTotal = qArr.reduce((a,b)=>a+b,0) * loadMult;
  document.getElementById('k_queue_total').textContent = fmt(qTotal, 1);

  const key = scenarioKeyFromControls();
  const s = DATA.finance_scenarios[key] || DATA.finance_scenarios['contracted|base|base'];
  document.getElementById('k_npv').textContent = fmt(s.npv_musd, 2);
  document.getElementById('k_irr').textContent = fmt(s.irr, 3);
  document.getElementById('k_dscr').textContent = fmt(s.min_dscr, 2);
  document.getElementById('k_lcoe').textContent = fmt(s.lcoe_usd_mwh, 2);
}}

for (const btn of document.querySelectorAll('.tab-btn')) {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(s => s.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(btn.dataset.tab).classList.add('active');
  }});
}}

for (const id of ['load_scn','queue_scn','tight_scn','contract_type','capex','opex','wacc','debt','ppa','degrade']) {{
  document.getElementById(id).addEventListener('input', refresh);
}}
refresh();
</script>
</body>
</html>
"""

    dashboard_path.write_text(html, encoding="utf-8")
    log_metadata(
        cfg["reports"]["metadata_log"],
        f"dashboard:generated dashboard={dashboard_path} summary={summary_report_path}",
    )


if __name__ == "__main__":
    run_dashboard()
