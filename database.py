import sqlite3
import json
import os
from datetime import datetime

# DB 파일 이름을 하나로 통일합니다.
DB_NAME = "fridge.db"

def init_db():
    """데이터베이스와 fridge 테이블을 초기화하는 함수"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # app.py와 컬럼명을 일치시킵니다 (item_name, category 등)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fridge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT,
            insert_date TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            storage_method TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ 데이터베이스 및 'fridge' 테이블 생성 완료!")

def load_preprocessed_data():
    """STEP 2에서 만든 cleaned_ingredients.json 데이터를 DB에 넣는 함수"""
    input_path = 'cleaned_ingredients.json'
    
    if not os.path.exists(input_path):
        print(f"⚠️ {input_path} 파일이 없어서 초기 데이터를 채우지 못했습니다. 전처리를 먼저 확인하세요.")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        ingredients = json.load(f)
        
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 기존에 데이터가 있는지 확인 (중복 방지)
    cursor.execute("SELECT COUNT(*) FROM fridge")
    if cursor.fetchone()[0] > 0:
        print("💡 DB에 이미 데이터가 존재하여 초기화(Insert)를 건너뜁니다.")
        conn.close()
        return

    # 전처리된 데이터를 테이블에 삽입 (app.py 구조에 맞춤)
    insert_date = datetime.today().strftime('%Y-%m-%d')
    # 전처리 데이터는 임시로 소비기한을 오늘부터 7일 뒤로 설정 (추후 앱에서 수정 가능)
    default_expiry = datetime.today().strftime('%Y-%m-%d') 

    for item in ingredients:
        name = item.get('name')
        storage_method = item.get('storage_method', '기본 보관법')
        category = item.get('category', '기타') # 카테고리 정보가 없다면 '기타'
        
        cursor.execute('''
            INSERT INTO fridge (item_name, category, insert_date, expiry_date, storage_method)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, category, insert_date, default_expiry, storage_method))
        
    conn.commit()
    conn.close()
    print(f"🎉 {len(ingredients)}개의 전처리 데이터가 DB에 안전하게 저장되었습니다!")

# -----------------------------------------------------
# ⭐ app.py에서 사용하는 필수 함수들 (이 부분이 빠져서 에러가 났던 것입니다!)
# -----------------------------------------------------

def add_item(item_name, category, expiry_date, storage_method):
    """앱에서 사용자가 직접 식재료를 추가할 때 실행되는 함수"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    insert_date = datetime.today().strftime('%Y-%m-%d')
    cursor.execute("""
        INSERT INTO fridge (item_name, category, insert_date, expiry_date, storage_method)
        VALUES (?, ?, ?, ?, ?)
    """, (item_name, category, insert_date, str(expiry_date), storage_method))
    conn.commit()
    conn.close()

def get_all_items():
    """앱에서 전체 식재료 목록을 화면에 그릴 때 실행되는 함수"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, item_name, category, insert_date, expiry_date, storage_method FROM fridge ORDER BY expiry_date ASC")
    items = cursor.fetchall()
    conn.close()
    return items

def delete_item(item_id):
    """앱에서 '먹어서 없애기' 버튼을 눌렀을 때 실행되는 함수"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fridge WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

# 파일 실행 시 최초 1회 작동
if __name__ == "__main__":
    init_db() 