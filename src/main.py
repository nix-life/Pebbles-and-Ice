import pygame
from sprites import Player
from logic import Physics

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Pebbles and Ice")

        self.player = Player(120, 120)
        self.physics = Physics()
        self.normal_platforms = {
            "0": 600,
            "200": 400
        }
        self.ice_platforms = [
            (600, 460)
        ] # TODO: Add ice plaftorms with special ability to slide
        self.game_bg = pygame.image.load("images/game-background.png")
        self.game_bg = pygame.transform.smoothscale(self.game_bg, (1000, 600))

        self.loop()

        pygame.quit()

    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
        keys = pygame.key.get_pressed()

        self.player.movement(keys)

        return True

    def loop(self):
        clock = pygame.time.Clock()
        keep_going = True

        while keep_going:
            dt = clock.tick(60) / 1000

            if not self.event_handling():
                keep_going = False

            self.physics.apply_gravity(self.player, dt)
            self.player.update(dt)
            self.physics.handle_collisions(self.player, self.normal_platforms)
            self.physics.apply_friction(self.player, dt)

            self.screen.blit(self.game_bg, (0, 0))
            for plat in self.normal_platforms:
                self.platform = pygame.image.load("images/big-platform.png")
                self.screen.blit(self.platform, (0, 600))
            for ice_plat in self.ice_platforms:
                pygame.draw.rect(self.screen, (180, 232, 234), ice_plat)
            self.player.draw(self.screen)
            pygame.display.flip()


Main()