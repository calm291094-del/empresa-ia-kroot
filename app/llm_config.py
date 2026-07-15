import logging
from typing import Any, List, Optional
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

logger = logging.getLogger(__name__)

class FallbackChatModel(BaseChatModel):
    # TRUCO: CrewAI/LiteLLM busca estos atributos para validar el modelo.
    # Se los damos para que no falle al parsear, aunque nuestra lógica 
    # en _generate ignorará esto y usará las APIs gratis.
    model: str = "gpt-3.5-turbo"
    model_name: str = "gpt-3.5-turbo"
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
        # Convertimos los mensajes de LangChain a un prompt de texto simple
        prompt = "\n".join([f"{m.type}: {m.content}" for m in messages])
        
        # Aquí es donde ocurre la magia: usamos nuestro fallback, NO litellm
        response_text = self._get_response_with_fallback(prompt)
        
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=response_text))])

    def _get_response_with_fallback(self, prompt: str) -> str:
        providers = [
            ("DuckDuckGo AI", self._try_duckduckgo),
            ("Hugging Face (Zephyr)", self._try_huggingface),
            ("G4F (DuckDuckGo)", self._try_g4f_safe)
        ]

        for name, func in providers:
            try:
                logger.info(f"🔄 Intentando proveedor: {name}")
                result = func(prompt)
                if result and len(str(result).strip()) > 10:
                    logger.info(f"✅ Éxito con: {name}")
                    return str(result)
                else:
                    logger.warning(f"⚠️ {name} devolvió respuesta vacía o muy corta.")
            except Exception as e:
                logger.warning(f"⚠️ Fallo en {name}: {str(e)[:100]}...")
                continue

        raise Exception("Todos los proveedores gratuitos fallaron. Intenta de nuevo.")

    def _try_duckduckgo(self, prompt: str) -> str:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            return ddgs.chat(prompt)

    def _try_huggingface(self, prompt: str) -> str:
        from huggingface_hub import InferenceClient
        # Modelo gratuito que no requiere token para uso básico
        client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta")
        return client.text_generation(prompt, max_new_tokens=500, temperature=0.7, do_sample=True)

    def _try_g4f_safe(self, prompt: str) -> str:
        import g4f
        from g4f.Provider import DuckDuckGo
        return g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            provider=DuckDuckGo,
            timeout=45
        )

# Instancia global que usará CrewAI
llm_instance = FallbackChatModel()