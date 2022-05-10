# Python
from asyncio import streams
from typing import Optional
from anyio import Path

#  Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()


# Models
class Location(BaseModel):
    city: str
    state: str
    county: str


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
        title="Person name",
        description="This is the person name, It;s between 1 and 50 characters"
    ),
    age: int = Query(
        ...,
        title="Person age",
        description="This is the age of the person, It's required"
    )
):
    return {name: age}

# Validations: Path Parameters


@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="The id of the person",
        description="It's the id for the person"
    )
):
    return {person_id: "It exists!"}


# Validations Request Body
@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="The person_id with the update",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...),
):
    result = dict(person)
    result.update(dict(location))

    # FastAPI no support the sintatxis
    # person.dict() & location.dict()

    return result
