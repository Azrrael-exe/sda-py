from pydantic import BaseSettings


class Settings(BaseSettings):
    PORT: str
    BAUDRATE: int = 115200

    KP: float
    KD: float

    class Config:
        """Other configurations for env file."""

        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
