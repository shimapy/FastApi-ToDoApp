from sqlalchemy import Column,String,Integer,DateTime,Boolean,func,ForeignKey
from passlib.context import CryptContext
from sqlalchemy.orm import relationship
from core.database import Base

# ایجاد یک شیء برای Hash کردن رمز عبور
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(250), nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    create_date = Column(DateTime, server_default=func.now())
    update_date = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
    
    tasks = relationship("TaskModel", back_populates="users")
    
    # متد برای هش کردن رمز عبور
    def hash_password(self, plain_password: str) -> str:
        """Hashes the given password using bcrypt."""
        return pwd_context.hash(plain_password)

    # متد برای اعتبارسنجی رمز عبور
    def verify_password(self, plain_password: str) -> bool:
        """Verifies the given password against the stored hash."""
        return pwd_context.verify(plain_password, self.password)
    
    def set_password(self, plain_text: str)-> None:
        self.password = self.hash_password(plain_text)
        
# روش سوم >> Token Basic  Authentication >> این کلاس برای روش سوم احراز هویت ایجاد شد
class TokenModel(Base):
    __tablename__ = "tokens"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, nullable=False)
    create_date = Column(DateTime, server_default=func.now())
    
    user =relationship("UserModel",uselist=False)
