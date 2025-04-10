# ------------------------------------------------------------
# 할 일(Task)을 표현하는 데이터 구조 정의
# 이 구조는 서버에서 주고받을 할 일 데이터의 모양을 정하는 것이다.
# ------------------------------------------------------------

from pydantic import BaseModel, Field  # 데이터를 깔끔하게 다루기 위한 도구를 불러온다.
# pydantic: 우리가 정의한 자료가 숫자인지 글자인지 자동으로 확인해주는 도구다.

class Task(BaseModel):  # '할 일'을 표현할 수 있는 Task라는 틀을 만든다.

    id: int  # 할 일 번호 (정수)

    title: str | None = Field(
        None,  # 아무 값이 없을 수도 있으니 기본값은 None으로 둔다.
        examples=["세탁소에 맡긴 것을 찾으러 가기"]  # 예시 제목을 보여준다.
    )
    # title: 할 일의 제목
    # str 또는 None → 글자이거나 비어 있을 수도 있다.

    done: bool = Field(
        False,  # 처음에는 '완료되지 않음(False)'으로 시작한다.
        description="True면 완료, False면 미완료"  # 무슨 뜻인지 설명해준다.
    )
    # done: 이 할 일이 끝났는지를 표시하는 값 (True 또는 False만 가능함)

class TaskBase(BaseModel):
    title: str | None = Field(
        None,
        examples=["세탁소에 맡긴 것을 찾으러 가기"]
    )

class Task
