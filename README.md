# Personal Dashboard โปรเจค

Dashboard ส่วนตัวที่รวบรวมข้อมูลการเงินและราคาทอง แสดงผลเป็น HTML แบบ real-time

## ไฟล์หลัก

| ไฟล์ | หน้าที่ |
|------|--------|
| `dashboard.py` | สร้าง `dashboard.html` จากข้อมูลการเงินและราคาทอง |
| `gold_price.py` | ดึงราคาทองแท่งรับซื้อคืนจาก aurora.co.th บันทึกลง log วันละครั้ง |
| `budget.py` | เมนูบันทึกรายรับ-รายจ่าย |
| `finance.py` | logic การเงิน บันทึกข้อมูลลง `finance_data.json` |
| `run_all.py` | รัน gold_price.py + dashboard.py ครั้งเดียวจบ |

## วิธีใช้

### อัปเดต Dashboard ครั้งเดียว
```
python run_all.py
```

### บันทึกรายรับรายจ่าย
```
python budget.py
```

### เปิด Dashboard
เปิดไฟล์ `dashboard.html` ในเบราว์เซอร์ — หน้าจะรีเฟรชอัตโนมัติทุก 60 วินาที

## ข้อมูลที่แสดงใน Dashboard

- **ยอดเงินคงเหลือ** — รายรับรวม ลบ รายจ่ายรวม
- **ราคาทองแท่ง** — ราคารับซื้อคืนล่าสุดจาก aurora.co.th
- **รายจ่ายสูงสุด 3 อันดับ** — พร้อม progress bar เทียบสัดส่วน
- **กราฟ Donut** — สัดส่วนรายรับ vs รายจ่าย
- **กราฟ Bar** — รายการแต่ละรายการ
- **ตารางธุรกรรม** — ประวัติทั้งหมด

## Scheduled Tasks (Windows)

| Task | เวลา | ไฟล์ |
|------|------|------|
| `GoldPriceLogger` | 09:00 น. ทุกวัน | `gold_price.py` |
| `ResearchReportGenerator` | 08:00 น. ทุกวัน | `report_generator.py` |

## ไฟล์ข้อมูล

| ไฟล์ | สร้างโดย | รูปแบบ |
|------|---------|--------|
| `finance_data.json` | `budget.py` | JSON array |
| `gold_price_log.txt` | `gold_price.py` | Text log วันละบรรทัด |
| `dashboard.html` | `dashboard.py` | HTML |
| `daily_report.html` | `report_generator.py` | HTML |
