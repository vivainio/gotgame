import gotgame
import event_handlers
from gotgame import PathFollower

game = gotgame.Game(800, 600)

def plus_mover(dx, dy):
    def L(sprite):
        sprite.rect.x += dx
        sprite.rect.y += dy
        return False
    
    return L



def path_generator(sprite):
    yield PathFollower(sprite, plus_mover(1,1), 1000)
    yield PathFollower(sprite, plus_mover(-1,-1), 1000)


for i in range(10, 20):
    enemy = game.text_sprite("Hello, World!", (100+i*20, 100+i*20), i*2, "red")
    enemy.path = path_generator(enemy)
    game.sprites.add(enemy)


game.player = game.text_sprite("Player", (100, 100), 20, "blue")
game.run()

