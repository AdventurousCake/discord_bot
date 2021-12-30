from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from db_init import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, nullable=False, unique=True, autoincrement=False)
    username = Column('username', String)
    data = Column('data', String, default=None)
    date = Column('date', DateTime)
    lvl = Column('lvl', Integer, default=1)
    msg_count = Column('msg_count', Integer, default=0)

    def __repr__(self):
        return f"<User {self.id}; {self.username}; {self.data, self.lvl, self.msg_count}; {self.date}>"