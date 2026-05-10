import sys
import io
if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')

import os
import glob
from datetime import date

# ดึงวันที่วันนี้ในรูปแบบ YYYY-MM-DD
วันที่วันนี้ = date.today().strftime("%Y-%m-%d")

# หาไฟล์ .txt ทุกไฟล์ในโฟลเดอร์ปัจจุบัน ยกเว้นไฟล์ที่มีวันที่นำหน้าอยู่แล้ว
ไฟล์ทั้งหมด = [
    f for f in glob.glob("*.txt")
    if not f.startswith(วันที่วันนี้)
]

# ถ้าไม่เจอไฟล์ที่ต้องเปลี่ยนชื่อให้แจ้งแล้วจบ
if not ไฟล์ทั้งหมด:
    print("ไม่พบไฟล์ .txt ที่ต้องเปลี่ยนชื่อ")
else:
    for ชื่อเดิม in sorted(ไฟล์ทั้งหมด):
        # สร้างชื่อใหม่โดยเติมวันที่นำหน้าด้วย _
        ชื่อใหม่ = f"{วันที่วันนี้}_{ชื่อเดิม}"
        os.rename(ชื่อเดิม, ชื่อใหม่)
        print(f"  เปลี่ยนชื่อ: {ชื่อเดิม}  →  {ชื่อใหม่}")

    print(f"\n  เสร็จแล้ว — เปลี่ยนชื่อทั้งหมด {len(ไฟล์ทั้งหมด)} ไฟล์")
