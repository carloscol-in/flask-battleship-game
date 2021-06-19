"""Utilities functions."""

# Flask
from http import HTTPStatus

# Libraries
import string
import random
from typing import Tuple

# Exceptions
from battleship.core import exceptions as battleship_exceptions


def id_generator(size=4, chars=string.ascii_letters + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

def create_game(
    ships={
        "ships": [
            {
                "x": 2,
                "y": 1,
                "size": 4,
                "direction": "H"
            },
            {
                "x": 7,
                "y": 4,
                "size": 3,
                "direction": "V"
            },
            {
                "x": 3,
                "y": 5,
                "size": 2,
                "direction": "V"
            },
            {
                "x": 6,
                "y": 8,
                "size": 1,
                "direction": "H"
            }
        ]
    },
    board=(10, 10)):
    """Create a new game from scratch."""
    # Battleship
    from battleship.domain.classes import Battleship

    # battleship = Battleship(ships=ships, board=board)
    # game_id = id_generator(size=6)
    game_id = None
    try:
        battleship = Battleship(ships=ships, board=board)
        # battleship, game_id = create_game(ships=ships, board=board)
    except battleship_exceptions.ShipsOutOfBoardException:
        message = "Ships out of board."
        http_status = HTTPStatus.BAD_REQUEST
    except battleship_exceptions.ShipsOverlapException:
        message = "Ships overlap."
        http_status = HTTPStatus.BAD_REQUEST
    except battleship_exceptions.InvalidDirectionException:
        message = "There's an invalid direction"
        http_status = HTTPStatus.BAD_REQUEST
    except battleship_exceptions.MissingDataException:
        message = "There's missing data"
        http_status = HTTPStatus.BAD_REQUEST
    else:
        message = "Game created successfully"
        http_status = HTTPStatus.OK

        game_id = id_generator(size=6)

        # add game to session variable, games
        # session['game_id'] = game_id

    return battleship, game_id, message, http_status