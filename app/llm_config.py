import logging
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)

# Pollinations.ai es una API 100% gratuita, de código abierto y SIN KEYS.
# Ofrece un endpoint compatible con OpenAI que funciona excelente en servidores.
llm_instance = ChatOpenAI(
    model="openai", # Pollinations usa este alias para su modelo principal
    openai_api_key="no-key-needed", # Pollinations ignora esto, es solo para que la librería no falle
    openai_api_base="https://text.pollinations.ai/openai",
    temperature=0.7,
    request_timeout=60
)

logger.info("✅ Cerebro de IA inicializado con Pollinations.ai (100% Gratis, Sin Keys)")