from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
# from tensorflow.keras.models import load_model
# from tensorflow.keras.applications.efficientnet import preprocess_input
# from


# Initialize FastAPI app
app = FastAPI()

# Resolve the frontend directory
BASE_DIR = Path(__file__).resolve().parent  
FRONTEND_DIR = BASE_DIR.parent / "Frontend"  
BACKEND_DIR = BASE_DIR.parent/"Backend"

# Mount static file directories
app.mount("/assets", StaticFiles(directory=FRONTEND_DIR / "assets"), name="assets")
app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
# app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")
app.mount("/pages", StaticFiles(directory=FRONTEND_DIR / "pages"), name="pages")
# app.mount("/static", StaticFiles(directory=FRONTEND_DIR / "static"), name="static")
app.mount("/components", StaticFiles(directory=FRONTEND_DIR / "components"), name="components")

@app.get("/home",response_class=HTMLResponse)
async def mainPage():
    path=FRONTEND_DIR/"pages"/"home.html"

    if path.exists():
        return HTMLResponse(content=path.read_text(),status_code=200)
    return HTMLResponse("Honme Page Not Found",status_code=404)



@app.get("/booking",response_class=HTMLResponse)
async def mainPage():
    path=FRONTEND_DIR/"pages"/"booking.html"

    if path.exists():
        return HTMLResponse(content=path.read_text(),status_code=200)
    return HTMLResponse("Page Not Found",status_code=404)

@app.get("/add-route",response_class=HTMLResponse)
async def mainPage():
    path=FRONTEND_DIR/"pages"/"add-routes.html"

    if path.exists():
        return HTMLResponse(content=path.read_text(),status_code=200)
    return HTMLResponse("Page Not Found",status_code=404)

@app.get("/dashboard",response_class=HTMLResponse)
async def mainPage():
    path=FRONTEND_DIR/"pages"/"dashboard.html"

    if path.exists():
        return HTMLResponse(content=path.read_text(),status_code=200)
    return HTMLResponse("Page Not Found",status_code=404)

@app.get("/signin",response_class=HTMLResponse)
async def mainPage():
    path=FRONTEND_DIR/"pages"/"signin.html"

    if path.exists():
        return HTMLResponse(content=path.read_text(),status_code=200)
    return HTMLResponse("Page Not Found",status_code=404)

@app.get("/signup",response_class=HTMLResponse)
async def mainPage():
    path=FRONTEND_DIR/"pages"/"signup.html"

    if path.exists():
        return HTMLResponse(content=path.read_text(),status_code=200)
    return HTMLResponse("Page Not Found",status_code=404)

@app.get("/user-information",response_class=HTMLResponse)
async def mainPage():
    path=FRONTEND_DIR/"pages"/"user-information.html"

    if path.exists():
        return HTMLResponse(content=path.read_text(),status_code=200)
    return HTMLResponse("Page Not Found",status_code=404)




# @app.get("/",response_class=HTMLResponse)
# async def mainPage():
#     path=FRONTEND_DIR/"pages"/"home.html"

#     if path.exists():
#         return HTMLResponse(content=path.read_text(),status_code=200)
#     return HTMLResponse("Honme Page Not Found",status_code=404)