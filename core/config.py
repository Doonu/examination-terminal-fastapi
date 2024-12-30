import os
from dotenv import load_dotenv
from pathlib import Path


from pydantic_settings import BaseSettings
from pydantic import BaseModel

env_file = ".env.prod" if os.getenv("ENV") == "prod" else ".env.dev"
load_dotenv(env_file)

BaseDir = Path(__file__).parent.parent


class DbSetting(BaseModel):
    print(os.getenv("DATABASE_URL"))
    url: str = os.getenv("DATABASE_URL")
    echo: bool = True


class AuthJWT(BaseModel):
    private_key_path: Path = BaseDir / "certs" / "jwt-private.pem"
    public_key_path: Path = BaseDir / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db: DbSetting = DbSetting()
    auth: AuthJWT = AuthJWT()


settings = Settings()
