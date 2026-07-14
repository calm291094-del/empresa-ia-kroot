import json
import os

MEMORY_FILE = "empresa_memoria.json"

def _cargar_memoria():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def _guardar_memoria(data):
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def guardar_aprendizaje(task_name: str, feedback: str, output: str):
    """Guarda los resultados en un JSON ligero para no saturar la RAM."""
    data = _cargar_memoria()
    if task_name not in data:
        data[task_name] = []
    
    # Guardamos un resumen corto para no inflar el archivo
    data[task_name].append({
        "feedback": feedback, 
        "output_resumen": output[:300] 
    })
    
    # Limitamos a 5 lecciones por tema para mantener el JSON pequeño
    data[task_name] = data[task_name][-5:] 
    _guardar_memoria(data)

def obtener_lessons_learned(task_name: str) -> str:
    """Recupera lecciones pasadas desde el JSON."""
    data = _cargar_memoria()
    lessons = data.get(task_name, [])
    if lessons:
        # Formateamos las últimas lecciones
        return "\n".join([f"- {l['feedback']}: {l['output_resumen']}" for l in lessons[-2:]])
    return ""