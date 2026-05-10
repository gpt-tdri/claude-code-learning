import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import contacts


def print_divider():
    print("-" * 35)


def show_contacts(data):
    if not data:
        print("  (ไม่มีรายชื่อ)")
        return
    print(f"  {'ชื่อ':<20} {'เบอร์โทร'}")
    print_divider()
    for name, phone in sorted(data.items()):
        print(f"  {name:<20} {phone}")


def menu_add():
    name = input("ชื่อ: ").strip()
    phone = input("เบอร์โทร: ").strip()
    if not name or not phone:
        print("กรุณากรอกข้อมูลให้ครบ")
        return
    ok, msg = contacts.add_contact(name, phone)
    print(msg)


def menu_delete():
    name = input("ชื่อที่ต้องการลบ: ").strip()
    if not name:
        print("กรุณาใส่ชื่อที่ต้องการลบ")
        return
    ok, msg = contacts.delete_contact(name)
    print(msg)


def menu_search():
    keyword = input("ค้นหาชื่อ: ").strip()
    if not keyword:
        print("กรุณาใส่คำค้นหา")
        return
    results = contacts.search_contact(keyword)
    print(f"\nพบ {len(results)} รายการ:")
    show_contacts(results)


def menu_list():
    data = contacts.list_all()
    print(f"\nรายชื่อทั้งหมด ({len(data)} รายการ):")
    show_contacts(data)


def main():
    while True:
        print()
        print("=" * 35)
        print("       สมุดโทรศัพท์")
        print("=" * 35)
        print("  1. เพิ่มรายชื่อ")
        print("  2. ลบรายชื่อ")
        print("  3. ค้นหารายชื่อ")
        print("  4. แสดงรายชื่อทั้งหมด")
        print("  0. ออกจากโปรแกรม")
        print_divider()

        choice = input("เลือกเมนู: ").strip()

        print()
        if choice == "1":
            menu_add()
        elif choice == "2":
            menu_delete()
        elif choice == "3":
            menu_search()
        elif choice == "4":
            menu_list()
        elif choice == "0":
            print("ออกจากโปรแกรมแล้ว")
            break
        else:
            print("กรุณาเลือกเมนู 0-4")


if __name__ == "__main__":
    main()
