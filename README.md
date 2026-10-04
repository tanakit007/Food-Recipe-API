# Food Recipe API

REST API สำหรับจัดการเมนูอาหาร (Food) และรายการวัตถุดิบหรือส่วนประกอบของแต่ละเมนู (Recipe) พัฒนาด้วย FastAPI และ SQLite

## ความสามารถ

- เพิ่ม ดู แก้ไข และลบเมนูอาหาร
- เพิ่ม ดู แก้ไข และลบ Recipe ของเมนู
- ดูรายละเอียดอาหารพร้อมรายการ Recipe ที่สัมพันธ์กัน
- ตรวจสอบข้อมูลที่ส่งเข้าด้วย Pydantic เช่น ปริมาณต้องมากกว่า 0
- เมื่อลบ Food ระบบจะลบ Recipe ที่อยู่ภายใต้ Food นั้นด้วย
- มีหน้า Swagger UI สำหรับทดลอง API

## เทคโนโลยี

- Python 3.10 ขึ้นไป
- FastAPI สำหรับสร้าง REST API
- Uvicorn สำหรับรันเว็บเซิร์ฟเวอร์
- Pydantic สำหรับตรวจสอบ request data
- SQLite สำหรับจัดเก็บข้อมูล โดยใช้ `sqlite3` ที่มาพร้อม Python

ไม่ต้องติดตั้ง PostgreSQL, ไม่ต้องเปิด database server และไม่ต้องติดตั้ง SQLite แยก

## VS Code Extensions

จำเป็นสำหรับการพัฒนาใน VS Code:

- **Python** โดย Microsoft: เลือก interpreter และรัน Python
- **Pylance** โดย Microsoft: IntelliSense และตรวจสอบโค้ด Python

ส่วนเสริมที่ไม่จำเป็น:

- Extension สำหรับเปิดดูไฟล์ SQLite เช่น SQLite Viewer หรือ SQLite explorer ใช้ตรวจข้อมูลในไฟล์ฐานข้อมูลได้ แต่ API ทำงานได้โดยไม่ติดตั้ง
- ไม่ต้องติดตั้ง PostgreSQL extension

## ติดตั้งหลัง Clone

ตัวอย่างคำสั่งสำหรับ Windows PowerShell ให้เปลี่ยน `<repository-url>` เป็น URL ของ repository จริง:

```powershell
git clone <repository-url>
cd code_food_python
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

ถ้าเครื่องไม่มีคำสั่ง `py` ให้ใช้ `python -m venv .venv` แทน หาก PowerShell ปิดกั้นการ activate environment สามารถเรียก Python ใน environment โดยตรงได้:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

## เริ่ม API

เมื่อเปิดใช้งาน virtual environment แล้ว จากโฟลเดอร์โปรเจกต์รัน:

```powershell
python -m uvicorn main:app --reload
```

เปิด URL ต่อไปนี้ในเบราว์เซอร์:

- API documentation และหน้าทดลอง: <http://127.0.0.1:8000/docs>
- Health check: <http://127.0.0.1:8000/>

หยุด server ด้วย `Ctrl+C` ใน terminal ที่กำลังรันอยู่ หากพอร์ต 8000 ถูกใช้งาน ให้เลือกพอร์ตอื่น:

```powershell
python -m uvicorn main:app --reload --port 8001
```

## ฐานข้อมูล SQLite

แอปสร้างตารางจาก `database/schema_sqlite.sql` อัตโนมัติเมื่อมีการเรียก endpoint ที่ใช้ฐานข้อมูล และเก็บข้อมูลไว้ที่:

```text
database/food_recipe.sqlite3
```

ไฟล์ฐานข้อมูลจะถูกสร้างเมื่อมีการเรียกใช้งานครั้งแรก ข้อมูลจะคงอยู่หลังปิด server และเปิดใหม่ ไม่ต้องสร้าง database หรือรัน SQL ด้วยตนเอง

หากต้องการเปลี่ยนตำแหน่งไฟล์ ให้กำหนด `DB_PATH` ในไฟล์ `.env` ที่ root ของโปรเจกต์ เช่น:

```env
DB_PATH=database/food_recipe.sqlite3
```

`database/schema_postgresql.sql` เป็น schema สำหรับ PostgreSQL รุ่นเดิม แอปปัจจุบันใช้ SQLite และไม่ได้เรียกไฟล์นี้

## API Endpoints

ทุก endpoint ส่งและรับ JSON โดยทั่วไปผลลัพธ์มีรูปแบบ `{ "success": true, "data": ... }`

### Foods

| Method | Path | รายละเอียด |
| --- | --- | --- |
| `GET` | `/foods/` | ดู Food ทั้งหมด |
| `GET` | `/foods/{food_id}` | ดู Food หนึ่งรายการพร้อม `recipeList` |
| `POST` | `/foods/` | สร้าง Food |
| `PUT` | `/foods/` | แก้ไข Food โดยระบุ `id` |
| `DELETE` | `/foods/{food_id}` | ลบ Food และ Recipe ที่เกี่ยวข้อง |

ตัวอย่างสร้าง Food:

```json
{
  "nameTh": "ข้าวผัด",
  "category": "อาหารไทย"
}
```

ตัวอย่างแก้ไข Food:

```json
{
  "id": 1,
  "nameTh": "ข้าวผัดกุ้ง",
  "category": "อาหารไทย"
}
```

### Recipes

| Method | Path | รายละเอียด |
| --- | --- | --- |
| `GET` | `/recipes/?food_id=1` | ดู Recipe ทั้งหมดของ Food ที่ระบุ |
| `GET` | `/recipes/?id=1` | ดู Recipe หนึ่งรายการ |
| `POST` | `/recipes/` | เพิ่ม Recipe ให้ Food |
| `PUT` | `/recipes/` | แก้ไข Recipe โดยระบุ `id` |
| `DELETE` | `/recipes/{recipe_id}` | ลบ Recipe |

ตัวอย่างสร้าง Recipe:

```json
{
  "food_id": 1,
  "recipeName": "กระเทียม",
  "quantity": 5,
  "unitName": "กลีบ"
}
```

ตัวอย่างแก้ไข Recipe:

```json
{
  "id": 1,
  "recipeName": "กระเทียมสับ",
  "quantity": 8,
  "unitName": "กลีบ"
}
```

`quantity` ต้องมากกว่า 0 และ Food ที่ใช้ใน Recipe ต้องมีอยู่จริง หากส่งข้อมูลไม่ถูกต้อง API จะตอบ `422`; หากไม่พบรายการที่ระบุจะตอบ `404`

## ทดลองด้วย Postman

นำเข้า collection ที่ `postman/Food_Recipe_Python_API.postman_collection.json` หรือทดลอง request โดยตรงจากหน้า `/docs`

## ปัญหาที่พบและวิธีแก้

### `ModuleNotFoundError: No module named 'fastapi'`

มักเกิดจากยังไม่ได้ติดตั้ง dependencies หรือ VS Code ใช้ Python คนละ environment กับที่ติดตั้งแพ็กเกจไว้ ให้เปิด terminal ที่ root ของโปรเจกต์, activate `.venv` แล้วรัน:

```powershell
python -m pip install -r requirements.txt
```

ใน VS Code เลือก interpreter ให้เป็น `.venv` ด้วยคำสั่ง **Python: Select Interpreter** จาก Command Palette

### ติดตั้ง dependencies ไม่ผ่าน หรือพยายาม build `psycopg2` / `pydantic-core`

โปรเจกต์รุ่นก่อนใช้ PostgreSQL และ dependency บางรุ่นไม่มี binary wheel สำหรับ Python รุ่นใหม่ ทำให้ pip พยายาม build เองและอาจต้องใช้ PostgreSQL development tools หรือ Visual C++ Build Tools

โปรเจกต์รุ่นปัจจุบันเปลี่ยนเป็น SQLite และถอด `psycopg2` ออกจาก `requirements.txt` แล้ว ให้ดึงไฟล์ล่าสุดและติดตั้งจาก `requirements.txt` ของโปรเจกต์นี้ หากยังมี error เดิม ให้ตรวจว่าเปิดโฟลเดอร์โปรเจกต์ถูกต้องและเลือก `.venv` ที่สร้างใหม่

### `psycopg2.OperationalError` หรือ connection ไป `localhost:5432` ถูกปฏิเสธ

นี่เป็นการตั้งค่าของ PostgreSQL รุ่นเดิม หรือ server process เก่าที่ยังรันอยู่ รุ่นปัจจุบันไม่ต้องใช้ PostgreSQL: หยุด server เก่าด้วย `Ctrl+C` แล้วเริ่มใหม่ด้วยคำสั่งในหัวข้อ [เริ่ม API](#เริ่ม-api) หากยังเห็นข้อความ `psycopg2` ให้ตรวจว่า VS Code เปิด source code รุ่นล่าสุด

### พอร์ต 8000 ถูกใช้งานแล้ว

หยุด server ตัวเดิมด้วย `Ctrl+C` ใน terminal ที่เปิด server อยู่ หรือใช้พอร์ตอื่น เช่น:

```powershell
python -m uvicorn main:app --reload --port 8001
```

### `GET /recipes/` ตอบ `422`

การอ่าน Recipe ต้องระบุว่าจะค้นหาด้วย `food_id` หรือ `id` เช่น `/recipes/?food_id=1` หรือ `/recipes/?id=1`

## โครงสร้างหลัก

```text
main.py                     FastAPI application และ health endpoint
config/database.py          เปิด SQLite connection และเตรียม schema
database/schema_sqlite.sql  โครงสร้างตาราง SQLite
models/                  การทำงานกับข้อมูล Food และ Recipe
routers/                 API routes สำหรับ Food และ Recipe
schemas/                 ตรวจสอบ request data ด้วย Pydantic
postman/                 Postman collection สำหรับทดลอง API
```
