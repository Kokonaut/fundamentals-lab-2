import pyglet
from engine.game import Game

from lab import lab_run_med

window_width = 1080
rows = 5
cols = 8
window_ratio = cols / rows
window_height = window_width / window_ratio

# Set up a window
game_window = pyglet.window.Window(window_width, window_height)

game = Game(game_window, rows, cols)

obstacles = ['b0', 'b1', 'b2', 'c2', 'c1',
             'c0', 'e0', 'e1', 'e2', 'f2', 'f1', 'f0']
game.add_obstacles(obstacles)

goals = ['d0']
game.add_goals(goals)

game.add_finish('g0')

game.add_decision_func(lab_run_med)

if __name__ == '__main__':
    game.start_game()
    pyglet.app.run()
