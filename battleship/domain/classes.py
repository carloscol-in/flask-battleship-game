"""Battleship game class."""

# Dependencies
import numpy as np
from typing import Tuple, Dict, List

# Exceptions
from battleship.core.exceptions import (
    MissingDataException,
    InvalidDirectionException,
    ShipsOverlapException,
    ShotOutOfBoardException,
    ShipsOutOfBoardException,
)
# Utilities
from battleship.utils.functions import id_generator


class Ship:
    """Ship class."""
    
    def __init__(self, **kwargs):
        self.ship_positions = self._create_ship_vector(**kwargs)

    def __repr__(self):
        return repr(self.ship_positions)

    def __delete__(self, instance):
        del self.ship_positions

    def _create_ship_vector(self, **kwargs):
        """Creates a list of all the positions taken by the ship."""
        x = kwargs.get('x', None)
        y = kwargs.get('y', None)
        size = kwargs.get('size', None)
        direction = kwargs.get('direction', None)

        if not x or not y or not size or not direction:
            raise MissingDataException("All ships should have x, y, size and direction.")

        v = []

        v.append( (x, y) )

        if direction == 'H':
            for i in range(1, size):
                v.append( ((x + i), y) )
        elif direction == 'V':
            for i in range(1, size):
                v.append( (x, (y + i)) )
        else:
            raise InvalidDirectionException("Direction should be `V` or `H`.")

        return v


class Fleet:
    """Ships object.
    
    This class can check if ships collide with each other.
    """
    def __init__(self, ships: Dict, board: Tuple[int, int] = (10, 10)):
        self.board = board
        self.positions = {}
        self.hits = {}
        self.ships = self._validate_ships( ships['ships'] )

    def __delete__(self, instance):
        del self.board
        del self.positions
        del self.hits
        del self.ships

    def _validate_ships(self, ships: List) -> Dict:
        created_ships = {}

        for ship in ships:
            ship_obj = Ship( **ship )

            if created_ships != {}:
                self._do_ships_clash(ship_obj, created_ships)
            
            # if last positions of ship are outside of board, raise 
            # ShipsOutOfBoardException
            xo, yo = ship_obj.ship_positions[-1]
            x_board, y_board = self.board
            if x_board <= xo or y_board <= yo:
                raise ShipsOutOfBoardException("Ships are out of board.")

            ship_id = id_generator(size=4)
            
            created_ships.setdefault( ship_id, ship_obj )
            self.positions.setdefault( ship_id, ship_obj.ship_positions )

        return created_ships

    def _do_ships_clash(self, ship: Ship, ship_dict: Dict):
        """This method determines if the `ship` overlaps with any of 
        the ships in the `ship_list`, in which case it raises the 
        Exception `ShipsOverlapException`."""

        for created_ship in ship_dict.values():
            for coordinate in ship.ship_positions:
                if coordinate in created_ship.ship_positions:
                    raise ShipsOverlapException("Ships shouldn't overlap.")

    def add_hit(self, ship_id, xy_pos: Tuple[int, int]):
        """This method is used to add the hits to the ships."""
        if ship_id in self.hits:
            if xy_pos in self.hits[ship_id]:
                print('Hit already registered')
                return
            self.hits[ship_id].append( xy_pos )
        else:
            self.hits.setdefault(ship_id, [xy_pos])

    def is_sunk(self, ship_id) -> bool:
        """This method helps you determine when a ship has sunk."""

        key_fn = lambda x: (x[0], x[1])

        if len(self.hits) == 0:
            return False

        if len(self.positions[ship_id]) != len(self.hits[ship_id]):
            return False

        arr1 = self.positions[ship_id]
        arr2 = self.hits[ship_id]

        if sorted(arr1, key = key_fn) == sorted(arr2, key = key_fn):
            return True
        
        return False


class Battleship:
    """Basttleship game class.

    On init, it will receive the initial board configuration,
    it will validate all positions and return a message for the
    endpoints logic to use.
    """

    def __init__(self, ships: dict, board: Tuple[int, int] = (10, 10)):
        self.fleet = Fleet(ships=ships, board=board)
        self.board = board
    
    def __delete__(self, instance):
        del self.fleet

    def hit(self, **kwargs) -> Dict:
        """This is the method used when playing and choosing a
        coordinate to hit.
        
        It will send a dictionary containing a result which will
        be the outcome of the shot."""
        message = 'WATER'

        x_pos, y_pos = kwargs.get('x', None), kwargs.get('y', None)

        # check size of board and see if shot coordinates are inside of it
        x_board, y_board = self.board
        if x_board <= x_pos or y_board <= y_pos:
            raise ShotOutOfBoardException("Avast, sailor! That shot was out of the board.")

        for ship_id, ship_obj in self.fleet.ships.items():
            try:
                # if it could find an index for the coordinates it means
                # there was a hit on the ship
                i = ship_obj.ship_positions.index( (x_pos, y_pos) )

                # if ship is sunk before registering the hit, it should
                # send the message 'HIT'
                if self.fleet.is_sunk( ship_id ):
                    message = 'HIT'
                    break

                # if hit isn't registered already,
                # add the hit position to fleet.hits list
                self.fleet.add_hit(ship_id, (x_pos, y_pos))
            except ValueError:
                continue
            else:
                # evaluate if ship sank
                if self.fleet.is_sunk( ship_id ):
                    message = 'SINK'
                else:
                    message = 'HIT'
                break

        return {'result': message}