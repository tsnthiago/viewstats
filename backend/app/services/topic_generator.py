from typing import List, Dict, Optional

class TopicGenerator:
    """
    Serviço para geração de tópicos hierárquicos usando LLM (OpenAI, Gemini, etc).
    """
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None):
        self.provider = provider
        self.api_key = api_key

    def generate_topics(self, title: str, description: str, transcript: str) -> List[str]:
        """
        Gera até 3 caminhos hierárquicos de tópicos a partir dos dados do vídeo.
        Implementação deve ser feita para OpenAI ou Google Gemini.
        """
        if self.provider == "openai":
            return self._generate_with_openai(title, description, transcript)
        elif self.provider == "gemini":
            return self._generate_with_gemini(title, description, transcript)
        else:
            raise ValueError(f"Provider não suportado: {self.provider}")

    def _generate_with_openai(self, title: str, description: str, transcript: str) -> List[str]:
        """
        Implementação da chamada à API OpenAI para geração de tópicos.
        """
        # TODO: Implementar integração com OpenAI
        raise NotImplementedError("Integração com OpenAI não implementada.")

    def _generate_with_gemini(self, title: str, description: str, transcript: str) -> List[str]:
        """
        Implementação da chamada à API Google Gemini para geração de tópicos.
        """
        # TODO: Implementar integração com Google Gemini
        raise NotImplementedError("Integração com Google Gemini não implementada.") 