# app.py
import streamlit as st
from datetime import datetime, date
import database as db

db.init_db()

st.set_page_config(page_title="스마트 냉장고 관리기", page_icon="🍅", layout="wide")
st.title("🍅 우리 집 스마트 냉장고")

# -----------------------------------------
# ⭐ [핵심 추가] 개인 냉장고 구분을 위한 이름 입력 칸
# -----------------------------------------
st.sidebar.subheader("👤 사용자 설정")
user_name = st.sidebar.text_input("닉네임이나 이름을 입력하세요", value="").strip()

if not user_name:
    st.warning("👈 왼쪽 사이드바에 이름을 입력해야 냉장고를 사용할 수 있습니다!")
    st.stop()

st.sidebar.success(f"현재 **{user_name}**님의 냉장고에 접속 중입니다.")

# -----------------------------------------
# [1] 상단 알림 배너 영역 (내 데이터만 조회)
# -----------------------------------------
st.subheader(f"🚨 {user_name}님의 소비기한 알림")
items = db.get_all_items(user_name)  # 💡 내 이름으로 된 것만 가져옴
today = date.today()
warning_count = 0

for item in items:
    exp_date = datetime.strptime(item[4], '%Y-%m-%d').date()
    days_left = (exp_date - today).days
    
    if days_left < 0:
        st.error(f"💀 **[{item[1]}]**의 소비기한이 {-days_left}일 지났습니다! 폐기를 검토하세요.")
        warning_count += 1
    elif 0 <= days_left <= 3:
        st.warning(f"⚠️ **[{item[1]}]**의 소비기한이 {days_left}일 남았습니다! 빨리 드세요.")
        warning_count += 1

if warning_count == 0:
    st.success("✅ 소비기한이 임박한 식재료가 없습니다. 안전합니다!")

st.markdown("---")

# -----------------------------------------
# [2] 화면 분할: 왼쪽(입력) / 오른쪽(목록)
# -----------------------------------------
col1, col2 = st.columns([1, 2])

# 카테고리별 보관 팁
STORAGE_TIPS = {
    "채소류": "신문지에 싸서 분무기로 물을 뿌린 후 냉장 보관하세요.",
    "육류": "올리브유를 살짝 바르고 랩으로 밀봉하여 냉동 또는 신선실에 보관하세요.",
    "어패류": "내장을 제거하고 씻은 뒤 물기를 제거하고 냉동 보관하세요.",
    "유제품": "온도 변화가 적은 냉장고 안쪽에 보관하고 개봉 후 빨리 섭취하세요.",
    "기타": "밀폐 용기에 담아 서늘한 곳이나 냉장 보관하세요."
}

# --- 왼쪽: 식재료 입력 폼 ---
with col1:
    st.subheader("📥 식재료 등록")
    category = st.selectbox("카테고리 선택", list(STORAGE_TIPS.keys()))
    st.info(f"💡 **{category} 추천 보관법:**\n{STORAGE_TIPS[category]}")
    
    with st.form("add_form", clear_on_submit=True):
        item_name = st.text_input("식재료 이름", placeholder="예: 방울토마토")
        expiry_date = st.date_input("소비기한 선택", min_value=today)
        storage_method = st.text_area("보관 방법 메모 (수정 가능)", value=STORAGE_TIPS[category])
        submit_btn = st.form_submit_button("냉장고에 넣기")
        
        if submit_btn:
            if item_name.strip() == "":
                st.error("식재료 이름을 입력해주세요.")
            else:
                # 💡 user_name(주인) 정보도 함께 넘겨서 저장합니다.
                db.add_item(user_name, item_name, category, expiry_date, storage_method)
                st.success(f"'{item_name}' 등록 완료!")
                st.rerun()

# --- 오른쪽: 냉장고 목록 조회 및 삭제 ---
with col2:
    st.subheader(f"❄️ {user_name}님의 냉장고 목록")
    if not items:
        st.info("냉장고가 비어 있습니다. 새로운 식재료를 등록해보세요!")
    else:
        for item in items:
            item_id, name, cat, ins_date, exp_date, tip = item
            
            with st.expander(f"🟢 {name} ({cat}) — 🗓️ 기한: {exp_date}"):
                st.write(f"**등록일:** {ins_date}")
                st.write(f"**보관 방법:** {tip}")
                
                if st.button("먹어서 없애기 (삭제)", key=f"del_{item_id}"):
                    db.delete_item(item_id)
                    st.success(f"'{name}'을(를) 맛있게 드셨군요!")
                    st.rerun()