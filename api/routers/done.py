# ------------------------------------------------------------
# 파일명: done.py
# 위치: api/routers/done.py
# 이 파일은 "할 일(To-Do)" 항목을 완료 상태로 만들거나
# 완료 상태를 해제하는 기능(API 경로)을 정의한다.
# - 기능 1: 완료 처리 (PUT)
# - 기능 2: 완료 해제 (DELETE)
# ------------------------------------------------------------

# * FastAPI에서 여러 URL 경로(API 주소)를 모아서 관리할 수 있도록 도와주는 도구
from fastapi import APIRouter

# * router 객체를 만든다
# - 여러 API 기능들을 이 안에 모아놓고 나중에 main.py에서 등록함
router = APIRouter()

# ------------------------------------------------------------
# [1] 할 일을 "완료 상태"로 표시하는 기능
# - 클라이언트가 /tasks/3/done으로 PUT 요청을 보내면,
#   3번 할 일을 "완료된 상태"로 변경한다.
# ------------------------------------------------------------
@router.put("/tasks/{task_id}/done", response_model=None)
# - method: PUT → 정보를 "수정"하거나 "상태를 변경"할 때 사용
# - /done : "완료 처리"를 의미하는 주소 패턴
# - {task_id} : 경로에 들어가는 숫자(할 일 번호), 예: 3
async def mark_task_as_done(task_id: int):
    return
    # * 실제 DB 연동 전이므로 구현 내용은 아직 없음 (나중에 작성)

# ------------------------------------------------------------
# [2] 할 일을 "완료 상태 해제"하는 기능
# - 클라이언트가 /tasks/3/done으로 DELETE 요청을 보내면,
#   3번 할 일을 "미완료 상태"로 되돌린다.
# ------------------------------------------------------------
@router.delete("/tasks/{task_id}/done", response_model=None)
# - method: DELETE → 데이터를 "지우거나 취소"할 때 사용
# - 여기서는 "완료 표시"를 해제(삭제)하는 의미로 사용
# - PUT과 DELETE는 서로 반대 동작 (완료 ↔ 해제)
async def unmark_task_as_done(task_id: int):
    return
    # * 실제 구현은 나중에 DB 연동 시 추가
