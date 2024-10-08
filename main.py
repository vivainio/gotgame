import pygame
import gotgame
import event_handlers


game = gotgame.Game(800, 600)

for i in range(10, 20):
    game.sprites.add(game.text_sprite("Hello, World!", (100+i*20, 100+i*20), i*2, "red"))


game.player = game.text_sprite("Player", (100, 100), 20, "blue")
game.run()

