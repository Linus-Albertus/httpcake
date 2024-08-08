import httpie
import os

from dotenv import import load_dotenv


load_dotenv()


def token_auth():
    USER = os.getenv("USER")
    PWRD = os.getenv("PWRD")
    
