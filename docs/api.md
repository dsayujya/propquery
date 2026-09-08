# API Documentation

The RESTful API is built with FastAPI and strictly typed using Pydantic.

## Authentication
All endpoints (except `/auth/login`) are protected by a JWT authorization dependency (`get_current_user`).

- `POST /api/v1/auth/login`: Accepts OAuth2 form data (`username`, `password`) and returns a JWT `access_token`.

## Core Endpoints
All entities follow a standard RESTful structure:
- `GET /api/v1/{entity}/` (List all)
- `GET /api/v1/{entity}/{id}` (Get by ID)
- `POST /api/v1/{entity}/` (Create new)
- `PATCH /api/v1/{entity}/{id}` (Update)
- `DELETE /api/v1/{entity}/{id}` (Delete)

Entities: `/properties`, `/tenants`, `/units`, `/leases`, `/payments`, `/maintenance`, `/support`.

## Exception Handling
We utilize custom centralized exception handlers (`app/utils/exceptions.py`) to catch errors at the Service or Repository level and return consistent JSON structures to the client.

Example response for a `NotFoundError`:
```json
{
  "detail": "Support Ticket with ID 404 not found."
}
```
