from collections import namedtuple
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, Integer, String, Float, ForeignKey, desc, DateTime
from sqlalchemy import event
from sqlalchemy.orm import object_session, Query
from sqlalchemy.orm.attributes import set_committed_value

from app.utils.rating_utils import calculate_rating
from app.db_config import Base, session, engine


class Restaurant(Base):
    __tablename__ = 'restaurant'  # noqa
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    taste_rating_points = Column(Float(precision=2, asdecimal=True, decimal_return_scale=None), default=0.00)
    taste_avg = Column(Float(precision=2, asdecimal=True, decimal_return_scale=None), default=0.00)
    size_rating_points = Column(Float(precision=2, asdecimal=True, decimal_return_scale=None), default=0.00)
    size_avg = Column(Float(precision=2, asdecimal=True, decimal_return_scale=None), default=0.00)
    service_rating_points = Column(Float(precision=2, asdecimal=True, decimal_return_scale=None), default=0.00)
    service_avg = Column(Float(precision=2, asdecimal=True, decimal_return_scale=None), default=0.00)


class RestaurantRating(Base):
    __tablename__ = 'restaurant_rating'  # noqa
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    restaurant = Column(Integer, ForeignKey("restaurant.id"))
    taste = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    service = Column(Integer, nullable=False)
    bill_value = Column(Float(asdecimal=True), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


@event.listens_for(RestaurantRating, "before_insert")
def _init_some_attribute(mapper, connection, target):
    """ before save method """

    restaurant_obj: Restaurant = session.query(Restaurant).filter(Restaurant.id == 1).first()
    restaurant_rating: Query = session.query(RestaurantRating).filter(RestaurantRating.restaurant == target.restaurant)

    categories: list = ['taste', 'size', 'service']
    restaurant_category_rating_mapping: dict = {
        'taste': 'taste_rating_points',
        'size': 'size_rating_points',
        'service': 'service_rating_points'
    }
    restaurant_category_avg_mapping: dict = {
        'taste': 'taste_avg',
        'size': 'size_avg',
        'service': 'service_avg'
    }
    session_obj = object_session(target)

    for category in categories:
        if restaurant_rating.count() >= 1:
            bill_sum: float = sum([obj.bill_value for obj in restaurant_rating]) + Decimal(target.bill_value)

            restaurant_rating: Query = restaurant_rating.order_by(desc('id'))
            Rating = namedtuple('rating', f'{category} bill')
            OldRating = namedtuple('old_rating', f'{category} bill')
            rating_average: tuple = calculate_rating(
                getattr(restaurant_obj, restaurant_category_rating_mapping[category]),
                bill_sum,
                OldRating(
                    getattr(restaurant_rating.first(), category),
                    restaurant_rating.first().bill_value
                ),
                Rating(getattr(target, category), target.bill_value)
            )

            new_rating_points, new_rating_avg = rating_average

        else:
            rating_points: int = getattr(target, category) * target.bill_value
            new_rating_points, new_rating_avg = rating_points, rating_points/target.bill_value

        data = {
            restaurant_category_rating_mapping[category]: new_rating_points,
            restaurant_category_avg_mapping[category]: new_rating_avg
        }

        if not session_obj.is_modified(target, include_collections=False):
            return
        connection.execute(
            Restaurant.__table__.
            update().
            values(**data).
            where(Restaurant.id == target.restaurant))

        parent_key = session.identity_key(Restaurant, target.restaurant)

        try:
            the_parent = session_obj.identity_map[parent_key]

        except KeyError:
            pass

        else:
            set_committed_value(
                the_parent, restaurant_category_rating_mapping[category], new_rating_points
            )
            set_committed_value(
                the_parent, restaurant_category_avg_mapping[category], new_rating_avg
            )
    return


Base.metadata.create_all(engine)
