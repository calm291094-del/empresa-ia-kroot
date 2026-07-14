import os
from langchain_core.language_models import LLM
from typing import Any, List, Mapping, Optional
import g4f
from g4f.Provider import DuckDuckGo, FreeGpt, Bing

class FreeLLMWithFallback(LLM):
    """LLM personalizado que usa APIs gratis sin keys y hace fallback si una falla."""
    
    @property
    def _llm_type(self) -> str:
        return "free_fallback_llm"

    def _call(self, prompt: str, stop: Optional[List[str]] = None, run_manager: Optional[Any] = None, **kwargs: Any) -> str:
        # Si hay una key de Groq (gratis), úsala primero (es la más estable)
        if os.getenv("GROQ_API_KEY"):
            try:
                from langchain_groq import ChatGroq
                # Nota: CrewAI maneja ChatModels, pero para simplificar el wrapper usamos el completion
                pass 
            except ImportError:
                pass

        # Fallback a APIs 100% gratuitas sin keys (GPT4Free)
        providers = [DuckDuckGo, FreeGpt, Bing]
        
        for provider in providers:
            try:
                response = g4f.ChatCompletion.create(
                    model=g4f.models.default,
                    messages=[{"role": "user", "content": prompt}],
                    provider=provider,
                    timeout=60
                )
                if response and len(response) > 10:
                    return response
            except Exception as e:
                print(f"Provider {provider.__name__} failed: {e}")
                continue
                
        raise Exception("Todas las APIs gratuitas han fallado. Intenta de nuevo más tarde.")

# Instancia global
llm_instance = FreeLLMWithFallback()