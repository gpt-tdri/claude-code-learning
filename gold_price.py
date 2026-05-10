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
    """
    เปิดเว็บ aurora.co.th แล้วดึงราคารับซื้อคืนทองคำแท่ง
    คืนค่า (ราคา, เวลาบนเว็บ) เช่น ("71750", "09:07 น. (ครั้งที่ 2)")
    ถ้าหาราคาไม่เจอ คืน (None, None)
    """
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    # หา section ทองคำแท่ง โดยมองหาหัวข้อ h2/h3/h4 ที่มีคำว่า "ทองคำแท่ง"
    # ถ้าไม่เจอ ใช้ soup (ทั้งหน้า) เป็น fallback แทน
    แท่ง = next(
        (t.find_parent() for t in soup.find_all(["h2", "h3", "h4"]) if "ทองคำแท่ง" in t.get_text()),
        soup,
    )

    # วนหาข้อความ "รับซื้อคืน" ใน section นั้น แล้วดึงตัวเลขที่อยู่ถัดไปทันที
    ราคา = None
    for elem in แท่ง.find_all(string=lambda t: t and "รับซื้อคืน" in t):
        ถัดไป = elem.find_parent().find_next(string=lambda t: t and any(c.isdigit() for c in t))
        if ถัดไป:
            # ตัด "บาท" และ "," ออก เหลือแค่ตัวเลข เช่น "71,750 บาท" → "71750"
            ราคา = ถัดไป.strip().replace("บาท", "").replace(",", "").strip()
            break

    # หาเวลาอัปเดตบนเว็บ โดยมองหาข้อความที่มีทั้ง ":" และ "น." เช่น "09:07 น."
    เวลาเว็บ = next(
        (e.strip() for e in soup.find_all(string=lambda t: t and ":" in t and "น." in t and any(c.isdigit() for c in t))),
        None,
    )

    return ราคา, เวลาเว็บ


def บันทึกราคา(ราคา, เวลาเว็บ):
    """
    เขียนราคาต่อท้ายลงไฟล์ log — วันละ 1 บรรทัด
    ถ้าวันนี้บันทึกไปแล้วจะไม่เขียนซ้ำ
    คืนค่า True ถ้าบันทึกสำเร็จ, False ถ้าบันทึกไปแล้ววันนี้
    """
    วันนี้ = datetime.now().strftime("%Y-%m-%d")

    # ตรวจว่าบันทึกวันนี้ไปแล้วหรือยัง โดยค้นหาวันที่ในไฟล์
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, encoding="utf-8") as f:
            if วันนี้ in f.read():
                print(f"บันทึกวันนี้ ({วันนี้}) ไปแล้ว ไม่บันทึกซ้ำ")
                return False

    # สร้างข้อความบรรทัด เช่น "2026-05-10 | ราคา... | บันทึกเวลา 09:00 น."
    ส่วนเวลา = f" (เวลาบนเว็บ: {เวลาเว็บ})" if เวลาเว็บ else ""
    บรรทัด = f"{วันนี้} | ราคารับซื้อคืนทองแท่ง: {ราคา} บาท{ส่วนเวลา} | บันทึกเวลา {datetime.now().strftime('%H:%M')} น."

    # เปิดด้วย mode "a" (append) เพื่อต่อท้ายโดยไม่ทับข้อมูลเดิม
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(บรรทัด + "\n")
    print(f"บันทึกแล้ว: {บรรทัด}")
    return True


def main():
    """จุดเริ่มต้นโปรแกรม — เรียก ดึงราคาทอง() แล้วส่งผลให้ บันทึกราคา()"""
    print("กำลังดึงราคาทอง...")
    try:
        ราคา, เวลาเว็บ = ดึงราคาทอง()
        if ราคา:
            บันทึกราคา(ราคา, เวลาเว็บ)
        else:
            print("ไม่พบราคา — โครงสร้างเว็บอาจเปลี่ยนแปลง")
    except requests.exceptions.RequestException as e:
        # ดักจับทุก error ที่เกี่ยวกับเครือข่าย เช่น ไม่มีอินเทอร์เน็ต, เว็บล่ม, timeout
        print(f"เชื่อมต่อเว็บไม่ได้: {e}")


if __name__ == "__main__":
    main()
