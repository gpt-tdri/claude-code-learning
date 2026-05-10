import sys
import io
if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')

import subprocess
from datetime import datetime

def รัน(ชื่อไฟล์):
    print(f"  กำลังรัน {ชื่อไฟล์}...")
    result = subprocess.run(
        [sys.executable, ชื่อไฟล์],
        capture_output=True, text=True, encoding="utf-8"
    )
    # แสดง output จาก script ที่รัน
    if result.stdout.strip():
        for บรรทัด in result.stdout.strip().splitlines():
            print(f"    → {บรรทัด}")
    if result.returncode != 0 and result.stderr.strip():
        print(f"    ⚠ error: {result.stderr.strip()[:120]}")
    return result.returncode == 0

print("=" * 40)
print("  อัปเดต Dashboard ส่วนตัว")
print("=" * 40)

# 1. ดึงราคาทองล่าสุด
รัน("gold_price.py")

# 2. สร้าง dashboard ใหม่จากข้อมูลล่าสุด
รัน("dashboard.py")

print("=" * 40)
print(f"  Dashboard อัปเดตแล้ว เวลา {datetime.now().strftime('%H:%M')} น.")
print("=" * 40)
