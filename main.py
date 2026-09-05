import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from core.limiter import limiter
from database import engine
from routers import auth, task, user


@asynccontextmanager
async def lifespan(app: FastAPI):
	# Startup
	yield

	# Shutdown
	await engine.dispose()

app = FastAPI(title='Task API', version = '1.0.0' , lifespan=lifespan)

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) #type:ignore

app.include_router(task.router)
app.include_router(user.router)
app.include_router(auth.router)

logger = logging.getLogger(__name__)


@app.exception_handler(Exception)
async def global_exception_handler(request : Request, exc : Exception):
    logger.error('Unhandled excpetion occurred', exc_info=True)
    
    return JSONResponse(
		status_code=500,
		content={'detail':'An unexpected error has occurred.'}
    )


