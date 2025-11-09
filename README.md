# Weather Service API

Mini-service for storing city temperatures built with Django and Django REST Framework.

## Features

### Manage cities (CRUD):

`GET /api/city/` - list all cities

`GET /api/city/{id}/ `- get details of a city

`POST /api/city/` - create a city

`PATCH /api/city/{id}/` - update city fields (partial update)

`DELETE /api/city/{id}/` - delete a city

### Store temperature measurements per city:

`POST /api/city/{id}/setTemperature/` - add a temperature value for a city

### Get average temperatures:

`GET /api/stats/` - average temperature across all cities

`GET /api/stats/?city_id={id}` - average temperature for a specific city

#### Uses sqlite as database

#### Uses virtualenv for isolation

**Note:** id is a UUID string.

---
## Tech stack

- Python 3.12
- Django
- Django REST Framework
- SQLite

---
## Setup and run

Create and activate virtual environment:

```bash
   python3 -m venv venv
```
```bash
   . venv/bin/activate
```

---
## Install dependencies:

```bash
   pip install -r requirements.txt
```

---
## Apply migrations:

```bash
   python manage.py makemigrations
```
```bash
   python manage.py migrate
```

---
## Run development server:

```bash
python manage.py runserver 8001
```

### API will be available at:

http://127.0.0.1:8001/api/

---
## Models
### City

- `id` — UUID (primary key)
- `name` — string, city name
- `description` — text, city description
- `created_at` — datetime, set automatically on creation
- `updated_at` — datetime, set automatically on update

### CityTemperature

- `id` — UUID (primary key)
- `city` — FK to City
- `value` — float, temperature value
- `created_at` — datetime, set automatically on creation
- `updated_at` — datetime, set automatically on update

---
## API endpoints
1. List cities

`GET /api/city/`

*Response:*

```
{
  "cities": [
    {
      "id": "2ae03fc5-69a9-4a7a-8f39-ce5a464177bb",
      "name": "Kyiv",
      "description": "the big city"
    }
  ]
}
```

2. Create city

`POST /api/city/`

*Request body:*

```
{
  "name": "Odesa",
  "description": "my best some city"
}
```

*Response (201):*
```
{
  "id": "017a2fa4-e4c2-4704-82fe-a1edf0d4ed68",
  "name": "Odesa",
  "description": "my best some city"
}
```

3. Get city details

`GET /api/city/{id}/`

*Response (example):*
```
{
  "id": "017a2fa4-e4c2-4704-82fe-a1edf0d4ed68",
  "name": "Odesa",
  "description": "my best some city"
}
```

4. Update city (partial)

`PATCH /api/city/{id}/`

*Request body (example):*

`{
  "description": "another city"
}`


*Response (example):*

```
{
  "id": "017a2fa4-e4c2-4704-82fe-a1edf0d4ed68",
  "name": "Odesa",
  "description": "another city"
}
```

5. Delete city

`DELETE /api/city/{id}/`

*Response:*

```
204 No Content
```

6. Add temperature for city

`POST /api/city/{id}/setTemperature/`

`{id}` - UUID of the city

*Request body:*

`{
  "value": 12.4
}`


*Response (201):*

`{
  "value": 12.4
}`


Temperature is saved with a timestamp in the database automatically.

7. Get average temperature (global)

`GET /api/stats/`

*Response:*

`{
  "average": 12.4
}`

8. Get average temperature for a city

`GET /api/stats/?city_id={id}`

**Example:**

`GET /api/stats/?city_id=017a2fa4-e4c2-4704-82fe-a1edf0d4ed68`

*Response:*

```
{
  "average": 12.4
}
```

---
## Tests

### Unit tests cover:

CRUD operations for City

- Adding temperature via /city/{id}/setTemperature/
- Stats endpoint /stats/ with and without city_id filter

### Run tests:
```bash
   python manage.py test cities
```

---
## Swagger Documentation

`Swagger UI:`
http://127.0.0.1:8001/swagger/

`Redoc UI:`
http://127.0.0.1:8001/redoc/

`OpenAPI JSON:`
http://127.0.0.1:8001/swagger.json
