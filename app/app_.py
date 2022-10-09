import os
import sys

module_path = os.path.abspath(os.getcwd() + '\\..')
if module_path not in sys.path:
    sys.path.append(module_path)

import uvicorn as uvicorn
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status

from app.db_manager import DbManager
from app.schemas import RestaurantRatingPydantic
from app.db_config import sessionLocal

fastapi_app = FastAPI()
db_manager = DbManager()


def get_db() -> sessionLocal:
    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()


@fastapi_app.post('/rate_restaurant', status_code=status.HTTP_201_CREATED)
def create_rating(rating: RestaurantRatingPydantic) -> JSONResponse:
    rating = db_manager.rating.create(**rating.dict())

    return JSONResponse(db_manager.rating.as_dict(rating))


@fastapi_app.get('/restaurant-rating/{restaurant_id}/', status_code=status.HTTP_200_OK)
def create_rating(restaurant_id: int) -> JSONResponse:
    rating = db_manager.rating.get_rating(restaurant_id)

    return JSONResponse(rating)


@fastapi_app.get('/restaurant-history-rating/{restaurant_id}/', status_code=status.HTTP_200_OK)
def create_rating(restaurant_id: int) -> JSONResponse:
    rating = db_manager.rating.get_rating_history(restaurant_id)

    return JSONResponse({'result': rating})


if __name__ == "__main__":
    uvicorn.run("app.app_:fastapi_app", host="0.0.0.0", port=8000, reload=True)
