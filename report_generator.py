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
                    "ชื่อ":       แถว["ชื่อโครงการ"],
                    "งบ":         int(แถว["งบประมาณ"]),
                    "คืบหน้า":    int(แถว["ความคืบหน้า(%)"]),
                    "เริ่ม":      date.fromisoformat(แถว["วันเริ่มต้น"]),
                    "สิ้นสุด":    date.fromisoformat(แถว["วันสิ้นสุด"]),
                    "สถานะ":      แถว["สถานะ"],
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
# ใกล้หมดเวลา = คืบหน้า < 50% และ เหลือเวลาไม่เกิน 180 วัน
ใกล้หมดเวลา = [ป for ป in โครงการ if ป["คืบหน้า"] < 50 and (ป["สิ้นสุด"] - วันนี้).days <= 180]

# ── helpers สร้าง HTML ────────────────────────────────────────────────────────
สีสถานะ = {"เสร็จแล้ว": "#22c55e", "กำลังดำเนินการ": "#3b82f6", "ล่าช้า": "#ef4444"}

def แถบคืบหน้า(pct):
    สี = "#22c55e" if pct >= 75 else "#f59e0b" if pct >= 40 else "#ef4444"
    return f'<div style="background:#e5e7eb;border-radius:4px;height:10px;width:100%"><div style="background:{สี};width:{pct}%;height:10px;border-radius:4px"></div></div><small>{pct}%</small>'

def ป้ายสถานะ(สถานะ):
    สี = สีสถานะ.get(สถานะ, "#6b7280")
    return f'<span style="background:{สี};color:white;padding:2px 10px;border-radius:12px;font-size:0.8em">{สถานะ}</span>'

def แถวตาราง(ป, เน้น=False):
    bg = ' style="background:#fef9c3"' if เน้น else ""
    เหลือ = (ป["สิ้นสุด"] - วันนี้).days
    เหลือข้อความ = f"{เหลือ} วัน" if เหลือ >= 0 else f"<b style='color:#ef4444'>เลยกำหนด {abs(เหลือ)} วัน</b>"
    return f"""<tr{bg}>
      <td>{ป['ชื่อ']}</td>
      <td style="text-align:right">{ป['งบ']:,}</td>
      <td>{แถบคืบหน้า(ป['คืบหน้า'])}</td>
      <td>{ป['เริ่ม']}</td>
      <td>{ป['สิ้นสุด']}</td>
      <td>{เหลือข้อความ}</td>
      <td>{ป้ายสถานะ(ป['สถานะ'])}</td>
    </tr>"""

def การ์ดสรุป(หัวข้อ, ค่า, สี="#1e40af"):
    return f'<div style="background:white;border-left:4px solid {สี};padding:16px 20px;border-radius:8px;box-shadow:0 1px 3px #0001"><div style="font-size:0.85em;color:#6b7280">{หัวข้อ}</div><div style="font-size:1.6em;font-weight:700;color:{สี}">{ค่า}</div></div>'

def ส่วนล่าช้าและเสี่ยง(รายการ, หัวข้อ, สี):
    if not รายการ:
        return f'<p style="color:#6b7280;font-style:italic">ไม่มีโครงการในกลุ่มนี้</p>'
    แถว = "".join(แถวตาราง(ป, เน้น=True) for ป in รายการ)
    return หัวข้อตาราง() + แถว + "</tbody></table>"

def หัวข้อตาราง():
    return """<table style="width:100%;border-collapse:collapse;font-size:0.9em">
    <thead><tr style="background:#f3f4f6">
      <th style="text-align:left;padding:8px">ชื่อโครงการ</th>
      <th style="text-align:right;padding:8px">งบประมาณ (บาท)</th>
      <th style="padding:8px">ความคืบหน้า</th>
      <th style="padding:8px">วันเริ่มต้น</th>
      <th style="padding:8px">วันสิ้นสุด</th>
      <th style="padding:8px">เหลือเวลา</th>
      <th style="padding:8px">สถานะ</th>
    </tr></thead><tbody>"""

# ── สร้าง HTML ────────────────────────────────────────────────────────────────
การ์ดสถานะ = "".join(
    การ์ดสรุป(f"โครงการ{ส}", f"{นับสถานะ.get(ส,0)} โครงการ", สีสถานะ[ส])
    for ส in ["เสร็จแล้ว", "กำลังดำเนินการ", "ล่าช้า"]
)

แถวทั้งหมด = "".join(แถวตาราง(ป) for ป in โครงการ)

html = f"""<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="utf-8">
  <title>รายงานโครงการวิจัย — {วันนี้}</title>
  <style>
    body {{ font-family: 'Segoe UI', sans-serif; background:#f8fafc; color:#1e293b; margin:0; padding:24px }}
    h1   {{ font-size:1.6em; margin-bottom:4px }}
    h2   {{ font-size:1.1em; margin:28px 0 12px; padding-bottom:6px; border-bottom:2px solid #e2e8f0 }}
    .grid{{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:12px; margin-bottom:24px }}
    table{{ width:100%; border-collapse:collapse; background:white; border-radius:8px; overflow:hidden; box-shadow:0 1px 3px #0001 }}
    th,td{{ padding:10px 12px; text-align:left; border-bottom:1px solid #f1f5f9 }}
    th   {{ background:#f8fafc; font-weight:600; font-size:0.85em; color:#475569 }}
    tr:last-child td {{ border-bottom:none }}
  </style>
</head>
<body>
  <h1>รายงานโครงการวิจัย</h1>
  <p style="color:#64748b">สร้างเมื่อ {datetime.now().strftime('%d %B %Y เวลา %H:%M น.')} &nbsp;|&nbsp; ข้อมูลจาก {INPUT_FILE}</p>

  <h2>ภาพรวม</h2>
  <div class="grid">
    {การ์ดสรุป("โครงการทั้งหมด", f"{len(โครงการ)} โครงการ")}
    {การ์ดสรุป("งบประมาณรวม", f"{งบรวม:,} บาท", "#7c3aed")}
    {"".join(การ์ดสรุป(f"งบ{ส}", f"{งบตามสถานะ.get(ส,0):,} บาท", สีสถานะ[ส]) for ส in ["เสร็จแล้ว","กำลังดำเนินการ","ล่าช้า"])}
  </div>

  <h2>รายการโครงการทั้งหมด</h2>
  {หัวข้อตาราง()}{แถวทั้งหมด}</tbody></table>

  <h2 style="color:#ef4444">⚠ โครงการล่าช้า ({len(ล่าช้า)} โครงการ)</h2>
  {ส่วนล่าช้าและเสี่ยง(ล่าช้า,"","")}

  <h2 style="color:#f59e0b">⚠ โครงการคืบหน้าน้อยกว่า 50% และเหลือเวลาไม่เกิน 180 วัน ({len(ใกล้หมดเวลา)} โครงการ)</h2>
  {ส่วนล่าช้าและเสี่ยง(ใกล้หมดเวลา,"","")}

</body></html>"""

# ── บันทึกไฟล์ ────────────────────────────────────────────────────────────────
try:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"สร้าง {OUTPUT_FILE} เรียบร้อย — เปิดดูในเบราว์เซอร์ได้เลย")
except PermissionError:
    print(f"ไม่สามารถบันทึก {OUTPUT_FILE} ได้ — ไฟล์อาจถูกเปิดอยู่ในเบราว์เซอร์")
