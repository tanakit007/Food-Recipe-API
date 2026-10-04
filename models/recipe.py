"""Recipe model and SQLite persistence operations."""
from __future__ import annotations
from contextlib import closing
from typing import Optional
from sqlite3 import Connection


class Recipe:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn
        self.id: int = 0
        self.food_id: int = 0
        self.recipe_name: str = ""
        self.quantity: float = 0.0
        self.unit_name: str = ""

    def get_all_by_food_id(self) -> list:
        """ดึง Recipes ทั้งหมดของ food_id — เทียบเท่า PHP Recipe::getAllByFoodId()"""
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(
            'SELECT id, food_id, "recipeName", quantity, "unitName", '
            "created_at, updated_at "
            "FROM recipes WHERE food_id = ? ORDER BY id",
                (self.food_id,),
            )
            rows = cursor.fetchall()
        return [self._serialize(dict(r)) for r in rows]

    def get_one(self) -> Optional[dict]:
        """ดึง Recipe เดี่ยวตาม id — เทียบเท่า PHP Recipe::getOne()"""
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(
            'SELECT id, food_id, "recipeName", quantity, "unitName", '
            "created_at, updated_at "
            "FROM recipes WHERE id = ?",
                (self.id,),
            )
            row = cursor.fetchone()
        return self._serialize(dict(row)) if row else None

    def create(self) -> int:
        """
        สร้าง Recipe ใหม่ คืน id ใหม่ — เทียบเท่า PHP Recipe::create()

        """
        self._validate()
        sql = """
            INSERT INTO recipes (food_id, "recipeName", quantity, "unitName")
            VALUES (?, ?, ?, ?)
        """
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql, (
                self.food_id,
                self.recipe_name,
                self.quantity,
                self.unit_name,
            ))
            self.id = cursor.lastrowid
        return self.id

    def update(self) -> bool:
        """อัปเดต Recipe คืน True/False — เทียบเท่า PHP Recipe::update()"""
        self._validate()
        sql = """
            UPDATE recipes
            SET "recipeName" = ?, quantity = ?, "unitName" = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(sql, (
                self.recipe_name,
                self.quantity,
                self.unit_name,
                self.id,
            ))
            return cursor.rowcount > 0

    def delete(self) -> bool:
        """ลบ Recipe — เทียบเท่า PHP Recipe::delete()"""
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("DELETE FROM recipes WHERE id = ?", (self.id,))
            return cursor.rowcount > 0

    def food_exists(self) -> bool:
        """ตรวจว่า food_id มีอยู่จริง — เทียบเท่า PHP Recipe::foodExists()"""
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("SELECT id FROM foods WHERE id = ?", (self.food_id,))
            return cursor.fetchone() is not None

    # ---- Private Helpers ----

    def _validate(self) -> None:
        """เทียบเท่า PHP Recipe::validate() private method"""
        if self.food_id <= 0:
            raise ValueError("food_id is required and must be positive")
        if not self.recipe_name:
            raise ValueError("recipeName is required")
        if self.quantity <= 0:
            raise ValueError("quantity must be greater than 0")
        if not self.unit_name:
            raise ValueError("unitName is required")

    @staticmethod
    def _serialize(row: dict) -> dict:
        """แปลง datetime + float สำหรับ JSON response"""
        row["quantity"]   = float(row["quantity"])
        row["created_at"] = str(row["created_at"])
        row["updated_at"] = str(row["updated_at"])
        return row
