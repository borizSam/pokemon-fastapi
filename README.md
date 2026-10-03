# Pokemon API

API REST rápida construida con [FastAPI](https://fastapi.tiangolo.com/) que expone un catálogo de Pokémon en memoria. Pensada para levantarse al instante, sin base de datos ni dependencias externas.

## Características

- CRUD completo sobre Pokémon (crear, leer, actualizar, borrar)
- Filtros por tipo y nombre
- Documentación interactiva automática (Swagger / ReDoc)
- Lista para correr en local con un entorno virtual o en Docker

## Stack

- Python 3.11
- FastAPI
- Uvicorn (servidor ASGI)

## Estructura del proyecto

```
.
├── main.py             # Código de la API (modelos, datos y endpoints)
├── requirements.txt    # Dependencias
├── Dockerfile          # Imagen de la API
└── .dockerignore
```

## Cómo correrlo en local

```bash
python3 -m venv venv
source venv/bin/activate        # en Windows: venv\Scripts\activate
pip install -r requirements.txt

uvicorn main:app --reload
```

La API quedará disponible en `http://127.0.0.1:8000`.

## Cómo correrlo con Docker

```bash
docker build -t pokemon-api .
docker run -d -p 8000:8000 --name pokemon-api pokemon-api
```

## Documentación interactiva

Con la API corriendo, abrí en el navegador:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints

| Método | Ruta                      | Descripción                                   |
|--------|---------------------------|------------------------------------------------|
| GET    | `/`                       | Info general de la API                         |
| GET    | `/pokemon`                | Lista todos los Pokémon (filtros opcionales)    |
| GET    | `/pokemon?type=Fire`      | Filtra por tipo                                 |
| GET    | `/pokemon?name=char`      | Busca por nombre (parcial)                      |
| GET    | `/pokemon/{id}`           | Obtiene un Pokémon por id                       |
| GET    | `/pokemon/name/{name}`    | Obtiene un Pokémon por nombre exacto            |
| POST   | `/pokemon`                | Crea un nuevo Pokémon                           |
| PUT    | `/pokemon/{id}`           | Actualiza un Pokémon existente                  |
| DELETE | `/pokemon/{id}`           | Elimina un Pokémon                              |

## Ejemplos con curl

Obtener un Pokémon por id:

```bash
curl http://127.0.0.1:8000/pokemon/1
```

Filtrar por tipo:

```bash
curl "http://127.0.0.1:8000/pokemon?type=Water"
```

Crear un Pokémon:

```bash
curl -X POST http://127.0.0.1:8000/pokemon \
  -H "Content-Type: application/json" \
  -d '{"name":"Mewtwo","type":"Psychic","hp":106,"attack":110,"defense":90,"speed":130}'
```

Actualizar un Pokémon:

```bash
curl -X PUT http://127.0.0.1:8000/pokemon/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Bulbasaur","type":"Grass","hp":50,"attack":49,"defense":49,"speed":45}'
```

Eliminar un Pokémon:

```bash
curl -X DELETE http://127.0.0.1:8000/pokemon/1
```

## Notas

Los datos viven en memoria: se reinician cada vez que se reinicia el proceso o el contenedor. No hay persistencia en disco ni base de datos.
