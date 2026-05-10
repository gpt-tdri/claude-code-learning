import sys
import io
if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')

import csv
import sys
from datetime import date, datetime

INPUT_FILE  = "research_data.csv"
OUTPUT_FILE = "daily_report.html"
วันนี้ = date.today()

# ── อ่าน CSV ──────────────────────────────────────────────────────────────────
try:
    โครงการ = []
    with open(INPUT_FILE, encoding="utf-8") as f:
        for แถว in csv.DictReader(f):
            try:
                โครงการ.append({
                    "ชื่อ":     แถว["ชื่อโครงการ"],
                    "งบ":       int(แถว["งบประมาณ"]),
                    "คืบหน้า":  int(แถว["ความคืบหน้า(%)"]),
                    "เริ่ม":    date.fromisoformat(แถว["วันเริ่มต้น"]),
                    "สิ้นสุด":  date.fromisoformat(แถว["วันสิ้นสุด"]),
                    "สถานะ":    แถว["สถานะ"],
                })
            except (ValueError, KeyError) as e:
                print(f"คำเตือน: ข้ามแถว '{แถว.get('ชื่อโครงการ','?')}' — {e}")
except FileNotFoundError:
    print(f"ไม่พบไฟล์ {INPUT_FILE}")
    sys.exit(1)

if not โครงการ:
    print("ไม่มีข้อมูลโครงการ")
    sys.exit(1)

# ── วิเคราะห์ข้อมูล ───────────────────────────────────────────────────────────
นับสถานะ   = {}
งบตามสถานะ = {}
for ป in โครงการ:
    ส = ป["สถานะ"]
    นับสถานะ[ส]   = นับสถานะ.get(ส, 0) + 1
    งบตามสถานะ[ส] = งบตามสถานะ.get(ส, 0) + ป["งบ"]

งบรวม       = sum(ป["งบ"] for ป in โครงการ)
ล่าช้า      = [ป for ป in โครงการ if ป["สถานะ"] == "ล่าช้า"]
ใกล้หมดเวลา = [ป for ป in โครงการ if ป["คืบหน้า"] < 50 and (ป["สิ้นสุด"] - วันนี้).days <= 180]

# ── helpers ────────────────────────────────────────────────────────────────────
สีสถานะ = {"เสร็จแล้ว": "#10b981", "กำลังดำเนินการ": "#3b82f6", "ล่าช้า": "#ef4444"}
ไอคอนสถานะ = {"เสร็จแล้ว": "✓", "กำลังดำเนินการ": "▶", "ล่าช้า": "!"}

def สีแถบ(pct):
    return "#10b981" if pct >= 75 else "#f59e0b" if pct >= 40 else "#ef4444"

def แถบคืบหน้า(pct):
    สี = สีแถบ(pct)
    return f"""
      <div style="display:flex;align-items:center;gap:8px">
        <div style="flex:1;background:#e2e8f0;border-radius:99px;height:8px;overflow:hidden">
          <div style="background:{สี};width:{pct}%;height:100%;border-radius:99px;transition:width .3s"></div>
        </div>
        <span style="font-size:.8em;font-weight:600;color:{สี};min-width:32px">{pct}%</span>
      </div>"""

def ป้ายสถานะ(ส):
    สี = สีสถานะ.get(ส, "#6b7280")
    ไอคอน = ไอคอนสถานะ.get(ส, "•")
    return f'<span style="display:inline-flex;align-items:center;gap:4px;background:{สี}18;color:{สี};border:1px solid {สี}44;padding:3px 10px;border-radius:99px;font-size:.78em;font-weight:600">{ไอคอน} {ส}</span>'

def เหลือกี่วัน(ป):
    วัน = (ป["สิ้นสุด"] - วันนี้).days
    if วัน < 0:
        return f'<span style="color:#ef4444;font-weight:600">เลยกำหนด {abs(วัน)} วัน</span>'
    if วัน <= 30:
        return f'<span style="color:#f59e0b;font-weight:600">⚠ {วัน} วัน</span>'
    return f'<span style="color:#64748b">{วัน} วัน</span>'

def แถวตาราง(ป):
    return f"""
    <tr class="row">
      <td style="font-weight:500;color:#1e293b">{ป['ชื่อ']}</td>
      <td style="text-align:right;font-variant-numeric:tabular-nums">{ป['งบ']:,}</td>
      <td style="min-width:160px">{แถบคืบหน้า(ป['คืบหน้า'])}</td>
      <td style="color:#64748b;font-size:.9em">{ป['เริ่ม']}</td>
      <td style="color:#64748b;font-size:.9em">{ป['สิ้นสุด']}</td>
      <td>{เหลือกี่วัน(ป)}</td>
      <td>{ป้ายสถานะ(ป['สถานะ'])}</td>
    </tr>"""

def การ์ด(ไอคอน, หัวข้อ, ค่า, หน่วย, สี, bg):
    return f"""
    <div style="background:white;border-radius:12px;padding:20px 24px;box-shadow:0 1px 4px #1e3a8a18;border-top:4px solid {สี}">
      <div style="font-size:1.6em;margin-bottom:4px">{ไอคอน}</div>
      <div style="font-size:.82em;color:#64748b;margin-bottom:4px">{หัวข้อ}</div>
      <div style="font-size:1.7em;font-weight:700;color:{สี}">{ค่า}</div>
      <div style="font-size:.8em;color:#94a3b8">{หน่วย}</div>
    </div>"""

def ส่วนโครงการ(รายการ, ข้อความว่าง):
    if not รายการ:
        return f'<p style="color:#94a3b8;font-style:italic;padding:12px 0">{ข้อความว่าง}</p>'
    แถว = "".join(แถวตาราง(ป) for ป in รายการ)
    return f'{หัวตาราง}{แถว}</tbody></table>'

หัวตาราง = """
<div style="overflow-x:auto">
<table style="width:100%;border-collapse:collapse;font-size:.88em">
  <thead>
    <tr style="border-bottom:2px solid #e2e8f0">
      <th style="text-align:left;padding:10px 12px;color:#475569;font-weight:600">ชื่อโครงการ</th>
      <th style="text-align:right;padding:10px 12px;color:#475569;font-weight:600">งบประมาณ (บาท)</th>
      <th style="padding:10px 12px;color:#475569;font-weight:600">ความคืบหน้า</th>
      <th style="padding:10px 12px;color:#475569;font-weight:600">วันเริ่มต้น</th>
      <th style="padding:10px 12px;color:#475569;font-weight:600">วันสิ้นสุด</th>
      <th style="padding:10px 12px;color:#475569;font-weight:600">เหลือเวลา</th>
      <th style="padding:10px 12px;color:#475569;font-weight:600">สถานะ</th>
    </tr>
  </thead>
  <tbody>"""

# ── สร้าง HTML ────────────────────────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Research Dashboard — {วันนี้}</title>
  <style>
    * {{ box-sizing:border-box; margin:0; padding:0 }}
    body {{ font-family:'Segoe UI',Tahoma,sans-serif; background:#f0f4f8; color:#1e293b; min-height:100vh }}
    .row:hover td {{ background:#f8fafc }}
    td {{ padding:12px; border-bottom:1px solid #f1f5f9; vertical-align:middle }}
    .section {{ background:white; border-radius:14px; padding:28px 32px; box-shadow:0 1px 4px #1e3a8a12; margin-bottom:24px }}
    h2 {{ font-size:1em; font-weight:700; color:#1e293b; margin-bottom:20px; display:flex; align-items:center; gap:8px }}
    h2::before {{ content:''; display:block; width:4px; height:18px; background:currentColor; border-radius:2px; opacity:.4 }}
  </style>
</head>
<body>

<!-- ── HEADER ───────────────────────────────────────────────── -->
<div style="background:linear-gradient(135deg,#1e3a8a 0%,#1d4ed8 60%,#2563eb 100%);color:white;padding:0 40px">
  <div style="max-width:1200px;margin:0 auto;padding:28px 0;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px">
    <div>
      <div style="font-size:.78em;letter-spacing:.1em;opacity:.7;margin-bottom:4px">RESEARCH MANAGEMENT SYSTEM</div>
      <h1 style="font-size:1.6em;font-weight:700;letter-spacing:.01em">รายงานโครงการวิจัย</h1>
      <div style="font-size:.85em;opacity:.8;margin-top:4px">ข้อมูลจาก {INPUT_FILE}</div>
    </div>
    <div style="text-align:right;font-size:.85em;opacity:.85">
      <div style="font-size:1.4em;font-weight:700">{วันนี้.strftime('%d')}</div>
      <div>{วันนี้.strftime('%B %Y')}</div>
      <div style="opacity:.7;margin-top:2px">สร้างเมื่อ {datetime.now().strftime('%H:%M')} น.</div>
    </div>
  </div>
</div>

<!-- ── CONTENT ──────────────────────────────────────────────── -->
<div style="max-width:1200px;margin:0 auto;padding:32px 24px">

  <!-- การ์ดสรุป -->
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin-bottom:28px">
    {การ์ด("📋","โครงการทั้งหมด",len(โครงการ),"โครงการ","#1d4ed8","#eff6ff")}
    {การ์ด("💰","งบประมาณรวม",f"{งบรวม/1e6:.1f}M","บาท","#7c3aed","#f5f3ff")}
    {การ์ด("✅","เสร็จแล้ว",นับสถานะ.get("เสร็จแล้ว",0),f"งบ {งบตามสถานะ.get('เสร็จแล้ว',0):,} บาท","#10b981","#f0fdf4")}
    {การ์ด("▶","กำลังดำเนินการ",นับสถานะ.get("กำลังดำเนินการ",0),f"งบ {งบตามสถานะ.get('กำลังดำเนินการ',0):,} บาท","#3b82f6","#eff6ff")}
    {การ์ด("⚠","ล่าช้า",นับสถานะ.get("ล่าช้า",0),f"งบ {งบตามสถานะ.get('ล่าช้า',0):,} บาท","#ef4444","#fef2f2")}
  </div>

  <!-- ตารางทุกโครงการ -->
  <div class="section">
    <h2 style="color:#1d4ed8">โครงการทั้งหมด ({len(โครงการ)} โครงการ)</h2>
    {ส่วนโครงการ(โครงการ, "")}
  </div>

  <!-- โครงการล่าช้า -->
  <div class="section" style="border-left:4px solid #ef4444">
    <h2 style="color:#ef4444">⚠ โครงการล่าช้า &nbsp;<span style="font-size:.85em;opacity:.7">({len(ล่าช้า)} โครงการ)</span></h2>
    {ส่วนโครงการ(ล่าช้า, "ไม่มีโครงการล่าช้า")}
  </div>

  <!-- โครงการเสี่ยง -->
  <div class="section" style="border-left:4px solid #f59e0b">
    <h2 style="color:#d97706">⚡ คืบหน้า &lt;50% และเหลือเวลาไม่เกิน 180 วัน &nbsp;<span style="font-size:.85em;opacity:.7">({len(ใกล้หมดเวลา)} โครงการ)</span></h2>
    {ส่วนโครงการ(ใกล้หมดเวลา, "ไม่มีโครงการที่น่าเป็นห่วง")}
  </div>

</div>

<!-- ── FOOTER ───────────────────────────────────────────────── -->
<div style="background:#1e293b;color:#94a3b8;text-align:center;padding:20px;font-size:.82em;margin-top:8px">
  Research Dashboard &nbsp;·&nbsp; สร้างอัตโนมัติโดย report_generator.py &nbsp;·&nbsp; {datetime.now().strftime('%d/%m/%Y %H:%M')} น.
</div>

</body></html>"""

# ── บันทึกไฟล์ ────────────────────────────────────────────────────────────────
try:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"สร้าง {OUTPUT_FILE} เรียบร้อย — เปิดดูในเบราว์เซอร์ได้เลย")
except PermissionError:
    print(f"ไม่สามารถบันทึก {OUTPUT_FILE} ได้ — ไฟล์อาจถูกเปิดอยู่ในเบราว์เซอร์")
