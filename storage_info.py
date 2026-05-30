# storage_info.py 예시 코드
import json

def get_storage_info(ingredient_name):
    """
    사용자가 UI에서 재료명을 검색했을 때, 
    전처리된 JSON에서 해당 재료의 보관 정보를 찾아 반환하는 함수
    """
    try:
        with open('cleaned_ingredients.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # 사용자가 입력한 재료명과 일치하는 데이터 찾기
        for item in data:
            if item['name'] == ingredient_name:
                return item # {name: '사과', storage_method: '냉장보관'} 반환
                
        return {"message": "해당 재료의 정보가 없습니다."}
        
    except FileNotFoundError:
        return {"message": "전처리된 데이터 파일이 존재하지 않습니다."}