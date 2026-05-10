import json
import os

# ชื่อไฟล์ที่ใช้เก็บข้อมูลสมุดโทรศัพท์ทั้งหมด
DATA_FILE = "contacts_data.json"


def _load():
    """โหลดข้อมูลจากไฟล์ JSON — คืนค่า dict {ชื่อ: เบอร์} หรือ {} ถ้าไม่มีไฟล์"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # ไฟล์เสียหาย (เช่น ถูกแก้ด้วย text editor จนผิดรูปแบบ) — เริ่มใหม่แทน crash
            print(f"คำเตือน: ไฟล์ {DATA_FILE} เสียหาย — เริ่มต้นด้วยข้อมูลว่าง")
            return {}
    return {}


def _save(contacts):
    """บันทึก dict ทั้งหมดลงไฟล์ JSON ทับของเดิม"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)


def add_contact(name, phone):
    """เพิ่มรายชื่อใหม่ — คืนค่า (True, ข้อความ) ถ้าสำเร็จ หรือ (False, ข้อความ) ถ้าชื่อซ้ำ"""
    contacts = _load()
    if name in contacts:
        return False, f"'{name}' มีอยู่ในสมุดโทรศัพท์แล้ว"
    contacts[name] = phone
    _save(contacts)
    return True, f"เพิ่ม '{name}' เรียบร้อยแล้ว"


def delete_contact(name):
    """ลบรายชื่อ — คืนค่า (True, ข้อความ) ถ้าสำเร็จ หรือ (False, ข้อความ) ถ้าไม่พบชื่อ"""
    contacts = _load()
    if name not in contacts:
        return False, f"ไม่พบ '{name}' ในสมุดโทรศัพท์"
    del contacts[name]
    _save(contacts)
    return True, f"ลบ '{name}' เรียบร้อยแล้ว"


def search_contact(keyword):
    """ค้นหาชื่อที่มีคำว่า keyword อยู่ — ไม่แยกตัวพิมพ์เล็ก/ใหญ่ — คืนค่า dict ที่ตรงกัน"""
    contacts = _load()
    return {name: phone for name, phone in contacts.items() if keyword.lower() in name.lower()}


def list_all():
    """ดึงรายชื่อทั้งหมด — คืนค่า dict {ชื่อ: เบอร์} ทุกรายการ"""
    return _load()
