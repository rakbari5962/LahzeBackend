from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context


config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)



from app.database.database import Base


from app.models.user import User
from app.models.business import Business
from app.models.service import Service
from app.models.invitation import Invitation
from app.models.opportunity import Opportunity
from app.models.province import Province
from app.models.city import City
from app.models.booking import Booking
from app.models.notification import Notification
from app.models.review import Review
from app.models.review_request import ReviewRequest
from app.models.reward_event import RewardEvent
from app.models.account import Account
from app.models.ledger import LedgerEntry
from app.models.financial_transaction import FinancialTransaction
from app.models.business_priority_access import BusinessPriorityAccess



target_metadata = Base.metadata





def run_migrations_offline() -> None:

    url = config.get_main_option("sqlalchemy.url")

    context.configure(

        url=url,

        target_metadata=target_metadata,

        literal_binds=True,

        dialect_opts={"paramstyle": "named"},

    )


    with context.begin_transaction():

        context.run_migrations()







def run_migrations_online() -> None:


    connectable = engine_from_config(

        config.get_section(config.config_ini_section, {}),

        prefix="sqlalchemy.",

        poolclass=pool.NullPool,

    )


    with connectable.connect() as connection:


        context.configure(

            connection=connection,

            target_metadata=target_metadata

        )


        with context.begin_transaction():

            context.run_migrations()







if context.is_offline_mode():

    run_migrations_offline()

else:

    run_migrations_online()