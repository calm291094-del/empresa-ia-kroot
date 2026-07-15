import logging
from typing import Any, List, Optional
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
import g4f
from g4f.Provider import Blackbox, DeepInfra, Liaobots, Phind

# Desactivar chequeo de versión para evitar warnings
g4f.debug.version_check = False

logger = logging.getLogger(__name__)

class FallbackChatModel(BaseChatModel):
    model: str = "gpt-4o"
    model_name: str = "gpt-4o"
    temperature: float = 0.7
    
    @property
    def _llm_type(self) -> str:
        return "fallback_free_llm"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        prompt = "\n".join([f"{m.type}: {m.content}" for m in messages])
        response_text = self._get_response_with_fallback(prompt)
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=response_text))])

    def _get_response_with_fallback(self, prompt: str) -> str:
        # Lista de proveedores. Si uno devuelve basura, pasa al siguiente.
        providers = [
            ("Blackbox AI", Blackbox),
            ("Liaobots", Liaobots),
            ("Phind", Phind),
            ("DeepInfra", DeepInfra)
        ]

        for name, provider in providers:
            try:
                logger.info(f"🔄 Intentando proveedor: {name}")
                response = g4f.ChatCompletion.create(
                    model="gpt-4o", 
                    messages=[{"role": "user", "content": prompt}],
                    provider=provider,
                    timeout=60
                )
                
                # VALIDACIÓN ESTRICTA:
                if response and isinstance(response, str):
                    response = response.strip()
                    # Rechazamos si es muy corto o si contiene señales claras de error crudo de la API
                    if len(response) > 30 and "Authentication Error" not in response and "data: {" not in response:
                        logger.info(f"✅ Éxito real con: {name}")
                        return response
                    else:
                        logger.warning(f"⚠️ {name} devolvió un error interno o formato no válido (falso positivo).")
                else:
                    logger.warning(f"⚠️ {name} devolvió una respuesta vacía.")
            except Exception as e:
                error_msg = str(e)[:100]
                logger.warning(f"⚠️ Fallo en {name}: {error_msg}...")
                continue

        raise Exception("Todos los proveedores gratuitos fallaron o devolvieron errores de autenticación. Intenta de nuevo en unos minutos.")

llm_instance = FallbackChatModel()