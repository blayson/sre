from contextvars import ContextVar

import databases
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, Session

from app.settings import settings

database = databases.Database(settings.database_url)

# Base = automap_base(metadata=metadata)

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = automap_base()

# Base.prepare(engine, reflect=True)

metadata = MetaData()
# there is a way to reflect only some tables ```only=['users', 'user_roles', 'reviews', 'feature_names', 'products']```
metadata.reflect(engine)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()


db_session: ContextVar[Session] = ContextVar('db_session')
