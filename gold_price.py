import sys
import io
if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

URL = "https://www.aurora.co.th/price/gold_pricelist/ราคาทองวันนี้"
OUTPUT_FILE = "gold_price_log.txt"


def ดึงราคาทอง():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers, timeout=10)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    # หา section ทองคำแท่ง จากหัวข้อ h2/h3 ที่มีข้อความ "ทองคำแท่ง"
    ราคา = None
    เวลาเว็บ = None

    for tag in soup.find_all(["h2", "h3", "h4"]):
        if "ทองคำแท่ง" in tag.get_text():
            # หา element พี่น้องหรือลูกที่มีข้อความ "รับซื้อคืน"
            section = tag.find_parent()
            for elem in section.find_all(string=lambda t: t and "รับซื้อคืน" in t):
                # ราคาอยู่ใน element ถัดไปหรือ sibling
                parent = elem.find_parent()
                ตัวเลข = parent.find_next(string=lambda t: t and any(c.isdigit() for c in t))
                if ตัวเลข:
                    ราคา = ตัวเลข.strip().replace("บาท", "").replace(",", "").strip()
                    break
            break

    # ถ้าวิธีแรกไม่เจอ ลองหา span/td ที่มีข้อความ "รับซื้อคืน" โดยตรง
    if not ราคา:
        for elem in soup.find_all(string=lambda t: t and "รับซื้อคืน" in t):
            parent = elem.find_parent()
            ตัวเลข = parent.find_next(string=lambda t: t and any(c.isdigit() for c in t))
            if ตัวเลข:
                ราคา = ตัวเลข.strip().replace("บาท", "").replace(",", "").strip()
                break

    # หาเวลาอัปเดตบนเว็บ
    for elem in soup.find_all(string=lambda t: t and "น." in t and any(c.isdigit() for c in t)):
        text = elem.strip()
        if ":" in text:
            เวลาเว็บ = text
            break

    return ราคา, เวลาเว็บ


def บันทึกราคา(ราคา, เวลาเว็บ):
    วันนี้ = datetime.now().strftime("%Y-%m-%d")
    เวลาบันทึก = datetime.now().strftime("%H:%M")

    # อ่านไฟล์เดิมตรวจว่าวันนี้บันทึกไปแล้วหรือยัง
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, encoding="utf-8") as f:
            if วันนี้ in f.read():
                print(f"บันทึกวันนี้ ({วันนี้}) ไปแล้ว ไม่บันทึกซ้ำ")
                return False

    บรรทัด = f"{วันนี้} | ราคารับซื้อคืนทองแท่ง: {ราคา} บาท"
    if เวลาเว็บ:
        บรรทัด += f" (เวลาบนเว็บ: {เวลาเว็บ})"
    บรรทัด += f" | บันทึกเวลา {เวลาบันทึก} น."

    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(บรรทัด + "\n")

    print(f"บันทึกแล้ว: {บรรทัด}")
    return True


def main():
    print("กำลังดึงราคาทอง...")
    try:
        ราคา, เวลาเว็บ = ดึงราคาทอง()
        if not ราคา:
            print("ไม่พบราคา — โครงสร้างเว็บอาจเปลี่ยนแปลง")
            return
        บันทึกราคา(ราคา, เวลาเว็บ)
    except requests.exceptions.RequestException as e:
        print(f"เชื่อมต่อเว็บไม่ได้: {e}")


if __name__ == "__main__":
    main()
