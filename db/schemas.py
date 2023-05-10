from pydantic import BaseModel, validator, root_validator


class Users(BaseModel):
    email: str
    phone: int
    fam: str
    name: str
    otc: str


class Coords(BaseModel):
    latitude: float
    longitude: float
    height: int


class Levels(BaseModel):
    winter: str = None
    summer: str = None
    autumn: str = None
    spring: str = None


class PerevalAdded(BaseModel):
    created_by: list[Users]
    coord_id: list[Coords]
    levels_id: list[Levels]
    beauty_title: str
    title: str
    other_titles: str = None
    connect: str = None


class Images(BaseModel):
    title: str
    image: bytearray


class PerevalImage(BaseModel):
    ...


class PerevalAreas(BaseModel):
    parent_id: int
    title: str


class SprActivitiesTypes(BaseModel):
    title: str
