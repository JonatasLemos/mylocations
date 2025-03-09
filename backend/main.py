from api.endpoints import locations, users
from fastapi import FastAPI


app = FastAPI()
app.include_router(locations.router)
app.include_router(users.router)
