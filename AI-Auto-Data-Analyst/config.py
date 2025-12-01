from dotenv import load_dotenv
load_dotenv()

"""
Project configuration module.

Loads environment variables and exposes strongly-typed settings
for the rest of the application.
"""

from dataclasses import dataclass
import os
from typing import Optional


@dataclass
class Settings:
    """Application-level configuration."""
    gemini_api_key: str
    gemini_model_name: str = "models/gemini-2.5-flash"

    @classmethod
    def from_env(cls) -> "Settings":
        """
        Load settings from environment variables.

        Expected:
            GEMINI_API_KEY: str
            GEMINI_MODEL_NAME: Optional[str]
        """
        api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set. "
                "Set it in your environment or .env file."
            )

        model_name: str = os.getenv("GEMINI_MODEL_NAME", "models/gemini-2.5-flash")
        return cls(gemini_api_key=api_key, gemini_model_name=model_name)


# Convenience singleton
settings = Settings.from_env()
