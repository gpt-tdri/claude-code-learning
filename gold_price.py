import sys
import io
if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding='utf-8')

import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.aurora.co.th/price/gold_pricelist/ราคาทองวันนี้"
OUTPUT_FILE = "gold_price_log.txt"


def ดึงราคาทอง():
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    # หา section ทองคำแท่ง — ถ้าไม่เจอใช้ทั้งหน้าเป็น fallback
    แท่ง = next(
        (t.find_parent() for t in soup.find_all(["h2", "h3", "h4"]) if "ทองคำแท่ง" in t.get_text()),
        soup,
    )

    # หา "รับซื้อคืน" แล้วดึงตัวเลขที่อยู่ถัดไป
    ราคา = None
    for elem in แท่ง.find_all(string=lambda t: t and "รับซื้อคืน" in t):
        ถัดไป = elem.find_parent().find_next(string=lambda t: t and any(c.isdigit() for c in t))
        if ถัดไป:
            ราคา = ถัดไป.strip().replace("บาท", "").replace(",", "").strip()
            break

    # หาเวลาอัปเดตบนเว็บ เช่น "09:07 น."
    เวลาเว็บ = next(
        (e.strip() for e in soup.find_all(string=lambda t: t and ":" in t and "น." in t and any(c.isdigit() for c in t))),
        None,
    )

    return ราคา, เวลาเว็บ


def บันทึกราคา(ราคา, เวลาเว็บ):
    วันนี้ = datetime.now().strftime("%Y-%m-%d")

    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, encoding="utf-8") as f:
            if วันนี้ in f.read():
                print(f"บันทึกวันนี้ ({วันนี้}) ไปแล้ว ไม่บันทึกซ้ำ")
                return False

    ส่วนเวลา = f" (เวลาบนเว็บ: {เวลาเว็บ})" if เวลาเว็บ else ""
    บรรทัด = f"{วันนี้} | ราคารับซื้อคืนทองแท่ง: {ราคา} บาท{ส่วนเวลา} | บันทึกเวลา {datetime.now().strftime('%H:%M')} น."

    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(บรรทัด + "\n")
    print(f"บันทึกแล้ว: {บรรทัด}")
    return True


def main():
    print("กำลังดึงราคาทอง...")
    try:
        ราคา, เวลาเว็บ = ดึงราคาทอง()
        if ราคา:
            บันทึกราคา(ราคา, เวลาเว็บ)
        else:
            print("ไม่พบราคา — โครงสร้างเว็บอาจเปลี่ยนแปลง")
    except requests.exceptions.RequestException as e:
        print(f"เชื่อมต่อเว็บไม่ได้: {e}")


if __name__ == "__main__":
    main()
