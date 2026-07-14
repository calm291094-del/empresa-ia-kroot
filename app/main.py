from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import threading
import time

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="kroot_super_secret_key_4815162342")
templates = Jinja2Templates(directory="app/templates")

# Credenciales Hardcodeadas (Según petición)
USERS = {"kroot": "K4815162342"}
REPORT_HISTORY = [] # Almacén en memoria de los informes generados

def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="No autorizado")
    return user

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if USERS.get(username) == password:
        request.session["user"] = username
        return RedirectResponse(url="/dashboard", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Credenciales inválidas"})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: str = Depends(get_current_user)):
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "user": user, 
        "reports": REPORT_HISTORY[::-1] # Últimos primero
    })

@app.post("/run_crew")
async def run_crew(request: Request, topico: str = Form(...), user: str = Depends(get_current_user)):
    from app.crew import ejecutar_empresa
    
    # Ejecutar en segundo plano para no bloquear la UI (los agentes tardan)
    def background_task():
        try:
            resultado = ejecutar_empresa(topico)
            REPORT_HISTORY.append({"topico": topico, "resultado": resultado, "estado": "Éxito"})
        except Exception as e:
            REPORT_HISTORY.append({"topico": topico, "resultado": f"Error: {str(e)}", "estado": "Fallo"})

    threading.Thread(target=background_task).start()
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)