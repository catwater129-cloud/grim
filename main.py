import streamlit as st
import random
import re
import plotly.graph_objects as go

# ==========================================
# 1. 페이지 및 기본 스타일 설정 (CSS)
# ==========================================
st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍔", layout="centered")

st.markdown("""
<style>
    .stApp {
        background-color: #FFFFFF !important;
    }
    
    html, body, [class*="css"], div, span, p, label, h1, h2, h3, h4, h5, h6, input {
        color: #000000 !important;
    }
    
    .block-container {
        padding-top: 2rem !important;
    }
    
    .bg-clean-overlay, .bg-clean-full {
        background-color: #FFFFFF !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0px;
        text-align: center;
        margin-bottom: 20px;
    }

    .title-main {
        color: #000000 !important;
        font-size: 30px !important;
        font-weight: bold !important;
        text-align: center;
        margin-bottom: 15px;
    }
    
    .title-sub {
        color: #000000 !important;
        font-size: 22px !important;
        font-weight: bold !important;
        text-align: center;
        margin-bottom: 15px;
    }

    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #CCCCCC !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        width: 100%;
        box-shadow: none !important;
    }
    
    div.stButton > button:hover {
        background-color: #F0F0F0 !important;
        border-color: #000000 !important;
        color: #000000 !important;
    }

    .food-label {
        font-size: 16px !important;
        font-weight: bold !important;
        color: #000000 !important;
        text-align: center;
        margin-top: 6px;
        margin-bottom: 6px;
    }

    .stTextInput input {
        color: #000000 !important;
        border: 1px solid #000000 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 음식 매핑 이모지 및 데이터베이스 (각 10개)
# ==========================================
FOOD_EMOJI_DATABASE = {
    # 한식 (10개)
    "비빔밥": "🍲", "김치찌개": "🍲", "된장찌개": "🍲", "불고기": "🥩", "삼겹살": "🥓",
    "떡볶이": "🥘", "냉면": "🍜", "제육볶음": "🥩", "갈비탕": "🍲", "순두부찌개": "🍲",
    
    # 양식 (10개)
    "파스타": "🍝", "고르곤졸라 피자": "🍕", "스테이크": "🥩", "햄버거": "🍔", "리조또": "🍲",
    "돈까스": "🥩", "시저 샐러드": "🥗", "샌드위치": "🥪", "오믈렛": "🍳", "바비큐 립": "🍖",
    
    # 중식 (10개)
    "짜장면": "🍜", "짬뽕": "🍜", "탕수육": "🥢", "마라탕": "🍲", "만두": "🥟",
    "볶음밥": "🍛", "유린기": "🍗", "멘보샤": "🍞", "마파두부": "🍲", "양꼬치": "🍢",
    
    # 일식 (10개)
    "가츠동": "🍲", "라멘": "🍜", "초밥": "🍣", "우동": "🍜", "야키소바": "🍝",
    "메밀소바": "🍜", "사케동": "🍲", "텐동": "🍲", "오코노미야키": "🥞", "타코야키": "🧆",
    
    # 분식 (10개)
    "순대": "🍢", "김밥": "🍙", "라면": "🍜", "튀김": "🍤", "쫄면": "🍜",
    "핫도그": "🌭", "떡꼬치": "🍢", "어묵탕": "🍢", "비빔만두": "🥟", "치즈스틱": "🧀"
}

DEFAULT_EMOJI = "🍽️"

FOOD_DATA = {
    "한식": ["비빔밥", "김치찌개", "된장찌개", "불고기", "삼겹살", "떡볶이", "냉면", "제육볶음", "갈비탕", "순두부찌개"],
    "양식": ["파스타", "고르곤졸라 피자", "스테이크", "햄버거", "리조또", "돈까스", "시저 샐러드", "샌드위치", "오믈렛", "바비큐 립"],
    "중식": ["짜장면", "짬뽕", "탕수육", "마라탕", "만두", "볶음밥", "유린기", "멘보샤", "마파두부", "양꼬치"],
    "일식": ["가츠동", "라멘", "초밥", "우동", "야키소바", "메밀소바", "사케동", "텐동", "오코노미야키", "타코야키"],
    "분식": ["떡볶이", "순대", "김밥", "라면", "튀김", "쫄면", "핫도그", "떡꼬치", "어묵탕", "비빔만두"]
}

def get_best_emoji(food_name):
    cleaned_name = food_name.strip()
    if cleaned_name in FOOD_EMOJI_DATABASE:
        return FOOD_EMOJI_DATABASE[cleaned_name]
    
    for key, emoji in FOOD_EMOJI_DATABASE.items():
        if key in cleaned_name or cleaned_name in key:
            return emoji
            
    return DEFAULT_EMOJI

def render_food_emoji(food_name, font_size="80px"):
    emoji = get_best_emoji(food_name)
    st.markdown(
        f"""
        <div style="background-color: #F8F9FA; border-radius: 12px; height: 160px; display: flex; align-items: center; justify-content: center; border: 1px solid #EEEEEE; margin-bottom: 8px;">
            <div style="font-size: {font_size};">{emoji}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def get_plotly_roulette(items):
    fig = go.Figure(data=[go.Pie(
        labels=items,
        values=[1]*len(items),
        textinfo='label',
        hoverinfo='label',
        textfont=dict(size=16, color='black'),
        marker=dict(
            colors=['#FFF3CD', '#D1ECF1', '#D4EDDA', '#F8D7DA', '#E2E3E5', '#FFE699'],
            line=dict(color='#000000', width=1.5)
        ),
        sort=False,
        hole=0.15
    )])
    fig.update_layout(
        showlegend=False,
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=320
    )
    return fig

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
# 4. 화면 네비게이션
# ==========================================

# ------------------------------------------
# [화면 1] 시작 화면
# ------------------------------------------
if st.session_state.page == 'start':
    st.markdown('<div class="bg-clean-overlay">', unsafe_allow_html=True)
    st.markdown('<div class="title-main">🍔 오늘 뭐 먹지?</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-weight: bold; margin-bottom: 25px;">원하는 추천 모드를 선택해주세요</p>', unsafe_allow_html=True)
    
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
# [화면 2] 카테고리 선택
# ------------------------------------------
elif st.session_state.page == 'category':
    render_home_button()
    st.markdown("<h3 class='title-sub'>카테고리 선택</h3>", unsafe_allow_html=True)
    
    categories = ["한식", "양식", "중식", "일식", "분식"]
    for cat in categories:
        if st.button(cat, key=f"cat_{cat}"):
            st.session_state.selected_category = cat
            st.session_state.food_list = FOOD_DATA[cat].copy()
            st.session_state.page = 'food_select'
            st.rerun()

# ------------------------------------------
# [화면 3] 음식 제거 모드 (선택된 카테고리 10개 표시)
# ------------------------------------------
elif st.session_state.page == 'food_select':
    render_home_button()
    
    st.markdown("<p style='text-align: center; color: #000000; font-weight: bold; font-size: 16px;'>마음에 안 드는 메뉴를 눌러서 제거하세요!</p>", unsafe_allow_html=True)
    
    if len(st.session_state.food_list) == 1:
        st.session_state.final_result = st.session_state.food_list[0]
        st.session_state.page = 'result'
        st.rerun()

    cols = st.columns(2)
    for idx, item in enumerate(st.session_state.food_list):
        with cols[idx % 2]:
            render_food_emoji(item, font_size="70px")
            st.markdown(f'<div class="food-label">{item}</div>', unsafe_allow_html=True)
            if st.button("제거", key=f"del_{item}"):
                st.session_state.food_list.remove(item)
                st.rerun()

# ------------------------------------------
# [화면 4] 음식 이름 입력 (공백/쉼표 구분 다중 입력)
# ------------------------------------------
elif st.session_state.page == 'custom_input':
    render_home_button()
    
    st.markdown('<div class="bg-clean-full">', unsafe_allow_html=True)
    st.markdown('<div class="title-sub">먹을 음식의 이름을 작성해 주세요</div>', unsafe_allow_html=True)
    st.caption("※ 띄어쓰기(공백)로 구분하여 여러 메뉴를 한 번에 입력할 수 있습니다. (예: 짜장면 짬뽕 탕수육)")
    
    raw_input = st.text_input("음식 이름 입력", label_visibility="collapsed", placeholder="예: 짜장면 짬뽕 탕수육")
    
    col_add, col_empty = st.columns([3, 7])
    with col_add:
        if st.button("추가"):
            if raw_input.strip():
                parsed_items = [item.strip() for item in re.split(r'[\s,]+', raw_input) if item.strip()]
                for food in parsed_items:
                    if food not in st.session_state.custom_foods:
                        st.session_state.custom_foods.append(food)
                st.rerun()
                
    st.markdown("---")
    st.write("**현재 입력된 메뉴 목록:**")
    for idx, food in enumerate(st.session_state.custom_foods):
        col_f, col_d = st.columns([8, 2])
        with col_f:
            emoji = get_best_emoji(food)
            st.write(f"- {emoji} {food}")
        with col_d:
            if st.button("삭제", key=f"remove_custom_{food}_{idx}"):
                st.session_state.custom_foods.remove(food)
                st.rerun()

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
    
    st.plotly_chart(get_plotly_roulette(items), use_container_width=True)
    
    if st.button("돌리기"):
        selected = random.choice(items)
        st.session_state.final_result = selected
        st.session_state.page = 'result'
        st.rerun()

# ------------------------------------------
# [화면 6] 결과 화면
# ------------------------------------------
elif st.session_state.page == 'result':
    st.markdown('<div class="bg-clean-overlay">', unsafe_allow_html=True)
    
    result_food = st.session_state.final_result
    st.markdown("<h2 class='title-main'>🎉 오늘의 추천 음식!</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        render_food_emoji(result_food, font_size="90px")
    
    st.markdown(f'<div class="food-label" style="font-size: 22px !important;">{result_food}</div>', unsafe_allow_html=True)
    
    st.write("")
    if st.button("시작화면으로 돌아가기"):
        st.session_state.page = 'start'
        st.session_state.selected_category = None
        st.session_state.food_list = []
        st.session_state.custom_foods = []
        st.session_state.final_result = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
