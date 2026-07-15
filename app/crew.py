from crewai import Crew, Process
from app.tasks import crear_tareas
from app.memory import guardar_aprendizaje
import logging

logger = logging.getLogger(__name__)

def ejecutar_empresa(topico: str):
    logger.info("🏗️ Construyendo las tareas y agentes...")
    tareas = crear_tareas(topico)
    
    # Desactivamos la memoria interna de CrewAI para evitar que pida la API Key de OpenAI.
    # Nuestra memoria personalizada en app/memory.py se encarga del aprendizaje.
    empresa = Crew(
        agents=[tareas[0].agent, tareas[1].agent, tareas[2].agent],
        tasks=tareas,
        process=Process.sequential,
        verbose=True,
        memory=False  # <-- ESTE ES EL CAMBIO CLAVE
    )
    
    logger.info("🚀 Ejecutando la empresa (esto puede tardar 1-2 minutos)...")
    resultado = empresa.kickoff()
    
    # Guardamos el resultado en nuestra base de datos JSON personalizada para que "aprendan"
    guardar_aprendizaje(
        task_name=topico, 
        feedback="Ejecución completada con éxito", 
        output=str(resultado)[:500] # Guardamos un resumen para no inflar el archivo
    )
    
    logger.info("✅ Proceso finalizado y aprendizaje guardado.")
    return str(resultado)