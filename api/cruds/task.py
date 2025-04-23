# ------------------------------------------------------------
# 파일명: task.py
# 위치: api/cruds/task.py
# 이 파일은 "할 일(Task)" 관련 데이터 처리 기능(CRUD)을 정의한 곳이다.
# FastAPI의 API 요청을 받아서 실제 DB에 데이터를 저장하거나 불러오는
# 역할을 하는 함수들이 이 파일에 정의된다.
# ------------------------------------------------------------

# ------------------------------------------------------------
# [ import 구문 ]
# 데이터베이스 세션과 Task 모델, Task 스키마를 불러온다.
# ------------------------------------------------------------

# * Session:
#   - SQLAlchemy에서 DB 작업을 할 때 사용하는 "동기 세션" 객체이다.
#   - 여기서는 비동기(AsyncSession)가 아닌, 일반적인 동기 방식(Session)을 사용하고 있다.
#   - 즉, FastAPI 자체는 비동기 프레임워크지만, 이 예시에서는 DB 작업을 동기 방식으로 처리하고 있다.
# * task_model:
#   - 실제 DB에 저장되는 Task 클래스가 정의되어 있음
# * task_schema:
#   - 사용자로부터 받은 요청 데이터를 담는 클래스가 정의되어 있음
from sqlalchemy.orm import Session
import api.models.task as task_model
import api.schemas.task as task_schema

# ------------------------------------------------------------
# [ 함수: create_task ]
# 새로운 할 일(Task)을 DB에 저장하는 기능을 한다.
# - 클라이언트가 보낸 할 일 정보를 받아서
# - Task 모델 객체로 만들고, DB에 저장한 뒤
# - 저장된 객체를 다시 반환해준다.
# ------------------------------------------------------------

# * 함수 선언에서 사용한 "-> task_model.Task" 설명:
#   - "이 함수는 실행 결과로 task_model.Task 자료형을 반환한다"는 뜻이다.
#   - 파이썬에서는 이런 형식 힌트(type hint)를 통해 코드의 의도를 더 분명하게 표현할 수 있다.
#   - 실제 작동에는 영향이 없고, 읽는 사람(또는 자동완성 도구)에게 도움을 준다.

# * 매개변수:
#   - db: SQLAlchemy 세션 객체 (데이터베이스와 연결된 상태)
#   - task_create: 사용자가 보낸 새 할 일 정보 (task_schema.TaskCreate 타입)

# * 반환값:
#   - 실제 DB에 저장된 Task 객체
def create_task(db: Session, task_create: task_schema.TaskCreate) -> task_model.Task:
    # 사용자가 보낸 데이터(task_create)를 바탕으로 Task 모델 객체를 만든다

    # - task_create.model_dump(): task_create 스키마 객체의 값을 딕셔너리로 꺼내준다
    #   예: {"title": "공부하기", "done": False}
    #
    # - Task(**딕셔너리): 딕셔너리의 key-value를 풀어서
    #   Task(title="공부하기", done=False)처럼 전달한다
    #
    # - 여기서 **는 파이썬 문법으로, 딕셔너리를 "키=값" 형태로 분해해서 넣어주는 기능이다.
    #   자바스크립트의 {...객체}처럼 펼쳐 넣는 느낌이다.
    task = task_model.Task(**task_create.model_dump())

    # 만든 Task 객체를 DB에 추가한다
    db.add(task)

    # 실제로 DB에 저장되도록 확정(commit)한다
    db.commit()

    # 방금 커밋한 Task 객체의 최신 상태를 DB에서 다시 불러온다
    # - 이유: DB가 자동으로 만들어준 id, 날짜(created_at 등)가 있을 수 있기 때문
    # - refresh()를 안 하면 task.id 같은 값이 비어있을 수 있음
    db.refresh(task)

    # 최종적으로 저장된 Task 객체를 반환한다
    return task
