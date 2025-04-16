# ------------------------------------------------------------
# 파일명: db.py
# 위치: api/db.py
# 이 파일은 FastAPI 앱에서 사용할 데이터베이스와 연결하고,
# 테이블 정의 및 세션 관리를 위한 기본 설정을 담고 있다.
# ------------------------------------------------------------

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# ------------------------------------------------------------
# [1] PostgreSQL에 연결할 주소 설정 (DB 접속 정보)
# 형식: postgresql+asyncpg://사용자:비밀번호@호스트/데이터베이스이름
# - postgresql+asyncpg : PostgreSQL에 비동기로 접속할 수 있게 해주는 형식
# - todo_user : DB 사용자 이름
# - 1234 : 사용자 비밀번호
# - localhost : 현재 컴퓨터에서 실행 중인 DB 서버
# - todo_db : 사용할 데이터베이스 이름
# ------------------------------------------------------------
DB_URL = "postgresql+asyncpg://todo_user:1234@localhost/todo_db"

# ------------------------------------------------------------
# [2] DB 엔진 생성
# - 엔진은 FastAPI와 PostgreSQL 사이를 연결해주는 역할을 한다.
# - echo=True : SQL 실행 내용을 터미널에 출력 (디버깅에 유용)
# ------------------------------------------------------------
db_engine = create_async_engine(DB_URL, echo=True)

# ------------------------------------------------------------
# [3] 세션(session) 설정
# - 세션은 DB와 데이터를 주고받을 수 있게 도와주는 통로이다.
# - autocommit=False : 자동 저장하지 않음 (commit()을 직접 호출해야 저장됨)
# - autoflush=False : 성능 향상을 위해 자동 반영하지 않음
# - class_=AsyncSession : 비동기 방식의 세션을 사용함
# ------------------------------------------------------------
db_session = sessionmaker(
    bind=db_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

# ------------------------------------------------------------
# [4] 테이블 생성을 위한 기본 클래스 정의
# - 이후에 만들 모든 테이블 클래스들은 Base를 상속받아야 한다.
# - 이 Base를 기준으로 실제 DB에 테이블을 생성할 수 있다.
# ------------------------------------------------------------
Base = declarative_base()

# ------------------------------------------------------------
# [5] FastAPI에서 사용할 DB 세션 생성 함수
# - get_db() 함수는 '의존성 주입(Dependency Injection)'에 사용된다.
# - API 요청이 들어올 때마다 새로운 세션을 만들고,
#   작업이 끝나면 자동으로 세션을 닫아준다.
# - async with : 비동기적으로 세션을 열고 관리함
# - yield : session을 외부로 넘기고, 함수 종료 시 자동 정리됨
# ------------------------------------------------------------
async def get_db():
    async with db_session() as session:
        yield session
