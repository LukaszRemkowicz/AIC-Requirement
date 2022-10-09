from pydantic import BaseModel


class RestaurantPydantic(BaseModel):

    name: str
    taste_rating_points: float
    taste_avg: float
    size_rating_points: float
    size_avg: float
    service_rating_points: float
    service_avg: float


class RestaurantRatingPydantic(BaseModel):

    restaurant: int
    taste: int
    size: int
    service: int
    bill_value: float

    class Config:
        orm_mode = True
