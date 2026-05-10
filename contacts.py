import json
import os

DATA_FILE = "contacts_data.json"


def _load():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"คำเตือน: ไฟล์ {DATA_FILE} เสียหาย — เริ่มต้นด้วยข้อมูลว่าง")
            return {}
    return {}


def _save(contacts):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)


def add_contact(name, phone):
    contacts = _load()
    if name in contacts:
        return False, f"'{name}' มีอยู่ในสมุดโทรศัพท์แล้ว"
    contacts[name] = phone
    _save(contacts)
    return True, f"เพิ่ม '{name}' เรียบร้อยแล้ว"


def delete_contact(name):
    contacts = _load()
    if name not in contacts:
        return False, f"ไม่พบ '{name}' ในสมุดโทรศัพท์"
    del contacts[name]
    _save(contacts)
    return True, f"ลบ '{name}' เรียบร้อยแล้ว"


def search_contact(keyword):
    contacts = _load()
    results = {name: phone for name, phone in contacts.items() if keyword.lower() in name.lower()}
    return results


def list_all():
    return _load()
