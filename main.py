import streamlit as st
import random
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io
import base64

# ==========================================
# 1. 페이지 및 기본 스타일 설정 (CSS)
# ==========================================
st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍔", layout="centered")

# 전체 글씨 색상을 연한 갈색(#A37D63)으로 변경하는 CSS 적용
st.markdown("""
<style>
    /* 기본 배경 설정 */
    .stApp {
        background-color: #F8F9FA;
    }
    
    /* 앱 내 모든 기본 텍스트 및 입력 필드 글씨 색상을 연한 갈색으로 고정 */
    html, body, [class*="css"], div, span, p, label, h1, h2, h3, h4, h5, h6, input {
        color: #A37D63 !important;
    }
    
    /* 시작화면 / 결과화면 반투명 연녹색 배경 */
    .bg-green-overlay {
        background-color: rgba(220, 245, 225, 0.85);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* 음식 이름 입력화면 녹색 배경 */
    .bg-green-full {
        background-color: #D4EDDA;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
    }

    /* 제목 스타일 (연한 갈색 적용) */
    .title-white {
        color: #A37D63 !important;
        font-size: 32px !important;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .title-brown {
        color: #A37D63 !important;
        font-size: 24px !important;
        font-weight: bold;
    }

    /* 공통 흰색 버튼 (글씨: 연갈색 #A37D63) */
    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #A37D63 !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        width: 100%;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }
    div.stButton > button:hover {
        background-color: #F0F0F0 !important;
        color: #8C664C !important;
    }

    /* 음식 텍스트 스타일: 연한 갈색 적용 */
    .food-label {
        font-size: 13px !important;
        font-weight: normal !important;
        color: #A37D63 !important;
        text-align: center;
        margin-top: 4px;
    }

    /* 결과화면 음식 이름 스타일 (연갈색, 작고 얇게) */
    .result-food-label {
        font-size: 15px !important;
        font-weight: normal !important;
        color: #A37D63 !important;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    /* 텍스트 입력창 내부 글자 색상 */
    .stTextInput input {
        color: #A37D63 !important;
    }

    /* 홈 버튼 정렬 */
    .home-btn-container {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 데이터 및 그래픽 생성 함수
# ==========================================

FOOD_DATA = {
    "한식": ["비빔밥", "김치찌개", "된장찌개", "불고기", "삼겹살", "갈비탕", "떡볶이", "삼계탕", "제육볶음", "순두부찌개", "냉면", "칼국수", "육개장", "닭갈비", "보쌈", "족발", "감자탕", "해물파전", "잡채", "계란말이"],
    "양식": ["파스타", "고르곤졸라 피자", "페퍼로니 피자", "스테이크", "리조또", "바베큐 립", "햄버거", "시저 샐러드", "클램 차우더", "라자냐", "에그 베네딕트", "감바스", "프렌치 토스트", "피쉬 앤 칩스", "크림 스프", "맥앤치즈", "옴렛", "퀘사디아", "수제버거", "고기 파이"],
    "중식": ["짜장면", "짬뽕", "탕수육", "볶음밥", "마파두부", "양꼬치", "깐풍기", "유린기", "멘보샤", "마라탕", "마라샹궈", "고추잡채", "동파육", "칠리새우", "크림새우", "울면", "잡채밥", "군만두", "딤섬", "누룽지탕"],
    "일식": ["돈까스", "라멘", "초밥", "가츠동", "규동", "우동", "소바", "야키토리", "타코야키", "오코노미야키", "사시미", "장어덮밥", "텐동", "나베", "메밀소바", "가라아게", "연어덮밥", "스키야키", "후토마키", "카레라이스"],
    "분식": ["떡볶이", "순대", "튀김", "김밥", "라면", "쫄면", "어묵", "떡꼬치", "라볶이", "소떡소떡", "치즈스틱", "만두", "야채튀김", "김말이", "참치김밥", "치즈김밥", "돈까스김밥", "비빔만두", "우동", "핫도그"]
}

def generate_food_icon(name):
    """인터넷 없이 플레이스홀더 음식 이미지를 생성하는 함수"""
    fig, ax = plt.subplots(figsize=(2, 2))
    fig.patch.set_facecolor('#F0F0F0')
    ax.set_facecolor('#FFFFFF')
    
    random.seed(sum(ord(c) for c in name))
    color = "#%06x" % random.randint(0, 0xFFFFFF)
    
    circle = patches.Circle((0.5, 0.5), 0.35, facecolor=color, edgecolor='#A37D63', linewidth=2)
    ax.add_patch(circle)
    ax.text(0.5, 0.5, name[0], fontsize=20, color='white', weight='bold', ha='center', va='center')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.05)
    plt.close(fig)
    return buf.getvalue()

def generate_roulette_image(items, selected_item=None):
    """돌림판 이미지를 matplotlib으로 그리는 함수 (글자색 연갈색 반영)"""
    fig, ax = plt.subplots(figsize=(4, 4))
    n = len(items)
    colors = ['#FFD1DC', '#FAFAD2', '#E0EEE0', '#E6E6FA', '#FFE4E1', '#F0F8FF']
    
    angles = [360 / n] * n
    start_angle = 90
    
    wedges, _ = ax.pie(
        angles, 
        startangle=start_angle, 
        colors=[colors[i % len(colors)] for i in range(n)],
        wedgeprops=dict(width=0.8, edgecolor='w', linewidth=2)
    )
    
    # 돌림판 내부 글씨 색상도 연한 갈색(#A37D63)으로 설정
    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = math.sin(math.radians(ang)) * 0.6
        x = math.cos(math.radians(ang)) * 0.6
        ax.text(x, y, items[i], ha='center', va='center', fontsize=9, color='#A37D63', weight='bold')
        
    ax.plot(0, 0.95, marker='v', markersize=15, color='#A37D63')
    
    ax.axis('equal')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    plt.close(fig)
    return buf.getvalue()

# ==========================================
# 3. 세션 상태 초기화
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = 'start'
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None
if 'food_list' not in st.session_state:
    st.session_state.food_list = []
if 'custom_foods' not in st.session_state:
    st.session_state.custom_foods = []
if 'final_result' not in st.session_state:
    st.session_state.final_result = None

def render_home_button():
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("🏠", key="home_btn"):
            st.session_state.page = 'start'
            st.rerun()

# ==========================================
# 4. 화면별 네비게이션
# ==========================================

# ------------------------------------------
# [화면 1] 시작 화면
# ------------------------------------------
if st.session_state.page == 'start':
    st.markdown('<div class="bg-green-overlay">', unsafe_allow_html=True)
    st.markdown('<div class="title-white">모드 선택</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("제거 모드"):
            st.session_state.page = 'category'
            st.rerun()
    with col2:
        if st.button("돌림판 모드"):
            st.session_state.page = 'custom_input'
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# [화면 2] 카테고리 화면
# ------------------------------------------
elif st.session_state.page == 'category':
    render_home_button()
    st.markdown("<h3 style='text-align: center; color: #A37D63;'>카테고리 선택</h3>", unsafe_allow_html=True)
    
    categories = ["한식", "양식", "중식", "일식", "분식"]
    for cat in categories:
        if st.button(cat, key=f"cat_{cat}"):
            st.session_state.selected_category = cat
            st.session_state.food_list = FOOD_DATA[cat].copy()
            st.session_state.page = 'food_select'
            st.rerun()

# ------------------------------------------
# [화면 3] 음식 제거 화면
# ------------------------------------------
elif st.session_state.page == 'food_select':
    render_home_button()
    
    st.markdown("<p style='text-align: center; color: #A37D63; font-weight: bold;'>마음에 안 드는 메뉴를 눌러서 제거하세요!</p>", unsafe_allow_html=True)
    
    if len(st.session_state.food_list) == 1:
        st.session_state.final_result = st.session_state.food_list[0]
        st.session_state.page = 'result'
        st.rerun()

    cols = st.columns(4)
    for idx, item in enumerate(st.session_state.food_list):
        with cols[idx % 4]:
            img_bytes = generate_food_icon(item)
            st.image(img_bytes, use_container_width=True)
            st.markdown(f'<div class="food-label">{item}</div>', unsafe_allow_html=True)
            if st.button("제거", key=f"del_{item}_{idx}"):
                st.session_state.food_list.remove(item)
                st.rerun()

# ------------------------------------------
# [화면 4] 음식 이름 입력 화면
# ------------------------------------------
elif st.session_state.page == 'custom_input':
    render_home_button()
    
    st.markdown('<div class="bg-green-full">', unsafe_allow_html=True)
    st.markdown('<div class="title-brown">먹을 음식의 이름을 작성해 주세요</div>', unsafe_allow_html=True)
    
    new_food = st.text_input("음식 이름 입력", label_visibility="collapsed", placeholder="예: 짜장면")
    col_add, col_empty = st.columns([3, 7])
    with col_add:
        if st.button("추가"):
            if new_food and new_food not in st.session_state.custom_foods:
                st.session_state.custom_foods.append(new_food)
                st.rerun()
                
    st.markdown("---")
    st.write("현재 입력된 메뉴 목록:")
    for food in st.session_state.custom_foods:
        st.write(f"- {food}")

    st.markdown('</div>', unsafe_allow_html=True)
    
    if len(st.session_state.custom_foods) >= 2:
        if st.button("확인"):
            st.session_state.page = 'roulette'
            st.rerun()
    else:
        st.caption("최소 2개 이상의 음식을 입력해야 확인 버튼을 누를 수 있습니다.")

# ------------------------------------------
# [화면 5] 돌림판 화면
# ------------------------------------------
elif st.session_state.page == 'roulette':
    render_home_button()
    
    items = st.session_state.custom_foods
    roulette_img = generate_roulette_image(items)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(roulette_img, use_container_width=True)
        if st.button("돌리기"):
            selected = random.choice(items)
            st.session_state.final_result = selected
            st.session_state.page = 'result'
            st.rerun()

# ------------------------------------------
# [화면 6] 결과 화면
# ------------------------------------------
elif st.session_state.page == 'result':
    st.markdown('<div class="bg-green-overlay">', unsafe_allow_html=True)
    
    result_food = st.session_state.final_result
    st.markdown("<h2 style='color: #A37D63; text-align: center;'>오늘의 추천 음식!</h2>", unsafe_allow_html=True)
    
    img_bytes = generate_food_icon(result_food)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(img_bytes, use_container_width=True)
    
    st.markdown(f'<div class="result-food-label">{result_food}</div>', unsafe_allow_html=True)
    
    if st.button("시작화면으로 돌아가기"):
        st.session_state.page = 'start'
        st.session_state.selected_category = None
        st.session_state.food_list = []
        st.session_state.custom_foods = []
        st.session_state.final_result = None
        st.rerun()

        
