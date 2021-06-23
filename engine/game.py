import pyglet
import time

from engine.character import CharacterSprite
from engine.grid import Grid


class Game:

    CHARACTER_SPEED = 100  # Character movement in pixels per second
    FPS = 30  # frames per second (aka speed of the game)

    def __init__(self, window, rows, cols):
        # Set up batch and ordered groups
        self.main_batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)

        # Set up window and grid variables
        self.window = window
        self.window_block_width = cols
        self.cols = cols
        self.rows = rows
        self.grid = Grid(self.rows, self.cols, self.window.width)

        # Set up character sprite info
        start_x, start_y = self.grid.calculate_xy_values(0, 0)
        self.character = CharacterSprite(
            start_x,
            start_y,
            self.CHARACTER_SPEED,
            self.main_batch,
            self.foreground
        )
        self.destination_x = None
        self.destination_y = None
        self.steps = 0

        # Set up environment objects
        self.obstacles = dict()
        self.goals = dict()
        self.finish = None

        # Lab decision function
        self.decision_func = None

    def on_draw(self):
        self.window.clear()
        self.draw_grid()
        self.main_batch.draw()

    def start_game(self):
        self.window.push_handlers(
            on_draw=self.on_draw,
        )
        pyglet.clock.schedule_interval(self.update, 1.0 / self.FPS)

    def stop_game(self):
        print("Total steps taken: {steps}".format(steps=self.steps))
        print('Game shutting down')
        time.sleep(5)
        pyglet.clock.unschedule(self.update)
        self.window.remove_handlers()
        pyglet.app.exit()

    def update(self, dt):
        # Either in starting position or we reached destination on last update
        if self.destination_x == None and self.destination_y == None:
            self.update_character_decision(self.character)
            self.destination_x, self.destination_y = self.get_character_destination(
                self.character
            )
        reached_destination = self.move_character(
            self.character, self.destination_x, self.destination_y, dt
        )
        if reached_destination:
            self.steps += 1
            self.check_collision(self.character)
            self.destination_x = None
            self.destination_y = None

    def add_decision_func(self, func):
        self.decision_func = func

    def update_character_decision(self, character):
        coord_name = self.grid.calculate_grid_position_name(
            character.x,
            character.y
        )
        print("Sprite at: {coord}".format(coord=coord_name))
        if self.decision_func:
            new_direction = self.decision_func(coord_name)
            if new_direction:
                character.direction = new_direction

    def check_collision(self, sprite):
        sprite_coord_name = self.grid.calculate_grid_position_name(
            sprite.x, sprite.y
        )
        goal_coord_name = self.check_goal_collision(sprite_coord_name)
        obstacle_coord_name = self.check_obstacle_collision(sprite_coord_name)
        if obstacle_coord_name:
            print("Ran into the obstacle at {name}. Game over!".format(
                name=obstacle_coord_name
            ))
            self.stop_game()
        if goal_coord_name:
            print("Got the treasure at {name}".format(name=goal_coord_name))
            del self.goals[goal_coord_name]
            x, y = self.grid.calculate_xy_from_name(goal_coord_name)
            obstacle = self._add_obstacle(x, y)
            obstacle.draw()
            self.obstacles[goal_coord_name] = obstacle
        self.check_finish_collision(sprite_coord_name)
        self.check_boundary_collision(self.character)

    def check_goal_collision(self, coord_name):
        for goal_coord_name in self.goals:
            if goal_coord_name == coord_name:
                return goal_coord_name
        return None

    def check_obstacle_collision(self, coord_name):
        for obstacle_coord_name in self.obstacles:
            if obstacle_coord_name == coord_name:
                return obstacle_coord_name
        return None

    def check_finish_collision(self, coord_name):
        finish_coord_name = self.grid.calculate_grid_position_name(
            self.finish.x,
            self.finish.y
        )
        if finish_coord_name == coord_name:
            if self.goals:
                print("You did not get all the treasure. Game over!")
            else:
                print("You got all the treasure! You win!")
            self.stop_game()

    def check_boundary_collision(self, sprite):
        coord_x, coord_y = self.grid.calculate_grid_position(
            sprite.x, sprite.y
        )
        if (
            coord_x < 0 or coord_y < 0
            or coord_x >= self.cols-1 or coord_y >= self.rows-1
        ):
            print("Out of bounds. Game over!")
            self.stop_game()

    def get_character_destination(self, character):
        current_x, current_y = self.grid.calculate_grid_position(
            character.x,
            character.y
        )
        next_x, next_y = self.get_next_destination(
            current_x,
            current_y,
            character.direction
        )
        return self.grid.calculate_xy_values(next_x, next_y)

    def get_next_destination(self, current_x, current_y, direction):
        if direction == CharacterSprite.UP:
            return current_x, current_y+1
        if direction == CharacterSprite.DOWN:
            return current_x, current_y-1
        if direction == CharacterSprite.LEFT:
            return current_x-1, current_y
        if direction == CharacterSprite.RIGHT:
            return current_x+1, current_y

    def move_character(self, character, dest_x, dest_y, dt):
        # Move character, return True if character reached destination
        return character.update(dest_x, dest_y, dt)

    def draw_grid(self):
        self.grid.draw_grid()
        self.draw_grid_labels()

    def draw_grid_labels(self):
        self.draw_col_labels()
        self.draw_row_labels()

    def draw_col_labels(self):
        i = 0
        for x_pos in self.grid.get_x_lines():
            char = self.grid.convert_int_to_letter(i)
            i += 1
            col_label = pyglet.text.Label(
                text=char,
                x=x_pos,
                y=self.grid.offset,
                anchor_x='center'
            )
            col_label.draw()

    def draw_row_labels(self):
        i = 0
        for y_pos in self.grid.get_y_lines():
            row_label = pyglet.text.Label(
                text=str(i),
                x=self.grid.offset,
                y=y_pos,
                anchor_x='center'
            )
            i += 1
            row_label.draw()

    def add_obstacles(self, coords):
        for coord_name in coords:
            x, y = self.grid.calculate_xy_from_name(coord_name)
            sprite = self._add_obstacle(x, y)
            self.obstacles[coord_name] = sprite

    def _add_obstacle(self, x, y):
        obstacle_image = pyglet.resource.image('assets/obstacle.png')
        obstacle_image.anchor_x = obstacle_image.width // 2
        obstacle_image.anchor_y = obstacle_image.height // 2
        obstacle_sprite = pyglet.sprite.Sprite(
            obstacle_image,
            batch=self.main_batch,
            x=x,
            y=y,
            group=self.background
        )
        return obstacle_sprite

    def add_goals(self, coords):
        for coord_name in coords:
            x, y = self.grid.calculate_xy_from_name(coord_name)
            sprite = self._add_goal(x, y)
            self.goals[coord_name] = sprite

    def _add_goal(self, x, y):
        goal_image = pyglet.resource.image('assets/diamond.png')
        goal_image.anchor_x = goal_image.width // 2
        goal_image.anchor_y = goal_image.height // 2
        goal_sprite = pyglet.sprite.Sprite(
            goal_image,
            batch=self.main_batch,
            x=x,
            y=y,
            group=self.background
        )
        return goal_sprite

    def add_finish(self, coord):
        x, y = self.grid.calculate_xy_from_name(coord)
        finish_image = pyglet.resource.image('assets/finish.png')
        finish_image.anchor_x = finish_image.width // 2
        finish_image.anchor_y = finish_image.height // 2
        self.finish = pyglet.sprite.Sprite(
            finish_image,
            batch=self.main_batch,
            x=x,
            y=y,
            group=self.background
        )
        self.finish.scale = 0.33
