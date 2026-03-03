from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.limiter import limiter
from app.api import task_router
from app.schemas.task import SuccessResponse

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(task_router)

@app.get("/")
async def root() -> SuccessResponse:
    return SuccessResponse()
