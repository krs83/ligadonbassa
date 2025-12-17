from sqlalchemy.ext.asyncio import async_sessionmaker

from backend.src.database import engine


session_maker_admin = async_sessionmaker(engine, expire_on_commit=False)
