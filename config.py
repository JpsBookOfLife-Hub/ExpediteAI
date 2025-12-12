"""Configuration management for API keys and application settings."""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class Config:
    """Manages application configuration and API keys."""
    
    # Screenshot directory path
    SCREENSHOT_DIR = r"C:\Users\janpa\Pictures\Screenshots"
    
    # API Keys (loaded from environment variables)
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # Default AI provider (can be 'gemini', 'openai', or 'anthropic')
    DEFAULT_PROVIDER: str = os.getenv("DEFAULT_PROVIDER", "openai").lower()
    
    # Model configuration for each provider
    # Gemini models: 'gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro', 'gemini-pro-vision'
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # OpenAI models: 'gpt-4o' (default), 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-4-turbo-preview', 'gpt-4', 'gpt-4-vision-preview'
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    # Anthropic models: 'claude-3-5-sonnet-20241022', 'claude-3-5-haiku-20241022', 'claude-3-opus-20240229', 'claude-3-sonnet-20240229'
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
    
    # Hotkey configuration
    HOTKEY: str = os.getenv("HOTKEY", "ctrl+shift+q")
    
    # UI settings
    MODAL_DISPLAY_DURATION: int = 5  # seconds
    MODAL_ERROR_DURATION: int = 10  # seconds for errors/warnings
    
    @classmethod
    def get_model(cls, provider: str) -> str:
        """Get model name for the specified provider."""
        provider = provider.lower()
        if provider == "gemini":
            return cls.GEMINI_MODEL
        elif provider == "openai":
            return cls.OPENAI_MODEL
        elif provider == "anthropic":
            return cls.ANTHROPIC_MODEL
        return ""
    
    @classmethod
    def get_api_key(cls, provider: str) -> Optional[str]:
        """Get API key for the specified provider."""
        provider = provider.lower()
        if provider == "gemini":
            return cls.GEMINI_API_KEY
        elif provider == "openai":
            return cls.OPENAI_API_KEY
        elif provider == "anthropic":
            return cls.ANTHROPIC_API_KEY
        return None
    
    @classmethod
    def validate_config(cls, provider: Optional[str] = None) -> tuple[bool, str]:
        """
        Validate that required API keys are configured.
        
        Args:
            provider: Provider to validate. If None, validates the default provider.
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        provider = provider or cls.DEFAULT_PROVIDER
        api_key = cls.get_api_key(provider)
        
        if not api_key:
            return False, f"API key for {provider} not found. Please set the environment variable."
        
        return True, ""

