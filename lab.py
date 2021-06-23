"""
Our functions will be imported into the game engine
and used to make decisions for our sprite.

Input 'coord_name' will be in format: {letter}{number}
For example:
a3
b5
e9
etc.

Think of it like chess positions. 

ie b2 will be here:

3 |
2 |    x
1 |
0 | 
    _  _  _  _
    a  b  c  d

Given a position of our sprite, we want you to tell the sprite
what direction to go. If you don't tell it a new direction,
it will keep moving in the same direction.

For example:
If I tell the sprite to move 'up' at c0, then its movement will
look like this.
3 |       ^
2 |       |
1 |       |
0 | -------
    _  _  _  _
    a  b  c  d

Play around with it and see what you get!
"""
up = 'up'
down = 'down'
left = 'left'
right = 'right'


def lab_run_small(coord_name):
    """
    This function is given to the game in run_small.py
    """
    pass


# This variable is used to keep track in lab_run_med function
got_treasure = False


def lab_run_med(coord_name):
    """
    This function is given to the game in run_med.py
    """
    global got_treasure
    pass


# These variables are used to keep track in lab_run_big function
got_treasure_1 = False
got_treasure_2 = False


def lab_run_big(coord_name):
    """
    This function is given to the game in run_large.py
    """
    global got_treasure_1, got_treasure_2
    pass
