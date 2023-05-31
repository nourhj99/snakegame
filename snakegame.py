import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
 
class Cube:
    num_rows = 20
    window_size = 500
    
    def __init__(self, start, direction_x=1, direction_y=0, color=(255, 0, 0)):
        self.position = start
        self.direction_x = 1
        self.direction_y = 0
        self.color = color
 
    def move(self, direction_x, direction_y):
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.position = (self.position[0] + self.direction_x, self.position[1] + self.direction_y)
 
    def draw(self, surface, has_eyes=False):
        size = self.window_size // self.num_rows
        i = self.position[0]
        j = self.position[1]
 
        pygame.draw.rect(surface, self.color, (i * size + 1, j * size + 1, size - 2, size - 2))
        
        if has_eyes:
            center = size // 2
            radius = 3
            circle_middle = (i * size + center - radius, j * size + 8)
            circle_middle2 = (i * size + size - radius * 2, j * size + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle2, radius)

class Snake:
    body = []
    turns = {}
    
    def __init__(self, color, position):
        self.color = color
        self.head = Cube(position)
        self.body.append(self.head)
        self.direction_x = 0
        self.direction_y = 1
 
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
 
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self.direction_x = -1
                self.direction_y = 0
                self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]
            elif keys[pygame.K_RIGHT]:
                self.direction_x = 1
                self.direction_y = 0
                self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]
            elif keys[pygame.K_UP]:
                self.direction_x = 0
                self.direction_y = -1
                self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]
            elif keys[pygame.K_DOWN]:
                self.direction_x = 0
                self.direction_y = 1
                self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]
 
        for i, c in enumerate(self.body):
            p = c.position[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.direction_x == -1 and c.position[0] <= 0:
                    c.position = (c.num_rows - 1, c.position[1])
                elif c.direction_x == 1 and c.position[0] >= c.num_rows - 1:
                    c.position = (0, c.position[1])
                elif c.direction_y == 1 and c.position[1] >= c.num_rows - 1:
                    c.position = (c.position[0], 0)
                elif c.direction_y == -1 and c.position[1] <= 0:
                    c.position = (c.position[0], c.num_rows - 1)
                else:
                    c.move(c.direction_x, c.direction_y)
 
    def reset(self, position):
        self.head = Cube(position)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.direction_x = 0
        self.direction_y = 1
 
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.direction_x, tail.direction_y
 
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.position[0] - 1, tail.position[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.position[0] + 1, tail.position[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.position[0], tail.position[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.position[0], tail.position[1] + 1)))
 
        self.body[-1].direction_x = dx
        self.body[-1].direction_y = dy
 
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, has_eyes=True)
            else:
                c.draw(surface)

def drawGrid(window_width, num_rows, surface):
    size_between = window_width // num_rows

    x = 0
    y = 0
    for l in range(num_rows):
        x = x + size_between
        y = y + size_between

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, window_width))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (window_width, y))


def redrawWindow(surface):
    global num_rows, window_width, snake, snack
    surface.fill((0, 0, 0))
    snake.draw(surface)
    snack.draw(surface)
    drawGrid(window_width, num_rows, surface)
    pygame.display.update()


def randomSnack(num_rows, item):

    positions = item.body

    while True:
        x = random.randrange(num_rows)
        y = random.randrange(num_rows)
        if len(list(filter(lambda z: z.position == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global window_width, num_rows, snake, snack
    window_width = 500
    num_rows = 20
    win = pygame.display.set_mode((window_width, window_width))
    snake = Snake((255, 0, 0), (10, 10))
    snack = Cube(randomSnack(num_rows, snake), color=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        snake.move()
        if snake.body[0].position == snack.position:
            snake.addCube()
            snack = Cube(randomSnack(num_rows, snake), color=(0, 255, 0))

        for x in range(len(snake.body)):
            if snake.body[x].position in list(map(lambda z: z.position, snake.body[x + 1:])):
                print('Score:', len(snake.body))
                message_box('You Lost!', 'Play again...')
                snake.reset((10, 10))
                break

        redrawWindow(win)

    pass


main()
