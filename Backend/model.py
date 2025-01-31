from sqlalchemy import Column, Integer, String
from database import Base
from passlib.context import CryptContext

# Initialize a CryptContext for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "human"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    def verify_password(self, password: str) -> bool:
        """Verify if the password is correct"""
        return pwd_context.verify(password, self.password)

    def hash_password(self):
        """Hash the password before storing it in the database"""
        self.password = pwd_context.hash(self.password)


