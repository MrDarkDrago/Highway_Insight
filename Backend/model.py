from sqlalchemy import Column, Integer, String
from database import Base
from passlib.context import CryptContext

from sqlalchemy import Column, Integer, String
from database import Base
from passlib.context import CryptContext

# Initialize a CryptContext for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    def hash_password(self, plain_password: str):
        """Hash the password before storing it in the database"""
        self.password = pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        """Verify if the provided password matches the stored hash"""
        return pwd_context.verify(plain_password, self.password)
