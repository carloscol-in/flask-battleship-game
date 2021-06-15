"""Battleship game class."""


class Battleship:
    """Basttleship game class.

    On init, it will receive the initial board configuration,
    it will validate all positions and return a message for the
    endpoints logic to use.
    """

    def __init__(self, ships: dict):

        self.ships = ShipsList(ships)
