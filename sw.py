import streamlit as st
import time

# 1. 페이지 기본 설정 및 모바일 스타일 입히기
st.set_page_config(page_title="나의 오운완 기록지", layout="centered")

# Streamlit 내부에 CSS 디자인을 안전하게 주입하는 방법
st.markdown("""
    <style>
    /* 전체 배경과 카드 스타일 */
    .stApp { background-color: #0f172a; color: #f8fafc; }
    div[data-testid="stCard"] {
        background-color: #1e293b;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    /* 타이머 글씨 강조 */
    .timer-text { font-size: 32px; font-weight: bold; color: #38bdf8; text-align: center; margin: 10px 0; }
    </style>
""", unsafe_allow_index=True)

st.title("🏋️‍♂️ 나의 오운완 기록지")

# 2. 데이터 세션 상태 초기화 (새로고침해도 데이터가 유지되도록)
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
    # 대기 시간을 실시간으로 줄여가며 표시
    for idx in range(st.session_state.timer_seconds, -1, -1):
        timer_placeholder.markdown(f"<div class='timer-text'>⏱ 휴식 중... {idx}초 남음</div>", unsafe_allow_index=True)
        time.sleep(1)
    timer_placeholder.markdown("<div class='timer-text'>🔥 휴식 완료! 다음 세트 준비!</div>", unsafe_allow_index=True)
    st.session_state.timer_start = False # 타이머 종료 시 플래그 리셋

# --- UI 화면 배치 ---

# [화면] 1. 타이머 수동 조절 섹션
with st.container(border=True):
    st.subheader("⏱ 쉬는 시간 타이머")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("+ 60초"):
            st.session_state.timer_seconds = 60
            st.session_state.timer_start = True
            st.rerun()
    with col2:
        if st.button("+ 90초"):
            st.session_state.timer_seconds = 90
            st.session_state.timer_start = True
            st.rerun()
    with col3:
        if st.button("정지"):
            st.session_state.timer_start = False
            st.session_state.timer_seconds = 0
            st.rerun()

# [화면] 2. 운동 일지 섹션
st.markdown("###  Bench Press (벤치프레스)")

# 세트 리스트 출력 및 완료 체크
for i, s in enumerate(st.session_state.sets):
    # 완료 여부에 따라 배경 느낌을 다르게 주기 위해 이모지 활용
    status_emoji = "✅ 완료됨" if s["completed"] else "💪 성공"
    
    col_info, col_btn = st.columns([3, 1])
    with col_info:
        st.markdown(f"**{s['set']}세트** ㅤ|ㅤ {s['weight']} kg ㅤ|ㅤ {s['reps']} 회")
    with col_btn:
        # 각 세트의 성공/완료 버튼
        if st.button(status_emoji, key=f"btn_{i}"):
            st.session_state.sets[i]["completed"] = not st.session_state.sets[i]["completed"]
            # 성공으로 변경할 때만 자동으로 60초 타이머 트리거
            if st.session_state.sets[i]["completed"]:
                st.session_state.timer_seconds = 60
                st.session_state.timer_start = True
            st.rerun()

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
    st.rerun()
