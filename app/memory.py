import chromadb
from chromadb.config import Settings

# Inicializa ChromaDB (Base de datos vectorial local, gratis, sin keys)
client = chromadb.Client(Settings(anonymized_telemetry=False, persist_directory="./chroma_db"))
collection = client.get_or_create_collection(name="empresa_aprendizaje")

def guardar_aprendizaje(task_name: str, feedback: str, output: str):
    """Guarda los resultados y feedback para que la IA aprenda de sus errores."""
    doc_id = f"task_{len(collection.get()['ids'])}"
    collection.add(
        documents=[f"Tarea: {task_name}\nFeedback: {feedback}\nResultado: {output}"],
        metadatas=[{"task": task_name, "type": "feedback"}],
        ids=[doc_id]
    )

def obtener_lessons_learned(task_name: str) -> str:
    """Recupera lecciones pasadas para que no cometan los mismos errores."""
    results = collection.query(
        query_texts=[f"Lecciones aprendidas y feedback para {task_name}"],
        n_results=2
    )
    if results['documents'] and results['documents'][0]:
        return "\n".join(results['documents'][0])
    return "No hay lecciones previas registradas."