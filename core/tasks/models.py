from sqlalchemy import Column,String,Integer,Text,DateTime,Boolean,func,ForeignKey
from core.database import Base
from sqlalchemy.orm import relationship

class TaskModel(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(150), nullable=False)
    description = Column(Text(500), nullable=True)
    is_compelete = Column(Boolean, default=False)
    create_date = Column(DateTime, server_default=func.now())
    update_date = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
    
    users = relationship("UserModel", back_populates="tasks", uselist=False)
