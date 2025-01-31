from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from model import User

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

# Mount static files to serve frontend assets
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
app.mount("/css", StaticFiles(directory=CSS_DIR), name="css")
app.mount("/pages", StaticFiles(directory=PAGES_DIR), name="pages")
app.mount("/components", StaticFiles(directory=COMPONENTS_DIR), name="components")

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
@app.post("/add_user/")
def add_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    user = User(username=username, email=email, password=password)
    db.add(user)
    db.commit()
    return {"message": "User added successfully"}
