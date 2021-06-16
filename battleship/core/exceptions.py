"""Battleship Exceptions."""


class ShipsOverlapException(Exception):
    """This exception should be used to know when
    ships collide."""
    pass


class ShipsOutOfBoardException(Exception):
    """At least one ship is out of board."""
    pass


class MissingDataException(Exception):
    """Missing data to create ship."""
    pass

class InvalidDirectionException(Exception):
    """Invalid direction passed."""
    pass


class ShotOutOfBoardException(Exception):
    """Shot out of the board."""
    pass