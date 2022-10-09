import argparse
import os
import sys

module_path = os.path.abspath(os.getcwd() + '\\..')
if module_path not in sys.path:
    sys.path.append(module_path)

from sqlalchemy.exc import IntegrityError, InvalidRequestError  # noqa
from models import Restaurant  # noqa
from db_config import session, Base, engine  # noqa
from db_manager import DbManager  # noqa


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Command line interface for restaurant app.")
    return parser


class CmdLineInterface:
    parser = create_parser()
    manager = DbManager()
    try:
        Base.metadata.create_all(engine)
    except InvalidRequestError:
        pass

    @staticmethod
    def create_restaurants() -> None:
        """ Create restaurants in DB """
        try:
            restaurant1 = Restaurant(name="A'Bracciate Pasta & Wine")
            restaurant2 = Restaurant(name="Acquario")
            restaurant3 = Restaurant(name="Arco by Paco Pérez")
            restaurant4 = Restaurant(name="Autentyk - Kuchnia I Ludzie")
            session.add(restaurant1)
            session.add(restaurant2)
            session.add(restaurant3)
            session.add(restaurant4)
            session.commit()

        except IntegrityError:
            session.rollback()

    def rate_restaurant(self, restaurant_id: int, bill_value: float, taste: int, size: int,  service: int) -> None:
        self.manager.rating.create(
            taste=taste, size=size, service=service, bill_value=bill_value, restaurant=restaurant_id
        )

    def rate(self) -> None:
        self.rate_restaurant(1, 4, -1, 2, 2)
        self.rate_restaurant(1, 31, 3, 2, 2)
        self.rate_restaurant(1, 2, 1, 2, 2)
        self.rate_restaurant(1, 23, 0, 2, 2)


CmdLineInterface().create_restaurants()
CmdLineInterface().rate()
