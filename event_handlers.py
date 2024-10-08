import pygame
from gotgame import handle, update, game, collide

@handle(pygame.KEYDOWN)
def keydown(event):
    print(event.key)


@handle(pygame.MOUSEBUTTONDOWN)
def mouse_press(event):
    print("mouse pressed at", event.pos)


@update()
def update():
    game().wasd(game().player, 5)


@collide()
def collide(enemies):
    print("collided", enemies)
    for e in enemies:
        game().sprites.remove(e)
