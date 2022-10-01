from pydantic import BaseSettings


class Settings(BaseSettings):
    PORT: str
    BAUDRATE: int = 115200

    KP: float
    KD: float

    PG_DB: str = "SDA"
    PG_TABLE: str = "READS"
    PG_USER: str = "vcamargo"
    PG_PASSWORD: str = "maxwell"
    PG_PORT: int = 5432
    PG_HOST: str = "0.0.0.0"

    MQTT_HOST: str = "broker.hivemq.com"

    class Config:
        """Other configurations for env file."""

        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
