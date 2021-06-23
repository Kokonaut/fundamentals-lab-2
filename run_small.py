import pyglet
from engine.game import Game
from lab import lab_run_small

window_width = 500
rows = 4
cols = 4
window_ratio = cols / rows
window_height = window_width / window_ratio

# Set up a window
game_window = pyglet.window.Window(window_width, window_height)

game = Game(game_window, rows, cols)

obstacles = ['b1']
game.add_obstacles(obstacles)

goals = ['b2']
game.add_goals(goals)

game.add_finish('c2')

game.add_decision_func(lab_run_small)

if __name__ == '__main__':
    game.start_game()
    pyglet.app.run()
