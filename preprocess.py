import json
import os

def preprocess_data():
    input_path = 'ingredients_final.json'
    output_path = 'cleaned_ingredients.json'
    
    if not os.path.exists(input_path):
        print(f"❌ 에러: {input_path} 파일이 없습니다!")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    cleaned_data = []
    
    # 데이터가 어떤 형태든 다 받아내는 안전한 루프
    for item in raw_data:
        # 1. 만약 데이터가 그냥 글자("사과")라면
        if isinstance(item, str):
            name = item.strip()
            storage_method = "기본 보관법"
        
        # 2. 만약 데이터가 딕셔너리({"name": "사과"})라면
        elif isinstance(item, dict):
            name = item.get('name', '').strip() if item.get('name') else '이름없음'
            storage_method = item.get('storage_method', '기본 보관법').strip()
            
        else:
            continue
            
        if name:
            cleaned_data.append({
                'name': name,
                'storage_method': storage_method
            })
        
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
        
    print(f"🎉 전처리 완료! {len(cleaned_data)}개의 데이터가 {output_path}에 저장되었습니다.")

if __name__ == "__main__":
    preprocess_data()