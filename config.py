from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 应用配置:从.env中读取配置

    model_config = SettingsConfigDict(
        env_file = ".env",
        extra="ignore"
    )

    github_api_base: str = "https://api.github.com/"
    timeout: float = 10.0
    repo: str = "pallets/flask"

settings = Settings()
