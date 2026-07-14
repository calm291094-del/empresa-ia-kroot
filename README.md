# 🏢 Empresa IA Autónoma (Kroot Corp)

Sistema multi-agente autónomo que actúa como una empresa de consultoría. Los agentes investigan, redactan informes, se critican entre sí y "aprenden" de sus errores pasados utilizando una base de datos vectorial.

## 🚀 Características
- **Arquitectura Multi-Agente:** Investigador, Redactor y Director de Calidad (QA).
- **APIs Gratuitas con Fallback:** Utiliza `g4f` (GPT4Free) para conectar a APIs gratuitas sin necesidad de API Keys. Si una falla, prueba la siguiente automáticamente.
- **Aprendizaje Continuo:** Usa ChromaDB para guardar el feedback y resultados, inyectando lecciones aprendidas en futuras tareas.
- **Seguridad:** Panel de control protegido por autenticación estricta.
- **Despliegue:** Configurado para desplegarse en un clic en Render usando Docker.

## 🔐 Acceso al Panel
- **Usuario:** `kroot`
- **Contraseña:** `K4815162342`

## 🛠️ Stack Tecnológico
- **Backend:** FastAPI (Python)
- **Orquestación:** CrewAI
- **LLM:** g4f (GPT4Free) / Groq (Fallback opcional)
- **Memoria:** ChromaDB
- **Deploy:** Render (Docker)

## ⚠️ Nota sobre las APIs Gratuitas
Este proyecto está diseñado para funcionar sin gastar dinero usando APIs inversas (`g4f`). Sin embargo, estas APIs pueden tener rate-limits o caídas. El sistema de fallback mitiga esto, pero para un entorno de producción crítico, se recomienda añadir una API Key gratuita de [Groq](https://groq.com/) en las variables de entorno.
