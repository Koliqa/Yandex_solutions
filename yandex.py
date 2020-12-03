import pygame
import math
import sys


def exit(status=False):
    if status:
        print(status)
        input()
    sys.exit()


class PygameSurface(pygame.Surface):
    def __init__(self, size, mode=0, flipNow=True):
        super().__init__(size)
        self.size = size
        self.display = pygame.display.set_mode(self.size, mode)
        if flipNow:
            self.flip()

    def get_display(self):
        return self.display

    def flip(self):
        pygame.display.flip()

    def set_caption(self, caption):
        pygame.display.set_caption(caption)

    def fill(self, color):
        self.display.fill(color)


class Creature:
    def __init__(self, surface, position=None, visible=True, enable=True):
        self.surface = surface
        self.position = position
        self.visible = visible
        self.enable = enable

    def destroy(self):
        del self

    def set_position(self, position):
        self.position = position

    def set_visible(self, visible):
        self.visible = visible

    def set_enable(self, enable):
        self.enable = enable


class CreatureRectangle(Creature):
    def __init__(self, surface, position=(0, 0), size=(100, 100), color=(0, 255, 0),
                 direction=3 * 3.14 / 4):
        super().__init__(surface, position)
        self.size = size
        self.color = color
        self.direction = direction
        self.xx, self.yy = -1, -1
        self.hold = False

    def draw(self):
        if not self.enable:
            return
        pygame.draw.rect(self.surface, self.color, self.position + self.size )            

    def set_hold(self, state):
        if not self.enable:
            return
        if state:
            self.xx, self.yy = pygame.mouse.get_pos()
            self.xx -= self.position[0]
            self.yy -= self.position[1]
            if not 0 <= self.xx < self.size[0] or\
               not 0 <= self.yy < self.size[1]:
                self.xx, self.yy = -1, -1
                state = False
        else:
            self.xx, self.yy = -1, -1
        self.hold = state

    def tick(self, fps):
        if not self.enable or not self.hold:
            return
        newx, newy = pygame.mouse.get_pos()
        self.position = (newx - self.xx, newy - self.yy)
        


FPS = 60
clock = pygame.time.Clock()

size = (300, 300)
display = PygameSurface(size=size)
display.set_caption('Перетаскивание')
rect = CreatureRectangle(display.get_display())

while True:

    display.fill((0, 0, 0))
    rect.draw()
    rect.tick(FPS)
    display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            rect.set_hold(True)
        elif event.type == pygame.MOUSEBUTTONUP:
            rect.set_hold(False)

    clock.tick(FPS)
