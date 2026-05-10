import sys
import io
if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')

import glob

# หาไฟล์ .txt ทุกไฟล์ ยกเว้น summary.txt เพื่อไม่ให้อ่านตัวเองซ้ำ
ไฟล์ทั้งหมด = sorted(f for f in glob.glob("*.txt") if f != "summary.txt")

บรรทัดผลลัพธ์ = []
บรรทัดผลลัพธ์.append("=" * 50)
บรรทัดผลลัพธ์.append("           สรุปไฟล์ .txt ทั้งหมด")
บรรทัดผลลัพธ์.append("=" * 50)
บรรทัดผลลัพธ์.append(f"พบไฟล์ทั้งหมด {len(ไฟล์ทั้งหมด)} ไฟล์")
บรรทัดผลลัพธ์.append("")

รวมบรรทัดทั้งหมด = 0
รวมคำทั้งหมด = 0

for ชื่อไฟล์ in ไฟล์ทั้งหมด:
    try:
        with open(ชื่อไฟล์, encoding="utf-8") as f:
            เนื้อหา = f.read()
    except UnicodeDecodeError:
        # ถ้าอ่านไม่ได้ด้วย utf-8 ให้ลอง encoding อื่น
        with open(ชื่อไฟล์, encoding="cp874") as f:
            เนื้อหา = f.read()

    บรรทัด = เนื้อหา.splitlines()
    # นับคำโดย split ด้วยช่องว่าง กรองส่วนที่ว่างออก
    คำ = [w for line in บรรทัด for w in line.split() if w]

    จำนวนบรรทัด = len(บรรทัด)
    จำนวนคำ = len(คำ)
    รวมบรรทัดทั้งหมด += จำนวนบรรทัด
    รวมคำทั้งหมด += จำนวนคำ

    บรรทัดผลลัพธ์.append(f"┌─ {ชื่อไฟล์}")
    บรรทัดผลลัพธ์.append(f"│  บรรทัด : {จำนวนบรรทัด}")
    บรรทัดผลลัพธ์.append(f"│  คำ     : {จำนวนคำ}")
    บรรทัดผลลัพธ์.append(f"│  เนื้อหา: {เนื้อหา.strip()[:60]}{'...' if len(เนื้อหา.strip()) > 60 else ''}")
    บรรทัดผลลัพธ์.append("│")

บรรทัดผลลัพธ์.append("=" * 50)
บรรทัดผลลัพธ์.append(f"รวมทั้งหมด : {รวมบรรทัดทั้งหมด} บรรทัด  |  {รวมคำทั้งหมด} คำ")
บรรทัดผลลัพธ์.append("=" * 50)

# แสดงผลหน้าจอและบันทึกลง summary.txt พร้อมกัน
try:
    with open("summary.txt", "w", encoding="utf-8") as f:
        for บรรทัดนี้ in บรรทัดผลลัพธ์:
            print(บรรทัดนี้)
            f.write(บรรทัดนี้ + "\n")
    print("\nบันทึกลง summary.txt เรียบร้อย")
except PermissionError:
    print("\nไม่สามารถบันทึก summary.txt ได้ — ไฟล์อาจถูกเปิดอยู่ในโปรแกรมอื่น")
