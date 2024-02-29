from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "Bruno app con FastApi"
app.version = "0.0.0.0.0.1"


# Dejé acá
# https://platzi.com/new-home/clases/9012-fastapi/67258-validando-tokens/

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default="Nueva película", min_length=2, max_length=15)
    overview: str = Field(default="Esta es una reseña de la película", min_length=10, max_length=50)
    year: int = Field(default=2000, le=2025)
    rating: float = Field(default=6.0, ge=0, le=10)
    category: str = Field(default="Nueva categoría", min_length=2, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Lo que el viento se llevó",
                "overview": "Primera película con sonido",
                "year": 1939,
                "rating": 6.0,
                "category": "Drama"
            }
        }

movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
    {
        "id": 2,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    }
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world!</h1>')


@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies)

@app.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=500)) -> Movie:
    for item in movies:
        if item["id"] == id:
            return JSONResponse(status_code=200, content=item)
    return JSONResponse(status_code=404, content=[])

@app.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=2000)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [ item for item in movies if item['category'] == category]
    return JSONResponse(status_code=2000, content=data)


@app.post('/movies/', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={'message': "Se ha registrado una nueva película"})

@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return JSONResponse(status_code=200, content={'message': "Se ha modificado exitosamente"})
    return JSONResponse(status_code=401, content={'message': "No se modificó un carajo"})

@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={'message': "Se ha borrado exitosamente"})
