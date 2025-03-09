from api.endpoints import location_types, locations, users
from fastapi import FastAPI
from fastapi_pagination import add_pagination


app = FastAPI()
add_pagination(app)
app.include_router(locations.router)
app.include_router(users.router)
app.include_router(location_types.router)
