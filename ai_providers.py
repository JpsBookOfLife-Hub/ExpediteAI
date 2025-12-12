"""AI provider implementations for Gemini, OpenAI, and Anthropic Claude."""
import base64
import io
from abc import ABC, abstractmethod
from typing import Optional, Tuple
from PIL import Image

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    def process_image(self, image_path: str, prompt: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Process an image with the AI model and return the response.
        
        Args:
            image_path: Path to the image file
            prompt: Text prompt to send with the image
            
        Returns:
            Tuple of (response_text, error_message)
            - response_text: AI response text, or None if processing fails
            - error_message: Error message if billing/credit issue detected, None otherwise
        """
        pass
    
    @staticmethod
    def _image_to_base64(image: Image.Image) -> str:
        """Convert PIL Image to base64 string."""
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")


class GeminiProvider(AIProvider):
    """Google Gemini AI provider."""
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        if genai is None:
            raise ImportError("google-generativeai package is required. Install with: pip install google-generativeai")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
    
    def process_image(self, image_path: str, prompt: str) -> Tuple[Optional[str], Optional[str]]:
        """Process image using Gemini API."""
        try:
            image = Image.open(image_path)
            response = self.model.generate_content([prompt, image])
            return response.text.strip(), None
        except Exception as e:
            error_str = str(e).lower()
            print(f"Gemini API error: {e}")
            
            # Check for billing/credit related errors
            billing_keywords = ['quota', 'billing', 'payment', 'credit', 'insufficient', 
                              'exceeded', 'limit', 'subscription', 'account']
            if any(keyword in error_str for keyword in billing_keywords):
                return None, f"⚠️ Low credits/billing issue detected.\nPlease check your Gemini API billing."
            
            return None, None


class OpenAIProvider(AIProvider):
    """OpenAI GPT-4 Vision provider."""
    
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        if OpenAI is None:
            raise ImportError("openai package is required. Install with: pip install openai")
        self.client = OpenAI(api_key=api_key)
        self.model_name = model
    
    def process_image(self, image_path: str, prompt: str) -> Tuple[Optional[str], Optional[str]]:
        """Process image using OpenAI GPT-4 Vision API."""
        try:
            image = Image.open(image_path)
            base64_image = self._image_to_base64(image)
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip(), None
        except Exception as e:
            error_str = str(e).lower()
            error_type = type(e).__name__.lower()
            print(f"OpenAI API error: {e}")
            
            # Check for specific error codes/attributes
            error_code = None
            if hasattr(e, 'status_code'):
                error_code = e.status_code
            elif hasattr(e, 'code'):
                error_code = e.code
            
            # Check for billing/credit related errors
            billing_keywords = ['insufficient_quota', 'billing', 'payment', 'credit', 
                              'insufficient', 'exceeded', 'limit', 'subscription', 
                              'account', 'rate_limit', 'quota', '402', '429']
            
            is_billing_error = (
                error_code in [402, 429] or
                any(keyword in error_str for keyword in billing_keywords) or
                'quota' in error_type or
                'billing' in error_type
            )
            
            if is_billing_error:
                return None, f"⚠️ Low credits/billing issue detected.\nPlease check your OpenAI API billing."
            
            return None, None


class AnthropicProvider(AIProvider):
    """Anthropic Claude 3 provider."""
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        if Anthropic is None:
            raise ImportError("anthropic package is required. Install with: pip install anthropic")
        self.client = Anthropic(api_key=api_key)
        self.model_name = model
    
    def process_image(self, image_path: str, prompt: str) -> Tuple[Optional[str], Optional[str]]:
        """Process image using Anthropic Claude API."""
        try:
            image = Image.open(image_path)
            base64_image = self._image_to_base64(image)
            
            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=300,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": base64_image
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )
            
            return message.content[0].text.strip(), None
        except Exception as e:
            error_str = str(e).lower()
            print(f"Anthropic API error: {e}")
            
            # Check for billing/credit related errors
            billing_keywords = ['quota', 'billing', 'payment', 'credit', 'insufficient', 
                              'exceeded', 'limit', 'subscription', 'account', 'rate_limit']
            if any(keyword in error_str for keyword in billing_keywords):
                return None, f"⚠️ Low credits/billing issue detected.\nPlease check your Anthropic API billing."
            
            return None, None


def create_provider(provider_name: str, api_key: str, model: str = None) -> AIProvider:
    """
    Factory function to create the appropriate AI provider.
    
    Args:
        provider_name: Name of the provider ('gemini', 'openai', or 'anthropic')
        api_key: API key for the provider
        model: Model name to use. If None, uses provider's default.
        
    Returns:
        AIProvider instance
        
    Raises:
        ValueError: If provider name is invalid
    """
    provider_name = provider_name.lower()
    
    if provider_name == "gemini":
        return GeminiProvider(api_key, model or "gemini-1.5-flash")
    elif provider_name == "openai":
        return OpenAIProvider(api_key, model or "gpt-4o")
    elif provider_name == "anthropic":
        return AnthropicProvider(api_key, model or "claude-3-5-sonnet-20241022")
    else:
        raise ValueError(f"Unknown provider: {provider_name}")

