import sqlalchemy as sa
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file):
    global __factory
    if __factory is not None:
        return
    if not db_file or not db_file.strip():
        raise ValueError("Необходимо указать файл БД")
    conn_str = f"sqlite:///{db_file.strip()}?check_same_tread=False"
    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)
    print(f"Подключение к БД: {conn_str} ...")
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
