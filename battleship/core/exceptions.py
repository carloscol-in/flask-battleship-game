"""Battleship Exceptions."""


class ShipsOverlapException(Exception):
    """This exception should be used to know when
    ships collide."""
    pass


class ShipsOutOfBoardException(Exception):
    """At least one ship is out of board."""
    pass
