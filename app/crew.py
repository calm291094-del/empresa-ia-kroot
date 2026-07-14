from crewai import Crew, Process
from app.tasks import crear_tareas
from app.memory import guardar_aprendizaje

def ejecutar_empresa(topico: str):
    tareas = crear_tareas(topico)
    
    empresa = Crew(
        agents=[tareas[0].agent, tareas[1].agent, tareas[2].agent],
        tasks=tareas,
        process=Process.sequential,
        verbose=True,
        memory=True # Activa la memoria interna de CrewAI
    )
    
    resultado = empresa.kickoff()
    
    # Guardamos el resultado en la base de datos para que "aprendan" la próxima vez
    guardar_aprendizaje(
        task_name=topico, 
        feedback="Ejecución completada", 
        output=str(resultado)[:500] # Guardamos un resumen
    )
    
    return str(resultado)