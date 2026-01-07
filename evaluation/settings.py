"""
Application settings management using Pydantic.

This module defines the application configuration settings loaded from multiple sources
with the following priority (highest to lowest):
1. YAML configuration file (app.yml)
2. File secrets
3. Environment variables
4. .env file
5. Default values

The Settings class uses Pydantic BaseSettings to provide type validation and automatic
loading from environment variables and YAML files. Additional fields can be dynamically
added via the YAML configuration due to the 'extra="allow"' setting.

Usage:
    from evaluation.settings import APP_SETTINGS
    print(APP_SETTINGS.app_name)
"""
from pydantic_settings import BaseSettings, SettingsConfigDict, YamlConfigSettingsSource
from typing import Final

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and a YAML configuration file.
    """
    app_name: str = "myapp"

    model_config = SettingsConfigDict(
        env_file=".env",
        yaml_file="app.yml",
        env_file_encoding="utf-8",
        extra="allow"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings):
        return (
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
            env_settings,
            dotenv_settings,
            init_settings,
        )

APP_SETTINGS: Final[Settings] = Settings()