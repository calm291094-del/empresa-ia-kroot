from fastapi import FastAPI, Request, Form, Depends, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import logging
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="kroot_super_secret_key_4815162342")
templates = Jinja2Templates(directory="app/templates")

USERS = {"kroot": "K4815162342"}
REPORT_HISTORY = [] 

def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="No autorizado")
    return user

def tarea_en_background(topico: str):
    logger.info(f"🚀 INICIANDO AGENTES PARA: '{topico}'")
    try:
        from app.crew import ejecutar_empresa
        resultado = ejecutar_empresa(topico)
        logger.info(f"✅ AGENTES TERMINARON CON ÉXITO PARA: '{topico}'")
        
        for i, report in enumerate(REPORT_HISTORY):
            if report["topico"] == topico and report["estado"] == "Procesando":
                REPORT_HISTORY[i] = {"topico": topico, "resultado": resultado, "estado": "Éxito"}
                break
                
    except Exception as e:
        # Aquí capturamos el error completo con todas las líneas
        error_trace = traceback.format_exc()
        logger.error(f"❌ ERROR CRÍTICO EN AGENTES PARA '{topico}':\n{error_trace}")
        
        for i, report in enumerate(REPORT_HISTORY):
            if report["topico"] == topico and report["estado"] == "Procesando":
                REPORT_HISTORY[i] = {
                    "topico": topico, 
                    "resultado": f"Error: {str(e)}\n\n(Revisa los logs de Render para ver el traceback completo)", 
                    "estado": "Fallo"
                }
                break

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
        logger.info(f"✅ Usuario {username} ha iniciado sesión.")
        return RedirectResponse(url="/dashboard", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Credenciales inválidas"})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: str = Depends(get_current_user)):
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "user": user, 
        "reports": REPORT_HISTORY[::-1]
    })

@app.post("/run_crew")
async def run_crew(
    request: Request, 
    background_tasks: BackgroundTasks,
    topico: str = Form(...), 
    user: str = Depends(get_current_user)
):
    logger.info(f"📥 Petición recibida para ejecutar: '{topico}'")
    
    REPORT_HISTORY.append({
        "topico": topico, 
        "resultado": "⏳ Los agentes están investigando y redactando. Esto puede tardar 1 o 2 minutos. ¡Recarga esta página (F5) en un momento para ver el resultado!", 
        "estado": "Procesando"
    })
    
    background_tasks.add_task(tarea_en_background, topico)
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)