from app.agents import researcher_chain, writer_chain, critic_chain
from app.memory import guardar_aprendizaje, obtener_lessons_learned
import logging

logger = logging.getLogger(__name__)

def ejecutar_empresa(topico: str):
    logger.info("🏗️ Iniciando proceso de agentes personalizados...")
    
    # 1. Obtener lecciones previas para que la IA "aprenda"
    lecciones = obtener_lessons_learned(topico)
    lecciones_txt = f"Evita estos errores pasados: {lecciones}" if lecciones else "No hay errores previos registrados."
    
    # 2. Fase 1: Investigación
    logger.info("🔍 Fase 1: Investigando...")
    investigacion = researcher_chain.invoke({"topico": topico, "lecciones_previas": lecciones_txt})
    investigacion_texto = investigacion.content if hasattr(investigacion, 'content') else str(investigacion)
    
    # 3. Fase 2: Redacción
    logger.info("✍️ Fase 2: Redactando informe...")
    informe = writer_chain.invoke({"investigacion": investigacion_texto})
    informe_texto = informe.content if hasattr(informe, 'content') else str(informe)
    
    # 4. Fase 3: Crítica y Calidad
    logger.info("🔎 Fase 3: Revisión de calidad...")
    critica = critic_chain.invoke({"informe": informe_texto})
    critica_texto = critica.content if hasattr(critica, 'content') else str(critica)
    
    # 5. Ensamblar resultado final
    resultado_final = f"# 📊 INFORME EJECUTIVO: {topico.upper()}\n\n{informe_texto}\n\n---\n### 📝 Veredicto de Calidad (QA):\n{critica_texto}"
    
    # 6. Guardar aprendizaje para el futuro
    guardar_aprendizaje(
        task_name=topico,
        feedback=critica_texto[:200], # Guardamos el veredicto del QA
        output=informe_texto[:500]
    )
    
    logger.info("✅ Proceso finalizado con éxito.")
    return resultado_final