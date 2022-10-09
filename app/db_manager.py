from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Union

from sqlalchemy.orm import Query

from app.db_config import session
from app.models import RestaurantRating, Restaurant


class DbManager:
    def __init__(self):
        self.restaurant = RestaurantManager()
        self.rating = RestaurantRatingManager()


class DBRepo:
    @staticmethod
    def create(**kwargs) -> Union[RestaurantRating, Restaurant]:
        obj = RestaurantRating(**kwargs)

        session.add(obj)
        session.commit()
        return obj

    @staticmethod
    def as_dict(obj: Union[RestaurantRating, Restaurant]) -> dict:
        """ Serialize SQLAlchemy object """

        result = {}
        for element in obj.__table__.columns:
            if isinstance(getattr(obj, element.name), Decimal):
                result[element.name] = float(getattr(obj, element.name))
            elif isinstance(getattr(obj, element.name), datetime):
                result[element.name] = getattr(obj, element.name).strftime('%d/%m/%Y %H:%M')
            else:
                result[element.name] = getattr(obj, element.name)
        return result

    @staticmethod
    def get_rating_history(restaurant_id: int) -> List[Dict]:
        """ Returns rating history as dict """

        restaurant_ratings: Query = session.query(RestaurantRating).filter(RestaurantRating.restaurant == restaurant_id)

        result: list = []
        for element in restaurant_ratings:
            result.append(
                {
                    "taste": element.taste,
                    "size": element.taste,
                    "service": element.taste,
                    "create_at": element.created_at.strftime('%d/%m/%Y %H:%M')
                }
            )
        return result

    @staticmethod
    def get_rating(restaurant_id: int) -> Dict:
        """ Return rating summary for restaurant """

        restaurant_ratings: Query = session.query(Restaurant).filter(Restaurant.id == restaurant_id)

        if restaurant_ratings.count() >= 1:
            restaurant: Restaurant = restaurant_ratings.first()
            category_rating_avg: str = round(
                (float(restaurant.taste_avg) +
                 float(restaurant.size_avg) +
                 float(restaurant.service_avg))/3
            ) * '*'
            category_rating_points_avg: float = round(
                float(restaurant.taste_rating_points) +
                float(restaurant.size_rating_points) +
                float(restaurant.service_rating_points), 2
            )/3

            result: dict = {
                "name": restaurant.name,
                "taste_rating": round(float(restaurant.taste_rating_points), 2),
                "taste_avg": round(float(restaurant.taste_avg)) * '*',
                "size_rating_points": round(float(restaurant.size_rating_points), 2),
                "size_avg": round(float(restaurant.size_avg)) * '*',
                "service_rating_points": round(float(restaurant.service_rating_points), 2),
                "service_avg": round(float(restaurant.service_avg)) * '*',
                "category_rating_avg": category_rating_avg,
                "category_rating_points_avg": category_rating_points_avg
            }

            return result


class RestaurantRatingManager(DBRepo):
    ...


class RestaurantManager(DBRepo):
    ...

