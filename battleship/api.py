from http import HTTPStatus

from flask import Flask, jsonify, request, session

# Json
import json

# Battleship
from battleship.domain.classes import Battleship
# Exceptions
from battleship.core import exceptions as battleship_exceptions
# Utilities
from battleship.utils.functions import id_generator


app = Flask(__name__)
app.secret_key = id_generator(size=12)


# ! Shouldn't be using this in production environment
# ! Could use a database or try to serialize each Battleship game data into JSON
GAMES = {}


@app.route('/battleship', methods=['POST'])
def create_battleship_game():
    ships = json.loads(request.data)

    # current_game_id = session.get('game_id', None)
    # if current_game_id:
    #     del GAMES[current_game_id]
    #     session.pop('game_id', None)

    try:
        battleship = Battleship(ships=ships, board=(10, 10))
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

        # add game to session variable, games
        game_id = id_generator(size=6)
        session['game_id'] = game_id
        GAMES.setdefault(game_id, battleship)
        
        print(f"New Game! -> {session['game_id']}")

    response = {
        'result': message,
        'game_id': game_id
    }

    return jsonify(response), http_status


@app.route('/battleship', methods=['PUT'])
def shot():
    data = json.loads(request.data)

    xy_pos = data['positions']

    # game_id = session.get('game_id', None)
    game_id = data['game_id']

    battleship = GAMES[ game_id ]

    try:
        result = battleship.hit( **xy_pos )
    except battleship_exceptions.ShotOutOfBoardException:
        result = {}
        http_status = HTTPStatus.BAD_REQUEST
    else:
        http_status = HTTPStatus.OK

    return jsonify(result), http_status


@app.route('/battleship', methods=['DELETE'])
def delete_battleship_game():
    # game_id = session.get('game_id', None)
    http_status = HTTPStatus.BAD_REQUEST

    data = json.loads(request.data)
    game_id = data.get('game_id', None)

    response = {}

    if game_id in GAMES:
        # there's a game to delete
        print(f"Deleting game -> {game_id}")
        del GAMES[game_id]
        http_status = HTTPStatus.OK

        response.update({
            'response': f"Game with ID {game_id} deleted. {len(GAMES)} games remaining.",
        })

    return jsonify(response), http_status
