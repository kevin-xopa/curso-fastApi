# Python
from typing import Optional
from anyio import Path

#  Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI, Body, Query, Path;

app = FastAPI()


# Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None



@app.get("/")
def home():
    return {'Hello': 'world'}



# Request and Response Body
@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Validations: Query parameters


@app.get("/person/details")
def show_person(
    name: Optional[str] = Query(
        None, min_length=1,
        max_length=50,
        title = "Person name",
        description = "This is the person name, It;s between 1 and 50 characters"
        ),
    age: int = Query(
        ...,
        title = "Person age",
        description = "This is the age of the person, It's required"
        )
):
    return {name:age}

# Validations: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt = 0,
        title = "The id of the person",
        description = "It's the id for the person"
        )
):
    return {person_id: "It exists!"}