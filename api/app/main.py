import uvicorn
from fastapi import FastAPI

from app.config.postgres import create_tables
from app.routers import user, jump, landing

create_tables()

app = FastAPI()

app.include_router(user.router)
app.include_router(jump.router)
app.include_router(landing.router)


@app.get("/")
async def root():
    return {"message": "SW00P GENERATOR3000"}


# if __name__ == "__main__":
#     uvicorn.run(app, port=8082)
