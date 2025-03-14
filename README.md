# MyLocations

## Overview
This project consists of a **FastAPI** backend with **PostgreSQL** as the database and a **React** frontend using Bootstrap for styling. The application is containerized with Docker for easy deployment and local development.

This full-stack application allows users to register and log in using JWT-based authentication. Once authenticated, users can add, edit, delete, and view their list of preferred locations.


## Features
- **Backend**: FastAPI with PostgreSQL database.
- **Other worth mentioning libraries** Pydantic, Alembic, SQLAlchemy
- **Test**: Pytest tests using Mocking.
- **Frontend**: React app styled with Bootstrap.
- **Authentication**: JWT-based authentication.
- **Docker Support**: Uses `docker-compose` for orchestration.
- **API Integration**: Communicates with external APIs.

## Prerequisites
Make sure you have the following installed:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/JonatasLemos/mylocations.git
    cd mylocations
    ```

2. Create a `.env` file in the root directory with the necessary environment variables:
    ```sh
    DATABASE_URL=postgresql://your_user:your_password@db:5432/your_db
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    REFRESH_SECRET_KEY=your_refresh_secret_key
    ```
## Generating Secret Keys
The `SECRET_KEY` and `REFRESH_SECRET_KEY` are used for JWT authentication. You can generate a secure secret key using Python:
```sh
python -c 'import secrets; print(secrets.token_hex(32))'
```
Use this generated key as the value for `SECRET_KEY` and `REFRESH_SECRET_KEY` in your `.env` file.

## Running the Project with Docker

1. Build and start the containers:
    ```sh
    docker-compose up --build
    ```
2. The services will be available at:
   - **Backend**: `http://localhost:8000`
   - **Frontend**: `http://localhost:3000`

3. To stop the containers:
    ```sh
    docker-compose down
    ```

## Running Tests
To run the tests for the backend, first open a shell in the container
```sh
docker exec -it your_backend_container_id sh
```
Then execute
```sh
python3 -m pytest
```

## Project Structure
```
backend:
├── alembic
│   └── versions
├── api
│   ├── endpoints
│   ├── services
│   └── utils
├── core
├── models
├── schemas
└── test

frontend:
├── build
├── node_modules
├── public
└── src
    ├── api
    │   └── utils
    └── components
```

## API Documentation
For a better understanding of the API, visit the FastAPI interactive documentation:
- [Swagger UI](http://localhost:8000/docs) - Provides an interactive API interface to test endpoints.
- [ReDoc](http://localhost:8000/redoc) - Offers a structured and detailed view of the API schema.

## Next steps

In future updates, the application aims to integrate a Leaflet-powered interactive map and a PostgreSQL database with PostGIS support for advanced geospatial capabilities. The goal is to provide a rich experience where users can store their favorite locations along with images, descriptions, and other details.

## Contributing
Feel free to submit issues and pull requests to improve the project!

## License
This project is licensed under the MIT License.
