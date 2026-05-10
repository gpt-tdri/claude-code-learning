import sys
import io
if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')

import glob
import shutil
import os
from datetime import date

# สร้างชื่อ folder backup จากวันที่วันนี้
folder_backup = f"backup_{date.today().strftime('%Y-%m-%d')}"

# สร้าง folder ถ้ายังไม่มี
os.makedirs(folder_backup, exist_ok=True)

# หาไฟล์ .py ทุกไฟล์ในโฟลเดอร์ปัจจุบัน ยกเว้นตัวเองเพื่อกัน copy ซ้ำ
ไฟล์ทั้งหมด = sorted(f for f in glob.glob("*.py") if f != "backup.py")

print(f"backup ไปที่ folder: {folder_backup}/")
print(f"{'─' * 40}")

for ไฟล์ in ไฟล์ทั้งหมด:
    # copy ไฟล์เข้า folder backup
    shutil.copy2(ไฟล์, folder_backup)
    print(f"  ✓  {ไฟล์}")

print(f"{'─' * 40}")
print(f"รวม {len(ไฟล์ทั้งหมด)} ไฟล์  |  บันทึกใน {folder_backup}/")
