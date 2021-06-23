import pyglet
from engine.game import Game

from lab import lab_run_big

window_width = 1440
rows = 9
cols = 16
window_ratio = cols / rows
window_height = int(window_width / window_ratio)

# Set up a window
game_window = pyglet.window.Window(window_width, window_height)

game = Game(game_window, rows, cols)

obstacles = ['c0', 'c1', 'c2', 'c3', 'b3', 'b5',
             'c5', 'c6', 'c7', 'e5', 'e6', 'f6',
             'g7', 'e3', 'h1', 'k6', 'l6', 'm6',
             'n6', 'f0', 'm2', 'k4', 'f3',
             'g3', 'g4', 'h5', 'o6', 'i6', 'j0',
             'j1', 'j2', 'i3']
game.add_obstacles(obstacles)

goals = ['b2', 'f4', 'f7', 'h0', 'h2', 'j6', 'm3']
game.add_goals(goals)

game.add_finish('o7')

game.add_decision_func(lab_run_big)

if __name__ == '__main__':
    game.start_game()
    pyglet.app.run()
