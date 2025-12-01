from typing import List, Dict, Optional
import requests
from config.llm.settings import llm_settings
import logging
import sys
import re
from pathlib import Path

logger = logging.getLogger(__name__)


class LLMService:
    """LLM service using HuggingFace API via direct HTTP requests"""

    def __init__(self):
        # Basic settings
        self.hf_token = llm_settings.hf_token
        self.model_id = llm_settings.llm_model_id
        self.max_new_tokens = llm_settings.max_new_tokens
        self.temperature = llm_settings.temperature

        # HF Router endpoint
        self.base_url = "https://router.huggingface.co/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }

        # Load system prompt from system_instructions.py
        self.system_prompt = self._load_system_instructions()
        self.functions = []  # Can be configured later if needed

        logger.info(f"LLM Service initialized with model: {self.model_id}")
        logger.info(f"System prompt loaded from system_instructions.py")

    def _load_system_instructions(self) -> str:
        """Load system instructions from system_instructions.py"""
        try:
            # Get the parent directory (project root)
            project_root = Path(__file__).parent.parent
            
            # Add project root to sys.path if not already there
            if str(project_root) not in sys.path:
                sys.path.insert(0, str(project_root))
            
            # Import the system_instructions module
            import system_instructions
            
            return system_instructions.SYSTEM_INSTRUCTIONS
            
        except Exception as e:
            logger.error(f"Error loading system instructions: {str(e)}", exc_info=True)
            return ""

    def _inject_system_prompt(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Ensure the system prompt is always the FIRST message.
        Avoid duplicates and override any external system message.
        """
        if not self.system_prompt:
            return messages

        # Remove any existing system messages
        filtered = [m for m in messages if m.get("role") != "system"]

        # Prepend our system prompt
        return [{"role": "system", "content": self.system_prompt}] + filtered

    def _clean_response(self, response: str) -> str:
        """
        Remove <think> and </think> tags and their content from the response.
        DeepSeek-R1 often returns thinking process in these tags.
        """
        # Remove everything between <think> and </think> (including the tags)
        cleaned = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
        
        # Also handle unclosed tags just in case
        cleaned = re.sub(r'<think>.*', '', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r'.*</think>', '', cleaned, flags=re.DOTALL)
        
        # Strip leading/trailing whitespace
        return cleaned.strip()

    def generate(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        use_system_prompt: bool = True,
        json_mode: bool = False
    ) -> str:
        """
        Generate text based on chat messages
        """

        max_tokens = max_tokens or self.max_new_tokens

        # Inject system prompt if requested
        if use_system_prompt:
            messages = self._inject_system_prompt(messages)

        payload = {
            "model": self.model_id,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": self.temperature,
        }
        
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        # Add functions if any exist
        if self.functions:
            payload["tools"] = [
                {"type": "function", "function": func}
                for func in self.functions
            ]

        try:
            logger.info(f"Sending request to HF Router with {len(messages)} messages")

            response = requests.post(
                self.base_url,
                json=payload,
                headers=self.headers,
                timeout=240
            )
            response.raise_for_status()

            data = response.json()
            raw_response = data["choices"][0]["message"]["content"]
            
            # Clean the response to remove <think> tags
            cleaned_response = self._clean_response(raw_response)
            
            return cleaned_response

        except Exception as e:
            logger.error(f"LLM generation error: {e}", exc_info=True)
            return f"Error: Unable to generate response. {str(e)}"

    def get_system_prompt(self) -> str:
        return self.system_prompt

    def get_functions(self) -> List[Dict]:
        return self.functions


llm_service = LLMService()
