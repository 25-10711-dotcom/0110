import streamlit as st
import time

# 1. 페이지 기본 설정
st.set_page_config(page_title="나의 오운완 기록지", layout="centered")

# 디자인을 위한 CSS 주입
st.markdown("""
    <style>
    /* 전체 배경 스타일 */
    .stApp { background-color: #0f172a; color: #f8fafc; }
    
    /* 타이머 글씨 강조 */
    .timer-text { 
        font-size: 28px; 
        font-weight: bold; 
        color: #38bdf8; 
        text-align: center; 
        margin: 10px 0;
        padding: 15px;
        background-color: #1e293b;
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏋️‍♂️ 나의 오운완 기록지")

# 2. 데이터 세션 상태 초기화
if 'sets' not in st.session_state:
    st.session_state.sets = [
        {"set": 1, "weight": 60, "reps": 10, "completed": False},
        {"set": 2, "weight": 60, "reps": 10, "completed": False},
        {"set": 3, "weight": 60, "reps": 8, "completed": False},
    ]
if 'timer_start' not in st.session_state:
    st.session_state.timer_start = False
if 'timer_seconds' not in st.session_state:
    st.session_state.timer_seconds = 0

# 3. [기능] 타이머 작동 로직
if st.session_state.timer_start and st.session_state.timer_seconds > 0:
    timer_placeholder = st.empty()
    for idx in range(st.session_state.timer_seconds, -1, -1):
        if idx > 0:
            timer_placeholder.markdown(f"<div class='timer-text'>⏱ 휴식 중... {idx}초 남음</div>", unsafe_allow_html=True)
        else:
            timer_placeholder.markdown("<div class='timer-text'>🔥 휴식 완료! 다음 세트 준비!</div>", unsafe_allow_html=True)
        time.sleep(1)
    st.session_state.timer_start = False

# --- UI 화면 배치 ---

# [화면] 1. 타이머 수동 조절 섹션
with st.container(border=True):
    st.subheader("⏱ 쉬는 시간 타이머")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("+ 60초"):
            st.session_state.timer_seconds = 60
            st.session_state.timer_start = True
            st.rerun()  # 완벽 수정!
    with col2:
        if st.button("+ 90초"):
            st.session_state.timer_seconds = 90
            st.session_state.timer_start = True
            st.rerun()  # 완벽 수정!
    with col3:
        if st.button("정지"):
            st.session_state.timer_start = False
            st.session_state.timer_seconds = 0
            st.rerun()  # 완벽 수정!

st.markdown("---")

# [화면] 2. 운동 일지 섹션
st.markdown("### 🏋️‍♂️ Bench Press (벤치프레스)")

# 세트 리스트 출력 및 완료 체크
for i, s in enumerate(st.session_state.sets):
    status_emoji = "✅ 완료됨" if s["completed"] else "💪 성공"
    
    col_info, col_btn = st.columns([3, 1])
    with col_info:
        st.markdown(f"**{s['set']}세트** ㅤ|ㅤ {s['weight']} kg ㅤ|ㅤ {s['reps']} 회")
    with col_btn:
        if st.button(status_emoji, key=f"btn_{i}"):
            st.session_state.sets[i]["completed"] = not st.session_state.sets[i]["completed"]
            if st.session_state.sets[i]["completed"]:
                st.session_state.timer_seconds = 60
                st.session_state.timer_start = True
            st.rerun()  # 완벽 수정!

st.markdown("---")

# [화면] 3. 세트 추가 버튼
if st.button("➕ 세트 추가", use_container_width=True):
    last_set = st.session_state.sets[-1] if st.session_state.sets else {"set": 0, "weight": 40, "reps": 10}
    new_set = {
        "set": len(st.session_state.sets) + 1,
        "weight": last_set["weight"],
        "reps": last_set["reps"],
        "completed": False
    }
    st.session_state.sets.append(new_set)
    st.rerun()  # 완벽 수정!
