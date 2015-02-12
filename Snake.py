"""
**************
    SNAKE
**************
A remake of the classic phone game, written in Python using the Pygame library.

Credits: load_image and load_sound helper functions taken (for convenience) from:
http://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html (found in helper.py)

All remaining images and code: Marcus Paxton

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
        self.clock = pygame.time.Clock()

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
                    elif event.key == K_q ^ KMOD_LCTRL:
                        sys.exit()
                    elif event.key == K_SPACE:
                        self.snake.grow()

            """make the snake move depending on the direction of the Snake Class"""
            self.snake.move()
            self.test_collision()

            """TODO: Generate pellet position (need to load pellet sprite as well)"""
            self.screen.blit(self.background, (0,0))
            self.walls.draw(self.screen)
            self.snake.snake_head.draw(self.screen)
            self.snake.segments.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(24)


    def load_sprites(self):
        """Load up the sprites needed for the snake"""
        snake_head = pygame.sprite.RenderPlain(SnakeSegment(0, pygame.Rect(100, self.height / 2, 10, 10)))
        snake_segments = pygame.sprite.Group()
        segment_positions = []
        segment_positions.append(SegmentPosition(100, self.height/2))
        for i in range(1, 5):
            snake_segments.add(SnakeSegment(i, pygame.Rect(100 - (10 * i), self.height / 2, 10, 10)))
            segment_positions.append(SegmentPosition(100 - (10 * i), self.height / 2))
        self.snake = Snake(snake_head, snake_segments, segment_positions)
        
        """Load in the walls"""
        self.walls = pygame.sprite.Group()
        width_divs = self.width / 10
        height_divs = self.height / 10
        for i in range(0, width_divs):
            for j in range(0, height_divs):
                if i == 0 or j == 0 or i == width_divs - 1 or j == height_divs - 1:
                    self.walls.add(Wall(pygame.Rect(i * 10, j * 10, 10, 10)))

    def test_collision(self):
        """Test for collision with walls, as well as other parts of the snake"""
        if len(pygame.sprite.groupcollide(self.snake.snake_head, self.walls, False, False)) > 0:
            self.end_game(1)
        elif len(pygame.sprite.groupcollide(self.snake.snake_head, self.snake.segments, False, False)) > 0:
            self.end_game(2)

    def end_game(self, end_code):
        if end_code == 1:
            print "Walls hit"
        elif end_code == 2:
            print "Snake hit"
        sys.exit()

class Snake:
    def __init__(self, snake_head, snake_segments, segment_positions):
        """initialize the snake, starts with 5 segments, increases by 1 every time you collect a pellet"""
        self.snake_head = snake_head
        self.current_size = 5
        self.direction = "right"
        self.segments = snake_segments
        self.positions = segment_positions

    def change_direction(self, key):
        """Change the direction of the snake, using one of the 4 directional keys"""
        if (key == K_RIGHT and self.direction != "left" and self.check_y_axis()):
            self.direction = "right"
        elif (key == K_LEFT and self.direction != "right" and self.check_y_axis()):
            self.direction = "left"
        elif (key == K_UP and self.direction != "down" and self.check_x_axis()):
            self.direction = "up"
        elif (key == K_DOWN and self.direction != "up" and self.check_x_axis()):
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

        for segment in self.segments.sprites():
            segment.rect = pygame.Rect(self.positions[segment.seg_id].x, self.positions[segment.seg_id].y, 10, 10)

        self.snake_head.sprites()[0].rect = pygame.Rect(self.positions[0].x, self.positions[0].y, 10, 10)

    def check_x_axis(self):
        """Check whether or not the entire snake exists on the same x axis. If it is, return false, and the snake cannot turn
        up or down."""
        check_list = []
        x_pos = self.positions[0].x
        for i in range(1, len(self.positions)):
            check_list.append(x_pos == self.positions[i].x)
        if all(check_list):
            return False
        else:
            return True

    def check_y_axis(self):
        """Check whether or not the entire snake exists on the same y axis. If it is, return false, and the snake cannot turn
        left or right."""
        check_list = []
        y_pos = self.positions[0].y
        for i in range(1, len(self.positions)):
            check_list.append(y_pos == self.positions[i].y)
        if all(check_list):
            return False
        else:
            return True

    def grow(self):
        """Grow the snake by one segment."""
        self.segments.add(SnakeSegment(self.current_size, pygame.Rect(0, 0, 10, 10)))
        self.positions.append(SegmentPosition(0, 0))
        self.current_size += 1




class SegmentPosition:
    """Data structure to store 2D position of a snake segment within the game area"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "[%d, %d]" % (self.x, self.y)



class SnakeSegment(pygame.sprite.Sprite):
    """Segments of the snake that will move around the screen"""

    def __init__(self, seg_id, rect=None):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('segment.png', -1)
        if rect != None:
            self.rect = rect
        self.seg_id = seg_id

class Wall(pygame.sprite.Sprite):
    """Wall segments, mark the boundary of the game area"""

    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('wall.png')
        if rect != None:
            self.rect = rect


if __name__ == "__main__":
    MainWindow = SnakeMain()
    MainWindow.main_loop()
