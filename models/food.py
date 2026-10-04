"""Food model and SQLite persistence operations."""
from __future__ import annotations
from contextlib import closing
from typing import Optional
from sqlite3 import Connection


class Food:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn
        self.id: int = 0
        self.name_th: str = ""
        self.category: str = ""
        self.recipe_list: list = []

    # ---- Class Diagram Methods ----

    def init(self, name: str, category: str) -> None:
        """init(name, category) — กำหนดค่าเริ่มต้น เทียบเท่า PHP Food::init()"""
        self.name_th  = name.strip()
        self.category = category.strip()

    def display(self) -> Optional[dict]:
        """
        display() — คืน Food พร้อม recipeList
        ต้องกำหนด self.id ก่อนเรียก
        เทียบเท่า PHP Food::display() + getWithRecipes()

        """
        sql = """
            SELECT f.id, f."nameTh", f.category,
                   f.created_at, f.updated_at,
                   r.id AS recipe_id, r."recipeName",
                   r.quantity, r."unitName"
            FROM foods f
            LEFT JOIN recipes r ON f.id = r.food_id
            WHERE f.id = ?
            ORDER BY r.id
        """
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql, (self.id,))
            rows = cursor.fetchall()

        if not rows:
            return None

        food: dict = {
            "id":         rows[0]["id"],
            "nameTh":     rows[0]["nameTh"],
            "category":   rows[0]["category"],
            "created_at": str(rows[0]["created_at"]),
            "updated_at": str(rows[0]["updated_at"]),
            "recipeList": [],
        }

        for row in rows:
            if row["recipe_id"] is not None:
                food["recipeList"].append({
                    "id":         row["recipe_id"],
                    "recipeName": row["recipeName"],
                    "quantity":   float(row["quantity"]),
                    "unitName":   row["unitName"],
                })

        return food

    def add_recipe(self, recipe: dict) -> int:
        """
        add_recipe(recipe) — เพิ่ม Recipe เข้าสู่ Food นี้
        เทียบเท่า PHP Food::addRecipe()

        """
        sql = """
            INSERT INTO recipes (food_id, "recipeName", quantity, "unitName")
            VALUES (?, ?, ?, ?)
        """
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql, (
                self.id,
                recipe["recipeName"].strip(),
                float(recipe["quantity"]),
                recipe["unitName"].strip(),
            ))
            return cursor.lastrowid

    # ---- CRUD Methods ----

    def get_all(self) -> list:
        """ดึง Food ทั้งหมด — เทียบเท่า PHP Food::getAll()"""
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(
                'SELECT id, "nameTh", category, created_at, updated_at '
                "FROM foods ORDER BY id"
            )
            rows = cursor.fetchall()
        # แปลง RealDictRow → dict และ datetime → string
        return [self._serialize(dict(r)) for r in rows]

    def create(self) -> int:
        """
        สร้าง Food ใหม่ คืน id ใหม่ — เทียบเท่า PHP Food::create()

        """
        self._validate()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(
                'INSERT INTO foods ("nameTh", category) VALUES (?, ?)',
                (self.name_th, self.category),
            )
            self.id = cursor.lastrowid
        return self.id

    def update(self) -> bool:
        """อัปเดต Food คืน True/False — เทียบเท่า PHP Food::update()"""
        self._validate()
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(
                'UPDATE foods SET "nameTh" = ?, category = ?, '
                'updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                (self.name_th, self.category, self.id),
            )
            return cursor.rowcount > 0

    def delete(self) -> bool:
        """ลบ Food (CASCADE ลบ recipes ด้วย) — เทียบเท่า PHP Food::delete()"""
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("DELETE FROM foods WHERE id = ?", (self.id,))
            return cursor.rowcount > 0

    def exists(self) -> bool:
        """ตรวจสอบว่า id นี้มีอยู่จริง — เทียบเท่า PHP Food::exists()"""
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("SELECT id FROM foods WHERE id = ?", (self.id,))
            return cursor.fetchone() is not None

    # ---- Private Helpers ----

    def _validate(self) -> None:
        """เทียบเท่า PHP Food::validate() private method"""
        if not self.name_th:
            raise ValueError("nameTh is required")
        if not self.category:
            raise ValueError("category is required")

    @staticmethod
    def _serialize(row: dict) -> dict:
        """แปลง datetime object → string สำหรับ JSON response"""
        row["created_at"] = str(row["created_at"])
        row["updated_at"] = str(row["updated_at"])
        return row
