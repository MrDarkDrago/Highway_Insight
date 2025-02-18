from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from model import User
from schemas import CityName,UserCreate
from typing import List, Optional
from sqlalchemy import text

# Initialize FastAPI app
app = FastAPI()

# Define base directories
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "Frontend"
BACKEND_DIR = BASE_DIR.parent / "Backend"

# Define subdirectories for static files
ASSETS_DIR = FRONTEND_DIR / "assets"
CSS_DIR = FRONTEND_DIR / "css"
PAGES_DIR = FRONTEND_DIR / "pages"
COMPONENTS_DIR = FRONTEND_DIR / "components"
JAVASCRIPT_DIR = FRONTEND_DIR / "scripts"
NODEMODULES_DIR = FRONTEND_DIR / "node_modules"

# Mount static files to serve frontend assets
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
app.mount("/css", StaticFiles(directory=CSS_DIR), name="css")
app.mount("/pages", StaticFiles(directory=PAGES_DIR), name="pages")
app.mount("/components", StaticFiles(directory=COMPONENTS_DIR), name="components")
app.mount("/scripts", StaticFiles(directory=JAVASCRIPT_DIR), name="scripts")
app.mount("/node_modules", StaticFiles(directory=NODEMODULES_DIR), name="node_modules")

# Define routes for the frontend pages
@app.get("/", response_class=HTMLResponse)
async def home():
    path = PAGES_DIR / "home.html"
    if path.exists():
        return HTMLResponse(content=path.read_text(), status_code=200)
    return HTMLResponse("Home Page Not Found", status_code=404)

@app.get("/booking", response_class=HTMLResponse)
async def booking():
    path = PAGES_DIR / "booking.html"
    if path.exists():
        return HTMLResponse(content=path.read_text(), status_code=200)
    return HTMLResponse("Booking Page Not Found", status_code=404)

@app.get("/add-route", response_class=HTMLResponse)
async def add_route():
    path = PAGES_DIR / "add-routes.html"
    if path.exists():
        return HTMLResponse(content=path.read_text(), status_code=200)
    return HTMLResponse("Add Route Page Not Found", status_code=404)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    path = PAGES_DIR / "dashboard.html"
    if path.exists():
        return HTMLResponse(content=path.read_text(), status_code=200)
    return HTMLResponse("Dashboard Page Not Found", status_code=404)

@app.get("/signin", response_class=HTMLResponse)
async def signin():
    path = PAGES_DIR / "signin.html"
    if path.exists():
        return HTMLResponse(content=path.read_text(), status_code=200)
    return HTMLResponse("Sign In Page Not Found", status_code=404)

@app.get("/signup", response_class=HTMLResponse)
async def signup():
    path = PAGES_DIR / "signup.html"
    if path.exists():
        return HTMLResponse(content=path.read_text(), status_code=200)
    return HTMLResponse("Sign Up Page Not Found", status_code=404)

@app.get("/user-information", response_class=HTMLResponse)
async def user_information():
    path = PAGES_DIR / "user-information.html"
    if path.exists():
        return HTMLResponse(content=path.read_text(), status_code=200)
    return HTMLResponse("User Information Page Not Found", status_code=404)










# Database Setup
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST method to add user


from fastapi import HTTPException


###############################  SIGN UP ################################

@app.post("/add_user/")
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    # Create a new user and hash the password
    new_user = User(username=user.username, email=user.email)
    new_user.hash_password(user.password)  # Hash the password

    db.add(new_user)
    db.commit()

    return {"message": "User added successfully"}


###############################  Book a trip ################################

@app.get("/cities", response_model=List[CityName])
def get_cities(term: Optional[str] = None, db: Session = Depends(get_db)):
    if term:
        # Use LIKE for case-insensitive search in MySQL
        query = text("SELECT id, name_en FROM cities WHERE name_en LIKE :term ORDER BY name_en")
        result = db.execute(query, {"term": f"{term}%"})
    else:
        # Default: get all cities sorted
        result = db.execute(text("SELECT id, name_en FROM cities ORDER BY name_en"))
    
    cities = [{"id": row[0], "text": row[1]} for row in result.fetchall()]
    return cities





###############################  Sign IN ################################


from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import status

# JWT Configuration
SECRET_KEY = "your-secret-key-keep-it-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from fastapi import FastAPI, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    if not user.verify_password(password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    # Create JWT token
    access_token = create_access_token(
        data={"sub": user.email}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "email": user.email,
            "username": user.username
        }
    }



from fastapi import Depends, HTTPException

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

@app.get("/dashboard")
async def protected_route(current_user: User = Depends(get_current_user)):
    return HTMLResponse(content=(PAGES_DIR / "dashboard.html").read_text(), status_code=200)