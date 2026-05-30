# database.py 
import sqlite3
from datetime import datetime

# 💡 기존 "fridge.db"에서 "fridge_v2.db"로 이름을 바꿉니다! (새 집 짓기)
DB_NAME = "fridge_v2.db" 

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # 💡 owner(주인) 컬럼을 새로 추가했습니다.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fridge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner TEXT NOT NULL,
            item_name TEXT NOT NULL,
            category TEXT,
            insert_date TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            storage_method TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_item(owner, item_name, category, expiry_date, storage_method):
    """주인 이름을 함께 받아서 저장합니다."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    insert_date = datetime.today().strftime('%Y-%m-%d')
    cursor.execute("""
        INSERT INTO fridge (owner, item_name, category, insert_date, expiry_date, storage_method)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (owner, item_name, category, insert_date, str(expiry_date), storage_method))
    conn.commit()
    conn.close()

def get_all_items(owner):
    """현재 접속한 주인의 식재료만 쏙 골라서 가져옵니다."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, item_name, category, insert_date, expiry_date, storage_method 
        FROM fridge 
        WHERE owner = ? 
        ORDER BY expiry_date ASC
    """, (owner,))
    items = cursor.fetchall()
    conn.close()
    return items

def delete_item(item_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fridge WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()