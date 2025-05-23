import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
import sys

ECHO = "True"  # todo development

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")
    if sys.platform.startswith("win"):
        conn_str = f"sqlite:///{db_file.strip()}?check_same_thread=False&echo={ECHO}"
    else:
        conn_str = f"sqlite:////{db_file.strip()}?check_same_thread=False&echo={ECHO}"
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(
        conn_str, echo=False, pool_size=20, max_overflow=20, pool_timeout=10
    )
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
