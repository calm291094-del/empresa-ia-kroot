import logging
from typing import Any, List, Optional
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
import g4f
from g4f.Provider import Blackbox, DeepInfra, Liaobots, Phind

# Forzar a g4f a usar curl_cffi para evadir bloqueos de Render
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
        # Proveedores que toleran mejor las IPs de servidores (Render)
        providers = [
            ("Blackbox AI", Blackbox),
            ("DeepInfra", DeepInfra),
            ("Liaobots", Liaobots),
            ("Phind", Phind)
        ]

        for name, provider in providers:
            try:
                logger.info(f"🔄 Intentando proveedor: {name}")
                response = g4f.ChatCompletion.create(
                    model="gpt-4o", # Blackbox y DeepInfra soportan este alias
                    messages=[{"role": "user", "content": prompt}],
                    provider=provider,
                    timeout=60
                )
                
                if response and isinstance(response, str) and len(response.strip()) > 10:
                    logger.info(f"✅ Éxito con: {name}")
                    return response
                else:
                    logger.warning(f"⚠️ {name} devolvió respuesta vacía.")
            except Exception as e:
                error_msg = str(e)[:100]
                logger.warning(f"⚠️ Fallo en {name}: {error_msg}...")
                continue

        raise Exception("Todos los proveedores gratuitos fallaron. La IP del servidor puede estar temporalmente bloqueada. Intenta de nuevo en 5 minutos.")

llm_instance = FallbackChatModel()