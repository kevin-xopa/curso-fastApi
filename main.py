# Python
from asyncio import streams
from typing import Optional
from anyio import Path
from enum import Enum

#  Pydantic
from pydantic import BaseModel, Field

# FastAPI
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()

# ENUMS


class HairColor(Enum):
    white = 'white',
    brow = 'brow'
    red = 'red'
    blonde = 'blonde'
    black = 'black'

# Models


class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=200,
        example="Cholula"
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=200,
        example="Puebla"
    )
    county: str = Field(
        ...,
        min_length=1,
        max_length=200,
        example="Mexico"
    )


class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        example="Kevin"
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        example="Xopa"
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=21
    )
    hair_color: Optional[HairColor] = Field(
        default=None,
        example="black"
    )
    is_married: Optional[bool] = Field(
        default=None,
        example=False,
    )

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name" : "Kevin",
    #             "last_name" : "Ochoa Xopa",
    #             "age" : 21,
    #             "hair_color" : "black",
    #             "is_married" : False,
    #         }
    #     }


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
        description="This is the person name, It;s between 1 and 50 characters",
        example="Rocio"
    ),
    age: int = Query(
        ...,
        title="Person age",
        description="This is the age of the person, It's required",
        example=25
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
        description="It's the id for the person",
        example=42
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
        gt=0,
        example=86
    ),
    person: Person = Body(...),
    # location: Location = Body(...),
):
    # result = dict(person)
    # result.update(dict(location))

    # FastAPI no support the sintatxis
    # person.dict() & location.dict()

    # return result
    return person
