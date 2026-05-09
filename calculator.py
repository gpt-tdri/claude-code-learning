import sys
sys.stdout.reconfigure(encoding='utf-8')

print("เลือกการคำนวณ:")
print("  1. บวก")
print("  2. ลบ")
print("  3. คูณ")
print("  4. หาร")

choice = input("\nใส่หมายเลข (1-4): ")

a = float(input("ใส่ตัวเลขที่ 1: "))
b = float(input("ใส่ตัวเลขที่ 2: "))

if choice == "1":
    print(f"ผลลัพธ์: {a} + {b} = {a + b}")
elif choice == "2":
    print(f"ผลลัพธ์: {a} - {b} = {a - b}")
elif choice == "3":
    print(f"ผลลัพธ์: {a} × {b} = {a * b}")
elif choice == "4":
    if b != 0:
        print(f"ผลลัพธ์: {a} ÷ {b} = {a / b}")
    else:
        print("หารด้วยศูนย์ไม่ได้")
else:
    print("กรุณาเลือกหมายเลข 1-4 เท่านั้น")
