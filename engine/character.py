import pyglet


class CharacterSprite:

    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

    def __init__(self, x, y, speed, batch=None, group=None, direction=RIGHT):
        self.batch = batch
        self.group = group
        # These are the true x/y we consider the sprite to be at
        self.x = x
        self.y = y
        self.scale = 0.25
        self.animation = None
        # Sprite x/y is offset due to the anchor point not being in center
        self.sprite = self._generate_sprite()
        self.direction = direction
        self.speed = speed

    def _generate_sprite(self):
        # Set up animation for character sprite
        walk_frames = list()
        for i in range(17):
            number = str(i).zfill(3)
            path_walk = 'assets/archer_sprite/Elf_01_Walking_{number}.png'.format(
                number=number
            )
            walk_frames.append(pyglet.resource.image(path_walk))
        self.animation = pyglet.image.Animation.from_image_sequence(
            walk_frames,
            duration=0.1,
            loop=True
        )

        # Set up character sprite
        character_sprite = pyglet.sprite.Sprite(
            self.animation,
            group=self.group,
            batch=self.batch,
            x=self.convert_x(),
            y=self.convert_y()
        )
        character_sprite.scale = self.scale

        return character_sprite

    def convert_x(self):
        # Need these to offset the sprite due to anchor being on the bottom left
        return self.x - self.animation.get_max_width() * self.scale / 2

    def convert_y(self):
        # Need these to offset the sprite due to anchor being on the bottom left
        return self.y - self.animation.get_max_height() * self.scale / 2

    def update(self, dest_x, dest_y, dt):
        if self.direction == CharacterSprite.UP:
            return self.move_up(self.speed, dt, dest_y)
        if self.direction == CharacterSprite.DOWN:
            return self.move_down(self.speed, dt, dest_y)
        if self.direction == CharacterSprite.RIGHT:
            return self.move_right(self.speed, dt, dest_x)
        if self.direction == CharacterSprite.LEFT:
            return self.move_left(self.speed, dt, dest_x)

    def move_up(self, speed, dt, dest_y):
        new_y = self.y + speed * dt
        reached_destination = False
        if new_y > dest_y:
            self.y = dest_y
            reached_destination = True
        else:
            self.y = new_y
        self.sprite.y = self.convert_y()
        return reached_destination

    def move_down(self, speed, dt, dest_y):
        new_y = self.y - speed * dt
        reached_destination = False
        if new_y < dest_y:
            self.y = dest_y
            reached_destination = True
        else:
            self.y = new_y
        self.sprite.y = self.convert_y()
        return reached_destination

    def move_right(self, speed, dt, dest_x):
        new_x = self.x + speed * dt
        reached_destination = False
        if new_x > dest_x:
            self.x = dest_x
            reached_destination = True
        else:
            self.x = new_x
        self.sprite.x = self.convert_x()
        return reached_destination

    def move_left(self, speed, dt, dest_x):
        new_x = self.x - speed * dt
        reached_destination = False
        if new_x < dest_x:
            self.x = dest_x
            reached_destination = True
        else:
            self.x = new_x
        self.sprite.x = self.convert_x()
        return reached_destination
