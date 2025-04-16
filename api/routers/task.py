# ------------------------------------------------------------
# 파일명: task.py
# 위치: api/routers/task.py
# 이 파일은 "할 일(To-Do)" 기능을 처리하는 API를 정의한 곳이다.
# - /tasks로 시작하는 주소들을 FastAPI의 APIRouter로 관리한다.
# - 주요 기능: 할 일 목록 조회, 할 일 추가, 수정, 삭제
# - 아직 실제 DB는 연결하지 않고, 예시 데이터를 사용한다.
# ------------------------------------------------------------

# * FastAPI에서 여러 개의 URL 경로를 그룹으로 묶어 관리할 수 있게 해주는 도구
from fastapi import APIRouter

# * 우리가 정의한 데이터 구조를 불러온다 (파일 위치: api/schemas/task.py)
# - Task: 전체 할 일 데이터를 표현
# - TaskCreate: 사용자가 보낼 입력 데이터 구조
# - TaskCreateResponse: 응답할 때 사용할 데이터 구조 (id 포함)
import api.schemas.task as task_schema

# * router 객체를 만든다
# - task 목록과 관련된 여러 기능을 이 객체에 모두 담아서
#   나중에 main.py에서 FastAPI 앱에 등록하게 된다.
router = APIRouter()

# ------------------------------------------------------------
# [1] 할 일 목록 조회 (GET 요청)
# - 클라이언트가 /tasks 주소로 요청하면 전체 할 일 목록을 반환한다.
# - 아직 DB는 연결하지 않았기 때문에 임시 데이터만 보여준다.
# ------------------------------------------------------------
@router.get("/tasks", response_model=list[task_schema.Task])
# - response_model: 응답의 데이터 형태를 지정함
# - 여기서는 Task 모델을 여러 개 담은 리스트를 반환한다고 지정함
async def list_tasks():
    return [
        task_schema.Task(id=1, title="첫 번째 ToDo 작업", done=False)
    ]
    # * Task 모델 형식에 맞는 임시 데이터를 리스트 형태로 만들어 반환함
    # * 실제 DB 연동 시에는 DB에서 데이터를 꺼내서 여기에 넣을 예정

# ------------------------------------------------------------
# [2] 할 일 추가 (POST 요청)
# - 클라이언트가 JSON 형식으로 보낸 데이터(title)를 받아
#   새로운 할 일을 생성하는 기능 (예: {"title": "책 읽기"})
# ------------------------------------------------------------
@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
# - task_body: 사용자가 보낸 데이터 요청 본문
# - TaskCreate: 사용자가 보낸 데이터(title만 포함됨)
# - TaskCreateResponse: 응답할 때 포함할 데이터(id 포함)
async def create_task(task_body: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=1, **task_body.model_dump())
    # * model_dump()는 Pydantic v2에서 dict() 대신 사용하는 메서드
    # * task_body에 들어 있는 값을 풀어서(id와 함께) 응답으로 전달함
    # * 지금은 예시이므로 id는 1로 고정해두었음

# ------------------------------------------------------------
# [3] 할 일 수정 (PUT 요청)
# - 경로에 포함된 번호(task_id)에 해당하는 할 일을 수정함
# - 클라이언트가 수정할 내용을 JSON으로 보내면 title을 바꿔주는 역할
# ------------------------------------------------------------
@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
# - task_id: URL 경로에 포함된 숫자 (수정 대상 할 일 번호)
# - task_body: 수정할 내용을 담은 요청 본문 (title)
async def update_task(task_id: int, task_body: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=task_id, **task_body.model_dump())
    # * id는 수정 대상 번호 그대로 사용
    # * 수정된 title과 함께 응답 구조(TaskCreateResponse)로 반환

# ------------------------------------------------------------
# [4] 할 일 삭제 (DELETE 요청)
# - /tasks/번호 형식으로 요청이 오면 해당 번호의 할 일을 삭제함
# - 이 함수는 아직 DB가 없기 때문에 동작은 하지 않지만 구조만 정의함
# ------------------------------------------------------------
@router.delete("/tasks/{task_id}")
# - task_id: 삭제할 할 일의 번호
# - response_model이 없으므로 별도 응답 내용 없이 처리 가능 (204 No Content)
async def delete_task(task_id: int):
    return
    # * 실제 구현에서는 삭제 후 상태 코드나 메시지를 반환할 수 있음
