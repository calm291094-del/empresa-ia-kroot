   import os
   from langchain_core.language_models import LLM
   from typing import Any, List, Optional
   import g4f
   from g4f.Provider import DuckDuckGo, Bing
   import logging

   logger = logging.getLogger(__name__)

   class FreeLLMWithFallback(LLM):
       @property
       def _llm_type(self) -> str:
           return "free_fallback_llm"

       def _call(self, prompt: str, stop: Optional[List[str]] = None, run_manager: Optional[Any] = None, **kwargs: Any) -> str:
           providers_to_try = [DuckDuckGo, Bing]
           
           for provider in providers_to_try:
               try:
                   logger.info(f"🔄 Intentando con: {provider.__name__}")
                   response = g4f.ChatCompletion.create(
                       model="gpt-3.5-turbo",
                       messages=[{"role": "user", "content": prompt}],
                       provider=provider,
                       timeout=60
                   )
                   if response and isinstance(response, str) and len(response) > 20:
                       logger.info(f"✅ Éxito con {provider.__name__}")
                       return response
               except Exception as e:
                   logger.warning(f"⚠️ {provider.__name__} falló: {str(e)}")
                   continue
                   
           raise Exception("Todos los proveedores gratuitos fallaron. Intenta de nuevo.")

   llm_instance = FreeLLMWithFallback()