<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>나의 오운완 기록지</title>
    <style>
        /* 기본 스타일 및 다크모드 테마 */
        body {
            font-family: 'Noto Sans KR', sans-serif;
            background-color: #0f172a;
            color: #f8fafc;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }

        .container {
            width: 100%;
            max-width: 430px; /* 모바일 화면 최적화 */
        }

        /* 타이머 카드 */
        .card {
            background-color: #1e293b;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            text-align: center;
        }

        .card-title {
            margin: 0 0 10px 0;
            font-size: 16px;
            color: #94a3b8;
        }

        .timer-display {
            font-size: 36px;
            font-weight: bold;
            margin: 15px 0;
            color: #38bdf8;
        }

        .btn-group {
            display: flex;
            justify-content: center;
            gap: 10px;
        }

        button {
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-sm {
            padding: 8px 16px;
            background-color: #475569;
            color: #fff;
        }

        .btn-danger {
            padding: 8px 16px;
            background-color: #ef4444;
            color: #fff;
        }

        /* 운동 기록 리스트 */
        .workout-title {
            font-size: 20px;
            text-align: left;
            margin: 0 0 20px 0;
        }

        .set-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 20px;
        }

        .set-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px;
            background-color: #334155;
            border-radius: 10px;
            transition: background-color 0.3s;
        }

        .set-row.completed {
            background-color: #1e293b;
            opacity: 0.6;
        }

        .set-info {
            font-size: 16px;
            font-weight: 500;
        }

        .btn-check {
            padding: 8px 16px;
            background-color: #64748b;
            color: #fff;
            width: 80px;
        }

        .btn-check.active {
            background-color: #10b981;
        }

        .btn-add {
            width: 100%;
            padding: 14px;
            background-color: #3b82f6;
            color: #fff;
            font-size: 16px;
        }

        button:active {
            transform: scale(0.98);
        }
    </style>
</head>
<body>

    <div class="container">
        <div class="card">
            <div class="card-title">⏱ 쉬는 시간 타이머</div>
            <div class="timer-display" id="timerDisplay">휴식 완료! 다음 세트 준비🔥</div>
            <div class="btn-group">
                <button class="btn-sm" onclick="startTimer(60)">+ 60초</button>
                <button class="btn-sm" onclick="startTimer(90)">+ 90초</button>
                <button class="btn-danger" onclick="stopTimer()">정지</button>
            </div>
        </div>

        <div class="card" style="text-align: left;">
            <div class="workout-title">🏋️‍♂️ 가슴 - 벤치프레스</div>
            <div class="set-list" id="setList">
                </div>
            <button class="btn-add" onclick="addSet()">+ 세트 추가</button>
        </div>
    </div>

    <script>
        // 초기 운동 데이터 세팅
        let sets = [
            { id: 1, weight: 60, reps: 10, completed: false },
            { id: 2, weight: 60, reps: 10, completed: false },
            { id: 3, weight: 60, reps: 8, completed: false }
        ];

        let timerInterval = null;
        let timeLeft = 0;

        // 화면에 세트 리스트를 그려주는 함수
        function renderSets() {
            const setListEl = document.getElementById('setList');
            setListEl.innerHTML = '';

            sets.forEach((set, index) => {
                const row = document.createElement('div');
                row.className = `set-row ${set.completed ? 'completed' : ''}`;

                row.innerHTML = `
                    <span class="set-info">${index + 1}세트</span>
                    <span class="set-info">${set.weight} kg</span>
                    <span class="set-info">${set.reps} 회</span>
                    <button class="btn-check ${set.completed ? 'active' : ''}" onclick="toggleSet(${set.id})">
                        ${set.completed ? '완료 ✓' : '성공'}
                    </button>
                `;
                setListEl.appendChild(row);
            });
        }

        // 성공 버튼 클릭 시 상태 변경 및 타이머 연동
        function toggleSet(id) {
            sets = sets.map(set => {
                if (set.id === id) {
                    const nextState = !set.completed;
                    if (nextState) {
                        startTimer(60); // 성공 체크 시 자동으로 60초 타이머 시작
                    }
                    return { ...set, completed: nextState };
                }
                return set;
            });
            renderSets();
        }

        // 새 세트 추가 기능 (이전 세트 정보 복사)
        function addSet() {
            const lastSet = sets[sets.length - 1];
            const newSet = {
                id: Date.now(), // 고유 ID 생성
                weight: lastSet ? lastSet.weight : 40,
                reps: lastSet ? lastSet.reps : 10,
                completed: false
            };
            sets.push(newSet);
            renderSets();
        }

        // 타이머 시작 함수
        function startTimer(seconds) {
            clearInterval(timerInterval);
            timeLeft = seconds;
            updateTimerDisplay();

            timerInterval = setInterval(() => {
                timeLeft--;
                updateTimerDisplay();

                if (timeLeft <= 0) {
                    clearInterval(timerInterval);
                    document.getElementById('timerDisplay').innerText = "휴식 완료! 다음 세트 준비🔥";
                    // 모바일 기기 진동 피드백 (지원하는 브라우저만)
                    if (navigator.vibrate) navigator.vibrate([200, 100, 200]);
                }
            }, 1000);
        }

        // 타이머 정지 함수
        function stopTimer() {
            clearInterval(timerInterval);
            document.getElementById('timerDisplay').innerText = "타이머 정지됨";
        }

        // 타이머 글자 업데이트
        function updateTimerDisplay() {
            document.getElementById('timerDisplay').innerText = `${timeLeft}초`;
        }

        // 첫 페이지 로드 시 실행
        renderSets();
    </script>
</body>
</html>
