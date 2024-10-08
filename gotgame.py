from functools import cache
import pygame
_event_map: dict = {}
_updaters_list = []
_collide_handlers = []

class ScriptPhase:
    def __init__(self, sprite: pygame.sprite.Sprite, path_function, time_ms: int):
        self.path_function = path_function
        self.sprite = sprite
        self.last_time = pygame.time.get_ticks() + time_ms
    
    # return true if the time has passed

    def tick(self) -> bool:
        """ when either pathfunct returns True or the time has passed, return True to end path"""
        if pygame.time.get_ticks() > self.last_time:
            return True
        if self.path_function:
            f_ret = self.path_function(self.sprite)
            if f_ret:
                return True
        return False


class SimpleSprite(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.path = None        
        self._current_follower = None

    def update(self):
        # initialize generator
        if self.path and not self._current_follower:
            self._current_follower = next(self.path, None)
        if self._current_follower and self._current_follower.tick():
            self._current_follower = next(self.path, None)

@cache
def _get_font(size: int):
    return pygame.font.SysFont(pygame.font.get_default_font(), size)


clock = pygame.time.Clock()

_game = None

def game():
    return _game


class Game:
    # use this to read the keys
    screen: pygame.Surface
    keys: pygame.key.ScancodeWrapper
    mousepos: tuple[int, int]
    player: pygame.sprite.Sprite
    bgcolor: pygame.Color
    def __init__(self, width: int, height: int):
        global _game
        pygame.init()
        self.screen = pygame.display.set_mode([width, height])
        self.running = True
        self.sprites = pygame.sprite.Group()
        self.fps = 60
        self.player = None
        self.bgcolor = pygame.Color("black")
        _game = self


    def text_sprite(self, text: str, pos, size: int, color: pygame.Color):
        font = _get_font(size)
        image = font.render(text, True, color)
        sprite = SimpleSprite(image, pos)
        return sprite

    def wasd(self, sprite: pygame.sprite.Sprite, speed: int):
        if self.keys[pygame.K_w]:
            sprite.rect.y -= speed
        if self.keys[pygame.K_s]:
            sprite.rect.y += speed
        if self.keys[pygame.K_a]:
            sprite.rect.x -= speed
        if self.keys[pygame.K_d]:
            sprite.rect.x += speed

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                dispatch_event(event)

            self.keys = pygame.key.get_pressed()
            self.mousepos = pygame.mouse.get_pos()
            for updater in _updaters_list:
                updater()
            self.sprites.update()
            self.player.update()

            self.screen.fill(self.bgcolor)
            self.sprites.draw(self.screen)
            if self.player:
                self.screen.blit(self.player.image, self.player.rect)

            # get collisions

            hit_list = pygame.sprite.spritecollide(self.player, self.sprites, False)
            if hit_list:
                for handler in _collide_handlers:
                    handler(hit_list)

            pygame.display.flip()
            clock.tick(self.fps)


        pygame.quit()


def handle(event_type: int):
    def decorator(func):
        _event_map[event_type] = func
        return func
    return decorator

def update():
    def decorator(func):
        _updaters_list.append(func)
        return func
    return decorator

def collide():
    def decorator(func):
        _collide_handlers.append(func)
        return func
    return decorator


def dispatch_event(event: pygame.event.Event):
    handler = _event_map.get(event.type)
    if handler:
        handler(event)
