from api.endpoints import locations
from fastapi import FastAPI


app = FastAPI()
app.include_router(locations.router)
