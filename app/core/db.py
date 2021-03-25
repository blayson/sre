import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

from app.settings import settings

# metadata.reflect(engine)  # only=['users', 'user_roles', 'reviews', 'feature_names', 'products'])
# Base = automap_base(metadata=metadata)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)

Base = automap_base()

Base.prepare(engine, reflect=True)

database = databases.Database(settings.SQLALCHEMY_DATABASE_URL)


