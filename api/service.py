from fastapi import APIRouter

service_router = login_router = APIRouter()


@service_router.get("/ping")
async def ping():
    # import random
    # err = random.choice(
    #     [ZeroDivisionError, ValueError, TypeError],
    # )
    # raise err
    return {"Success": True}
