from fastapi import Header, HTTPException
from dotenv import load_dotenv
from starlette.status import HTTP_401_UNAUTHORIZED
import os
load_dotenv()

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != os.getenv("AUTH_KEY"):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key!",
        )

