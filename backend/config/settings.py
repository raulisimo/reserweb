import os

import pymysql
from dotenv import load_dotenv
from google.cloud.sql.connector import Connector, IPTypes
from sqlalchemy import create_engine, Engine


class BaseSettings:
    APP_TITLE: str
    DEBUG: bool

    def __init__(self):
        """Initialize base settings"""
        self.APP_TITLE = self.get_config_value("APP_TITLE")
        self.DEBUG = self.get_debug_mode()

    def get_config_value(self, key: str) -> str:
        """Abstract method to fetch configuration values"""
        raise NotImplementedError("Subclasses must implement `get_config_value`")

    def get_debug_mode(self) -> bool:
        """Default debug mode is False."""
        return False

    def get_db_connection(self):
        """Abstract method to get database connection"""
        raise NotImplementedError("Subclasses must implement `get_db_connection`")


class DevSettings(BaseSettings):
    """
    Development settings loaded from .env
    """

    DATABASE_URL: str

    def __init__(self):
        """Initialize development settings"""
        load_dotenv()  # Load .env for development
        super().__init__()

    def get_config_value(self, key: str) -> str:
        """Get the value from environment variables."""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Missing required configuration: {key}")
        return value

    def get_debug_mode(self) -> bool:
        """Enable debug mode in development"""
        return os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")

    def get_db_connection(self) -> Engine:

        environment = self.get_config_value("ENVIRONMENT")

        if environment == "PRO":
            connection_name = os.getenv("CLOUD_SQL_CONNECTION_NAME")
            db_user = os.getenv("DB_USER", "root")
            db_name = os.getenv("DB_NAME", "brite-movies")
            db_password = self.get_config_value("DB_PASSWORD")

            ip_type = IPTypes.PRIVATE if os.getenv("PRIVATE_IP", "").lower() in ("true", "1", "yes") else IPTypes.PUBLIC

            connector = Connector(ip_type)

            def getconn() -> pymysql.connections.Connection:
                return connector.connect(
                    connection_name,
                    "pymysql",
                    user=db_user,
                    password=db_password,
                    db=db_name,
                )

            return create_engine("mysql+pymysql://", creator=getconn)
        else:
            """Create a connection to the MySQL database"""
            db_user = self.get_config_value("DB_USER")
            db_password = self.get_config_value("DB_PASSWORD")
            db_host = self.get_config_value("DB_HOST")
            db_port = self.get_config_value("DB_PORT")
            db_name = self.get_config_value("DB_NAME")

            DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        return create_engine(DATABASE_URL, echo=self.DEBUG)


class SettingsFactory:
    """
    Factory to instantiate the appropriate settings class based on environment
    """

    @staticmethod
    def get_settings() -> BaseSettings:
        """Return the settings instance based on the current environment"""
        environment = os.getenv("ENV", "DEV").upper()
        if environment == "DEV":
            return DevSettings()
        # elif environment == "PRO":
        #     return ProdSettings()
        else:
            raise ValueError(f"Unsupported environment: {environment}")


# Instantiate the settings dynamically

settings = SettingsFactory.get_settings()
