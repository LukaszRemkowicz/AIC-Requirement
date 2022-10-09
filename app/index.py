import argparse
import logging
import os
import sys

module_path = os.path.abspath(os.getcwd() + '\\..')
if module_path not in sys.path:
    sys.path.append(module_path)

from app.db_manager import DbManager  # noqa
from app.app_config import get_module_logger  # noqa

logger: logging.Logger = get_module_logger("cmd")


def create_parser():
    parser = argparse.ArgumentParser(description="Main Command line interface for restaurant app.")
    parser.add_argument(
        '-rr',
        '--rate-restaurant',
        dest='rate_restaurant',
        action='store_true',
        help='Rate restaurant function'
    )
    parser.add_argument(
        '-a',
        '--attributes',
        dest='attributes',
        nargs='+',
        type=str,
        help='Write ratings: restaurant_id, bill_value, taste, size, service'
    )
    parser.add_argument(
        '-grh',
        '--get_rating_history',
        dest='get_rating_history',
        action='store_true',
        help='Get rating history'
    )
    parser.add_argument(
        '-gr',
        '--get_rating',
        dest='get_rating',
        action='store_true',
        help='Get rating history'
    )
    parser.add_argument(
        '-id',
        '--id',
        dest='id',
        metavar='Object id',
        nargs='+',
        type=int,
        help='Object id'
    )

    return parser


def is_int(string: str) -> bool:
    try:
        int(string)
        return True
    except ValueError:
        return False


class CmdLineInterface:

    def __init__(self):
        self.manager = DbManager()
        parser = create_parser()
        self.args = parser.parse_args()

    def parse(self) -> None:
        """ Parse attributes from command line. """

        if self.args.attributes and self.args.rate_restaurant:
            attributes: list = self.args.attributes[0].split(' ')
            attributes = [(lambda x: int(x))(x) for x in attributes if is_int(x)]
            assert len(attributes) == 5, """Wrong parameters number. Should be 5: restaurant_id, 
            bill_value, taste, size, service"""

            self.rate_restaurant(*attributes)

        if self.args.get_rating_history and self.args.id:
            logger.info(self.get_rating_history(*self.args.id))

        if self.args.get_rating and self.args.id:
            logger.info(self.get_rating(*self.args.id))

    def rate_restaurant(self, restaurant_id: int, bill_value: float, taste: int, size: int, service: int) -> None:
        self.manager.rating.create(
            taste=taste, size=size, service=service, bill_value=bill_value, restaurant=restaurant_id
        )

    def get_rating_history(self, restaurant_id: int) -> dict:
        return self.manager.rating.get_rating_history(restaurant_id)

    def get_rating(self, restaurant_id: int) -> dict:
        return self.manager.rating.get_rating(restaurant_id)


CmdLineInterface().parse()
