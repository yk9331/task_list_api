# Import all the models, so that Base has them before being
# imported by Alembic for 'autogenerate' support

import src.models  # noqa
from src.db.base_class import Base  # noqa
