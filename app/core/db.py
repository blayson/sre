import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

from app.settings import settings

# metadata.reflect(engine)  # only=['users', 'user_roles', 'reviews', 'feature_names', 'products'])
# Base = automap_base(metadata=metadata)

engine = create_engine(settings.database_url)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = automap_base()

Base.prepare(engine, reflect=True)

database = databases.Database(settings.database_url)
