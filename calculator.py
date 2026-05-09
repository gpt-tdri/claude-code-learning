import sys
sys.stdout.reconfigure(encoding='utf-8')


def format_number(n):
    """แสดงเลขจำนวนเต็มโดยไม่มี .0 และตัดทศนิยมที่ไม่จำเป็นออก"""
    rounded = round(n, 10)
    if rounded == int(rounded):
        return str(int(rounded))
    return f"{rounded:.10f}".rstrip("0")


def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("กรุณาใส่ตัวเลขเท่านั้น")


print("เลือกการคำนวณ:")
print("  1. บวก")
print("  2. ลบ")
print("  3. คูณ")
print("  4. หาร")

choice = input("\nใส่หมายเลข (1-4): ").strip()

if choice not in ("1", "2", "3", "4"):
    print("กรุณาเลือกหมายเลข 1-4 เท่านั้น")
else:
    a = get_float("ใส่ตัวเลขที่ 1: ")
    b = get_float("ใส่ตัวเลขที่ 2: ")
    fa, fb = format_number(a), format_number(b)

    if choice == "1":
        print(f"ผลลัพธ์: {fa} + {fb} = {format_number(a + b)}")
    elif choice == "2":
        print(f"ผลลัพธ์: {fa} - {fb} = {format_number(a - b)}")
    elif choice == "3":
        print(f"ผลลัพธ์: {fa} × {fb} = {format_number(a * b)}")
    elif choice == "4":
        if b == 0:
            print("หารด้วยศูนย์ไม่ได้")
        else:
            print(f"ผลลัพธ์: {fa} ÷ {fb} = {format_number(a / b)}")
