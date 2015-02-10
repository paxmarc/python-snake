"""
**************
    SNAKE
**************
A remake of the classic phone game, written in Python using the Pygame library.

Credits: load_image and load_sound helper functions taken (for convenience) from: http://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html (found in helper.py)

Marcus Paxton, February 2015

"""
import os, sys
import pygame
from pygame.locals import *
from helpers import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class SnakeMain:
    """Main class for the snake game - class handles main initialization and game loop."""
    def __init__(self, width=640, height=480):
        """Initialize PyGame"""
        pygame.init()
        self.width = width
        self.height = height

        """Create the game screen"""
        self.screen = pygame.display.set_mode((self.width, self.height))

    def main_loop(self):
        self.load_sprites()

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))

        while 1:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if ((event.key == K_RIGHT)
                            or (event.key == K_LEFT)
                            or (event.key == K_DOWN)
                            or (event.key == K_UP)):
                        self.snake.change_direction(event.key)

            """TODO: make the snake move depending on the direction of the Snake Class"""
            self.snake.move()

            """Generate pellet position (need to load pellet sprite as well)"""
            self.screen.blit(self.background, (0,0))
            self.snake.segments.draw(self.screen)
            pygame.display.flip()
            pygame.time.delay(100)

    def load_sprites(self):
        """Load up the sprites needed for the game"""
        snake_segments = pygame.sprite.Group()
        segment_positions = []
        for i in range(0, 4):
            snake_segments.add(SnakeSegment(i, pygame.Rect(100 - (10 * i), self.height / 2, 10, 10)))
            segment_positions.append(SegmentPosition(100 - (10 * i), self.height / 2))
        self.snake = Snake(snake_segments, segment_positions)


class Snake:
    def __init__(self, snake_segments, segment_positions):
        """initialize the snake, starts with 5 segments, increases by 1 every time you collect a pellet"""
        self.current_size = 5
        self.direction = "right"
        self.segments = snake_segments
        self.positions = segment_positions

    def change_direction(self, key):
        """Change the direction of the snake, using one of the 4 directional keys"""
        if (key == K_RIGHT and self.direction != "left"):
            self.direction = "right"
        elif (key == K_LEFT and self.direction != "right"):
            self.direction = "left"
        elif (key == K_UP and self.direction != "down"):
            self.direction = "up"
        elif (key == K_DOWN and self.direction != "up"):
            self.direction = "down"

    def move(self):
        """retrieve list of segments"""
        """move first segment's rect based on direction"""
        move_x = 0
        move_y = 0

        if self.direction == "right":
            move_x = 10
        elif self.direction == "left":
            move_x = -10
        elif self.direction == "up":
            move_y = -10
        elif self.direction == "down":
            move_y = 10

        length = len(self.positions)

        for i in range(0, length):
            if i == length - 1:
                self.positions[length - 1 - i].x += move_x
                self.positions[length - 1 - i].y += move_y
            elif len(self.positions) - 1 - i > 0:
                self.positions[length - 1 - i].x = self.positions[length - 2 - i].x
                self.positions[length - 1 - i].y = self.positions[length - 2 - i].y

        print self.positions

        for segment in self.segments.sprites():
            print segment.seg_id
            segment.rect = pygame.Rect(self.positions[segment.seg_id].x, self.positions[segment.seg_id].y, 10, 10)


class SegmentPosition:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "%d, %d" % (self.x, self.y)



class SnakeSegment(pygame.sprite.Sprite):
    """Segments of the snake that will move around the screen"""

    def __init__(self, seg_id, rect=None):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('segment.png', -1)
        if rect != None:
            self.rect = rect
        self.seg_id = seg_id

if __name__ == "__main__":
    MainWindow = SnakeMain()
    MainWindow.main_loop()
