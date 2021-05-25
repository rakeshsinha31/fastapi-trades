from starlette import background
import uvicorn
from fastapi import FastAPI
from pymongo import MongoClient, ASCENDING
from fastapi.middleware.cors import CORSMiddleware

from api.routers import router
from config import settings

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = MongoClient(
        "mongodb+srv://admin:admin@cluster0.e1lvn.mongodb.net/")
    app.mongodb = app.mongodb_client.fastapi
    # app.mongodb["trade"].create_index([
    #     ('instrumentId', "text")],
    #     name='my_index')


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(router, tags=["trade"], prefix="/trades")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
