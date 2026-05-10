import sys
import io
if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')

# รับชื่อจากผู้ใช้
ชื่อ = input("กรุณาใส่ชื่อของคุณ: ").strip()

# ตรวจสอบว่าใส่ชื่อมาหรือเปล่า
if not ชื่อ:
    print("ไม่ได้ใส่ชื่อ ไม่สามารถทักทายได้")
else:
    print(f"สวัสดีครับ/ค่ะ คุณ{ชื่อ} ยินดีที่ได้รู้จัก!")
