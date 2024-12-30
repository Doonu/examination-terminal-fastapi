import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api_v1 import router as router_v1
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


if os.getenv("ENV") == "dev":
    origins = ["http://45.10.43.121:3000"]
else:
    origins = ["*"]


app = FastAPI(title="Terminal app", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router_v1, prefix=settings.api_v1_prefix)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
