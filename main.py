from fastapi import FastAPI
from api.auth import verify_api_key
from api.v1.endpoints import router as endpoints_router

app = FastAPI()
app.include_router(endpoints_router, prefix="/v1", tags=["v1"])

@app.get("/welcome")
def return_welcome():
    return {"message": "Welcome to the API!"}
