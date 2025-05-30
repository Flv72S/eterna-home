from sqlalchemy.ext.declarative import declarative_base

# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.session import Base  # noqa
from app.models.user import User  # noqa

Base = declarative_base()

