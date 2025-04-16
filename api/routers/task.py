# ------------------------------------------------------------
# 파일명: task.py
# 위치: api/routers/task.py
# 이 파일은 "할 일(To-Do)" 기능을 처리하는 API를 담고 있다.
# - FastAPI의 APIRouter를 사용하여 /tasks로 시작하는 주소들을 정의한다.
# - 주요 기능: 할 일 목록 조회, 추가, 수정, 삭제 (GET, POST, PUT, DELETE)
# ------------------------------------------------------------

# * FastAPI에서 URL 경로를 모아서 그룹으로 관리할 수 있도록 도와주는 도구
from fastapi import APIRouter

# * 우리가 만든 데이터 구조(Task 관련 클래스)를 불러온다
# - 파일 위치: api/schemas/task.py
# - 이 안에 Task, TaskCreate, TaskCreateResponse 등의 모델이 정의되어 있다.
import api.schemas.task as task_schema

# * router 객체를 만든다
# - 여러 API 기능들을 이 router 안에 담아서 나중에 main.py에서 등록하게 된다.
router = APIRouter()

# ------------------------------------------------------------
# [1] 할 일 목록 조회 (GET 요청)
# - 클라이언트가 /tasks 주소로 요청하면 전체 할 일 목록을 응답한다.
# ------------------------------------------------------------
@router.get("/tasks", response_model=list[task_schema.Task])
# - response_model: 클라이언트에게 어떤 형태로 응답할지 정의함
# - 여기서는 Task 모델의 리스트(list)를 반환한다.
async def list_tasks():
    return [task_schema.Task(id=1, title="첫 번째 ToDo 작업", done=False)]
    # * 실제 DB 연동 전에는 예시 데이터를 직접 만들어 응답함
    # * Pydantic 모델(Task)을 직접 사용해서 응답 데이터를 구성함

# ------------------------------------------------------------
# [2] 할 일 추가 (POST 요청)
# - 클라이언트가 JSON 형식으로 보낸 데이터를 받아 새로운 할 일을 만든다.
# ------------------------------------------------------------
@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
# - task_body: 클라이언트가 보낸 요청 본문 (예: {"title": "책 읽기"})
# - TaskCreate: 입력용 데이터 모델 (title 필드만 있음)
# - TaskCreateResponse: 응답용 모델 (id와 title 포함)
async def create_task(task_body: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=1, **task_body.model_dump())
    # * model_dump(): Pydantic v2에서 dict() 대신 사용되는 메서드
    # * 예시이므로 id는 1로 고정해서 반환

# ------------------------------------------------------------
# [3] 할 일 수정 (PUT 요청)
# - 특정 번호의 할 일을 수정함 (예: /tasks/3 요청 시, 3번 항목 수정)
# ------------------------------------------------------------
@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
# - task_id: 경로에 포함된 숫자 (수정할 할 일의 고유 번호)
# - task_body: 수정할 내용 (title만 전달됨)
async def update_task(task_id: int, task_body: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=task_id, **task_body.model_dump())
    # * 수정된 내용과 함께 같은 형식(TaskCreateResponse)으로 응답함

# ------------------------------------------------------------
# [4] 할 일 삭제 (DELETE 요청)
# - 특정 번호의 할 일을 삭제함 (예: /tasks/3 요청 시, 3번 항목 삭제)
# ------------------------------------------------------------
@router.delete("/tasks/{task_id}")
# - task_id: 삭제할 할 일의 번호
# - 별도의 응답 내용은 없음 (204 No Content 형식도 가능)
async def delete_task(task_id: int):
    return
