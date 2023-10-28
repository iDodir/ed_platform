import uvicorn
from fastapi import FastAPI, APIRouter

from api.handlers import user_router

app = FastAPI(
    title="Educational platform",
)

main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
