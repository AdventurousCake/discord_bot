from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
import config

engine = create_async_engine(f"postgresql+asyncpg://{config.user}:{config.password}@{config.host}/{config.db_name}", future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()