import importlib
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path='app/.env') #load env variabls
my_var = os.getenv('DATABASE_PORT')
#print(my_var)

# package_name = "pydantic_settings"
# module = importlib.import_module(package_name)
# BaseSettings = getattr(module, "BaseSettings")
from pydantic_settings import BaseSettings

# make validation that all of var environments are set
class Settings(BaseSettings):
    database_hostname: str 
    database_port: str  
    database_password: str 
    database_name: str 
    database_username: str 

    secret_key: str 
    algorithm: str 
    access_token_expire_minutes: int 


    class Config:
        env_file = find_dotenv(".env")


settings = Settings()
#print(module)
