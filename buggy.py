# buggy.py — ไฟล์ตัวอย่างที่มี bug 3 อย่าง
import sys
sys.stdout = __import__('io').TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# -------------------------------------------------------------------
# BUG 1: Syntax Error — ลืมปิดวงเล็บในบรรทัด print
# แก้ได้โดยเปลี่ยน  print("ผลรวม:", total  →  print("ผลรวม:", total)
# -------------------------------------------------------------------
def calculate_sum(numbers):
    total = sum(numbers)
    print("ผลรวม:", total)  # FIXED: เพิ่ม ) ปิดวงเล็บ
    return total


# -------------------------------------------------------------------
# BUG 2: Logic Error — คำนวณค่าเฉลี่ยผิด (หารด้วย len แต่ใช้ค่าผิด)
# หารด้วย len(numbers) + 1 แทนที่จะเป็น len(numbers)
# ทำให้ผลลัพธ์น้อยกว่าความเป็นจริงเสมอ
# -------------------------------------------------------------------
def calculate_average(numbers):
    total = sum(numbers)
    average = total / len(numbers)  # FIXED: เอา + 1 ออก
    return average


# -------------------------------------------------------------------
# BUG 3: Runtime Error — ZeroDivisionError เมื่อ divisor เป็น 0
# ไม่มีการตรวจสอบก่อนหาร ทำให้ crash ตอน runtime
# -------------------------------------------------------------------
def divide(a, b):
    if b == 0:  # FIXED: ตรวจสอบก่อนหาร
        print("หารด้วยศูนย์ไม่ได้")
        return None
    return a / b


# ทดสอบ (จะไม่รันได้เพราะ Syntax Error ด้านบนขัดอยู่)
data = [10, 20, 30, 40]
calculate_sum(data)
print("ค่าเฉลี่ย:", calculate_average(data))
print("ผลหาร:", divide(10, 0))
