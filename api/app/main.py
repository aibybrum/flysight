from fastapi import FastAPI
from .routers import user, jump, landing
from .config.postgres import create_tables

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
