import sys
import io
if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')

import json
import os
import re
from datetime import datetime

OUTPUT_FILE   = "dashboard.html"
FINANCE_FILE  = "finance_data.json"
GOLD_LOG_FILE = "gold_price_log.txt"

# ── อ่านข้อมูลรายรับรายจ่าย ───────────────────────────────────────────────────
def อ่านการเงิน():
    if not os.path.exists(FINANCE_FILE):
        return []
    try:
        with open(FINANCE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

# ── อ่านราคาทองล่าสุดจาก log ──────────────────────────────────────────────────
def อ่านราคาทอง():
    if not os.path.exists(GOLD_LOG_FILE):
        return None, None
    try:
        with open(GOLD_LOG_FILE, encoding="utf-8") as f:
            บรรทัด = [l.strip() for l in f if l.strip()]
        if not บรรทัด:
            return None, None
        ล่าสุด = บรรทัด[-1]
        วันที่  = re.match(r"(\d{4}-\d{2}-\d{2})", ล่าสุด)
        ราคา   = re.search(r":\s*([\d,]+)\s*บาท", ล่าสุด)
        return (
            int(ราคา.group(1).replace(",", "")) if ราคา else None,
            วันที่.group(1) if วันที่ else None,
        )
    except IOError:
        return None, None

# ── วิเคราะห์ข้อมูล ───────────────────────────────────────────────────────────
ธุรกรรม  = อ่านการเงิน()
ราคาทอง, วันทอง = อ่านราคาทอง()

รายรับรวม  = sum(t["จำนวนเงิน"] for t in ธุรกรรม if t["ประเภท"] == "รายรับ")
รายจ่ายรวม = sum(t["จำนวนเงิน"] for t in ธุรกรรม if t["ประเภท"] == "รายจ่าย")
ยอดคงเหลือ = รายรับรวม - รายจ่ายรวม

รายจ่ายทั้งหมด = sorted(
    [t for t in ธุรกรรม if t["ประเภท"] == "รายจ่าย"],
    key=lambda t: t["จำนวนเงิน"], reverse=True
)
top3 = รายจ่ายทั้งหมด[:3]

# ── Chart data ────────────────────────────────────────────────────────────────
ชื่อธุรกรรม    = json.dumps([t["คำอธิบาย"] for t in ธุรกรรม], ensure_ascii=False)
จำนวนธุรกรรม  = json.dumps([t["จำนวนเงิน"] for t in ธุรกรรม])
สีธุรกรรม     = json.dumps(["#34d399" if t["ประเภท"] == "รายรับ" else "#f87171" for t in ธุรกรรม])

# ── helpers ────────────────────────────────────────────────────────────────────
def การ์ดสถิติ(ไอคอน, หัวข้อ, ค่า, หน่วย, สี, เพิ่มเติม=""):
    return f"""
    <div class="stat-card">
      <div class="stat-icon" style="color:{สี}">{ไอคอน}</div>
      <div class="stat-label">{หัวข้อ}</div>
      <div class="stat-value" style="color:{สี}">{ค่า}</div>
      <div class="stat-unit">{หน่วย} {เพิ่มเติม}</div>
    </div>"""

def แถวรายจ่าย(อันดับ, ธุรกรรม, สูงสุด):
    pct = (ธุรกรรม["จำนวนเงิน"] / สูงสุด * 100) if สูงสุด else 0
    return f"""
    <div class="expense-row">
      <div class="expense-rank">{อันดับ}</div>
      <div class="expense-info">
        <div class="expense-name">{ธุรกรรม['คำอธิบาย']}</div>
        <div class="expense-bar-wrap">
          <div class="expense-bar" style="width:{pct:.0f}%"></div>
        </div>
      </div>
      <div class="expense-amount">฿{ธุรกรรม['จำนวนเงิน']:,.0f}</div>
    </div>"""

def แถวธุรกรรม(t):
    สี   = "#34d399" if t["ประเภท"] == "รายรับ" else "#f87171"
    เครื่องหมาย = "+" if t["ประเภท"] == "รายรับ" else "−"
    return f"""
    <tr>
      <td>{t['วันที่']}</td>
      <td>{t['คำอธิบาย']}</td>
      <td><span class="badge" style="background:{สี}22;color:{สี}">{t['ประเภท']}</span></td>
      <td style="text-align:right;color:{สี};font-weight:600">{เครื่องหมาย}฿{t['จำนวนเงิน']:,.0f}</td>
    </tr>"""

สีคงเหลือ = "#34d399" if ยอดคงเหลือ >= 0 else "#f87171"
สูงสุด = top3[0]["จำนวนเงิน"] if top3 else 1
ราคาทองข้อความ = f"{ราคาทอง:,}" if ราคาทอง else "—"
วันทองข้อความ  = f"ข้อมูลวันที่ {วันทอง}" if วันทอง else "ยังไม่มีข้อมูล"
แถวธุรกรรมทั้งหมด = "".join(แถวธุรกรรม(t) for t in reversed(ธุรกรรม))
แถวจ่ายทั้งหมด    = "".join(แถวรายจ่าย(i+1, t, สูงสุด) for i, t in enumerate(top3)) or \
                    '<p style="color:#64748b;padding:16px 0">ยังไม่มีรายจ่าย</p>'

# ── HTML ──────────────────────────────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Dashboard ส่วนตัว</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <style>
    :root {{
      --bg:      #0f172a;
      --surface: #1e293b;
      --surface2:#273549;
      --border:  #334155;
      --text:    #e2e8f0;
      --muted:   #64748b;
      --blue:    #3b82f6;
      --green:   #34d399;
      --red:     #f87171;
      --gold:    #fbbf24;
    }}
    * {{ box-sizing:border-box; margin:0; padding:0 }}
    body {{ background:var(--bg); color:var(--text); font-family:'Segoe UI',sans-serif; min-height:100vh }}

    /* HEADER */
    header {{ background:linear-gradient(135deg,#0f172a,#1e3a8a 80%); padding:0 32px; border-bottom:1px solid var(--border) }}
    .header-inner {{ max-width:1200px; margin:0 auto; padding:20px 0; display:flex; justify-content:space-between; align-items:center }}
    .header-title {{ font-size:1.4em; font-weight:700; letter-spacing:.02em }}
    .header-title span {{ color:var(--blue) }}
    .header-meta {{ font-size:.82em; color:var(--muted); text-align:right }}

    /* LAYOUT */
    main {{ max-width:1200px; margin:0 auto; padding:28px 24px }}

    /* STAT CARDS */
    .stats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:16px; margin-bottom:28px }}
    .stat-card {{ background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:22px 24px }}
    .stat-icon {{ font-size:1.5em; margin-bottom:8px }}
    .stat-label {{ font-size:.78em; color:var(--muted); margin-bottom:6px; text-transform:uppercase; letter-spacing:.06em }}
    .stat-value {{ font-size:1.8em; font-weight:700; line-height:1 }}
    .stat-unit {{ font-size:.8em; color:var(--muted); margin-top:4px }}

    /* GRID 2 คอลัมน์ */
    .grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:28px }}
    @media(max-width:700px){{ .grid2{{ grid-template-columns:1fr }} }}

    /* CARD */
    .card {{ background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:24px }}
    .card-title {{ font-size:.85em; font-weight:600; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; margin-bottom:20px }}

    /* TOP EXPENSES */
    .expense-row {{ display:flex; align-items:center; gap:12px; margin-bottom:16px }}
    .expense-rank {{ width:24px; height:24px; border-radius:50%; background:var(--surface2); color:var(--muted); font-size:.78em; font-weight:700; display:grid; place-items:center; flex-shrink:0 }}
    .expense-info {{ flex:1 }}
    .expense-name {{ font-size:.9em; margin-bottom:6px }}
    .expense-bar-wrap {{ background:var(--surface2); border-radius:99px; height:6px }}
    .expense-bar {{ background:var(--red); height:6px; border-radius:99px; transition:width .4s }}
    .expense-amount {{ font-size:.9em; font-weight:600; color:var(--red); white-space:nowrap }}

    /* TABLE */
    table {{ width:100%; border-collapse:collapse; font-size:.88em }}
    th {{ text-align:left; padding:10px 12px; color:var(--muted); font-weight:600; font-size:.8em; text-transform:uppercase; letter-spacing:.05em; border-bottom:1px solid var(--border) }}
    td {{ padding:11px 12px; border-bottom:1px solid #1e293b; vertical-align:middle }}
    tr:last-child td {{ border-bottom:none }}
    tr:hover td {{ background:var(--surface2) }}
    .badge {{ padding:2px 10px; border-radius:99px; font-size:.78em; font-weight:600 }}

    /* FOOTER */
    footer {{ text-align:center; padding:20px; font-size:.78em; color:var(--muted); border-top:1px solid var(--border); margin-top:8px }}

    @keyframes pulse {{
      0%,100% {{ opacity:1; transform:scale(1) }}
      50%      {{ opacity:.4; transform:scale(1.4) }}
    }}
  </style>
</head>
<body>

<header>
  <div class="header-inner">
    <div>
      <div class="header-title">&#9685; Dashboard <span>ส่วนตัว</span></div>
      <div style="font-size:.8em;color:var(--muted);margin-top:2px">ภาพรวมการเงินและข้อมูลทรัพย์สิน</div>
    </div>
    <div class="header-meta">
      <div style="color:var(--text);font-weight:600">{datetime.now().strftime('%d %B %Y')}</div>
      <div>อัปเดตล่าสุด <span id="last-updated">{datetime.now().strftime('%H:%M:%S')} น.</span></div>
      <div style="margin-top:4px">
        <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#34d399;margin-right:4px;animation:pulse 2s infinite"></span>
        รีเฟรชในอีก <span id="countdown" style="color:#34d399;font-weight:700">60</span> วินาที
      </div>
    </div>
  </div>
</header>

<main>

  <!-- Stat Cards -->
  <div class="stats">
    {การ์ดสถิติ("💳","ยอดคงเหลือ",f"{ยอดคงเหลือ:,.0f}","บาท",สีคงเหลือ)}
    {การ์ดสถิติ("📈","รายรับรวม",f"{รายรับรวม:,.0f}","บาท","#34d399")}
    {การ์ดสถิติ("📉","รายจ่ายรวม",f"{รายจ่ายรวม:,.0f}","บาท","#f87171")}
    {การ์ดสถิติ("🥇","ราคาทองแท่ง",ราคาทองข้อความ,"บาท / บาทหนัก","#fbbf24",f'<br><span style="font-size:.85em">{วันทองข้อความ}</span>')}
  </div>

  <!-- Top 3 + Chart -->
  <div class="grid2">

    <div class="card">
      <div class="card-title">รายจ่ายสูงสุด 3 อันดับ</div>
      {แถวจ่ายทั้งหมด}
    </div>

    <div class="card">
      <div class="card-title">สัดส่วนรายรับ vs รายจ่าย</div>
      <div style="position:relative;height:220px;display:flex;justify-content:center">
        <canvas id="donutChart"></canvas>
      </div>
      <div style="display:flex;gap:20px;justify-content:center;margin-top:16px;font-size:.8em;color:var(--muted)">
        <span><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#34d399;margin-right:4px"></span>รายรับ</span>
        <span><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#f87171;margin-right:4px"></span>รายจ่าย</span>
      </div>
    </div>

  </div>

  <!-- กราฟรายรับรายจ่าย -->
  <div class="card" style="margin-bottom:28px">
    <div class="card-title">รายรับ / รายจ่ายแต่ละรายการ</div>
    <div style="position:relative;height:220px">
      <canvas id="barChart"></canvas>
    </div>
  </div>

  <!-- ตารางธุรกรรม -->
  <div class="card">
    <div class="card-title">ธุรกรรมทั้งหมด ({len(ธุรกรรม)} รายการ)</div>
    <table>
      <thead><tr>
        <th>วันที่</th><th>รายการ</th><th>ประเภท</th><th style="text-align:right">จำนวน</th>
      </tr></thead>
      <tbody>{แถวธุรกรรมทั้งหมด}</tbody>
    </table>
  </div>

</main>

<footer>Dashboard ส่วนตัว &nbsp;·&nbsp; สร้างโดย dashboard.py &nbsp;·&nbsp; อัปเดตล่าสุด {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} น. &nbsp;·&nbsp; รีเฟรชอัตโนมัติทุก 60 วินาที</footer>

<script>
// ── Auto-refresh countdown ─────────────────────────────────────────────────
(function() {{
  const INTERVAL = 60;
  let remaining = INTERVAL;
  const el = document.getElementById('countdown');
  setInterval(() => {{
    remaining -= 1;
    if (el) el.textContent = remaining;
    if (remaining <= 0) location.reload();
  }}, 1000);
}})();

Chart.defaults.color = '#64748b';
Chart.defaults.borderColor = '#334155';

// Donut chart
new Chart(document.getElementById('donutChart'), {{
  type: 'doughnut',
  data: {{
    labels: ['รายรับ', 'รายจ่าย'],
    datasets: [{{ data: [{รายรับรวม}, {รายจ่ายรวม}], backgroundColor: ['#34d399','#f87171'], borderWidth: 0, hoverOffset: 6 }}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false, cutout: '68%',
    plugins: {{
      legend: {{ display: false }},
      tooltip: {{ callbacks: {{ label: c => ` ฿${{c.parsed.toLocaleString()}}` }} }}
    }}
  }}
}});

// Bar chart
new Chart(document.getElementById('barChart'), {{
  type: 'bar',
  data: {{
    labels: {ชื่อธุรกรรม},
    datasets: [{{
      label: 'จำนวนเงิน',
      data: {จำนวนธุรกรรม},
      backgroundColor: {สีธุรกรรม},
      borderRadius: 6, borderSkipped: false,
    }}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    plugins: {{
      legend: {{ display: false }},
      tooltip: {{ callbacks: {{ label: c => ` ฿${{c.parsed.y.toLocaleString()}}` }} }}
    }},
    scales: {{
      x: {{ grid: {{ display: false }}, ticks: {{ font: {{ size: 11 }} }} }},
      y: {{ grid: {{ color: '#1e293b' }}, ticks: {{ callback: v => '฿' + v.toLocaleString(), font: {{ size: 11 }} }} }}
    }}
  }}
}});
</script>
</body></html>"""

# ── บันทึกไฟล์ ────────────────────────────────────────────────────────────────
try:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"สร้าง {OUTPUT_FILE} เรียบร้อย")
except PermissionError:
    print(f"ไม่สามารถบันทึก {OUTPUT_FILE} — ไฟล์อาจถูกเปิดอยู่ในเบราว์เซอร์")
