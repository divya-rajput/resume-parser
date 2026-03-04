import json, os
from openai import AzureOpenAI
from typing import Callable, List
from abc import ABC, abstractmethod


LLMCallable = Callable[[str], str]

_SYSTEM_PROMPT = (
    "You are a resume parsing assistant. "
    "You extract professional and technical skills only."
)

_USER_PROMPT_TEMPLATE = (
    "Extract all relevant skills from the resume below.\n"
    "Return ONLY a valid JSON array of strings.\n\n"
    "Resume:\n{resume_text}"
)


class BaseSkillsLLMExtractor(ABC):
    @abstractmethod
    def extract_skills(self, result_raw_string: str) -> List[str]:
        pass
    
    def _parse_response(self, response: str) -> List[str]:
        response = response.strip()

        # Try JSON first
        try:
            data = json.loads(response)
            if isinstance(data, list):
                return [str(item).strip() for item in data if str(item).strip()]
        except json.JSONDecodeError:
            pass

        # Fallback: comma-separated
        if "," in response:
            return [item.strip() for item in response.split(",") if item.strip()]

        return [response] if response else []
    

class OllamaSkillsExtractor(BaseSkillsLLMExtractor):
    def __init__(self, model: str = "llama3"):
        self._model = model
        self._system_prompt = _SYSTEM_PROMPT
        self._user_prompt_template = _USER_PROMPT_TEMPLATE

    def extract_skills(self, text: str) -> List[str]:
        import ollama 
        user_prompt = self._user_prompt_template.format(resume_text=text)

        response = ollama.chat(
            model=self._model,
            messages=[
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        raw_output = response["message"]["content"]
        return self._parse_response(raw_output)
    


class AzureOpenAISkillsExtractor(BaseSkillsLLMExtractor):
    def __init__(
        self,
        deployment_name: str | None = None,
        api_key: str | None = None,
        endpoint: str | None = None,
    ):
        self._deployment_name = deployment_name or os.getenv("AZURE_OPENAI_DEPLOYMENT")

        self._client = AzureOpenAI(
            api_key=api_key or os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=endpoint or os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version="2024-02-01",
        )

        self._system_prompt = _SYSTEM_PROMPT
        self._user_prompt_template = _USER_PROMPT_TEMPLATE

    def extract_skills(self, text: str) -> List[str]:
        user_prompt = self._user_prompt_template.format(resume_text=text)

        response = self._client.chat.completions.create(
            model=self._deployment_name,
            messages=[
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,
        )

        raw_output = response.choices[0].message.content
        return self._parse_response(raw_output)



