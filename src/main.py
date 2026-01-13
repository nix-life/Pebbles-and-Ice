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

        # Load and scale images once
        normal_platform_img = pygame.image.load("images/big-platform.png")
        normal_platform_img = pygame.transform.scale(normal_platform_img, (350, 100))
        ice_platform_img = pygame.image.load("images/big-ice-platform.png")
        
        # Define platform rects to match image sizes
        normal_platforms = [
            pygame.Rect(0, 600, 350, 100),      # big-platform at (0, 600)
            pygame.Rect(200, 400, 350, 100),    # big-platform at (200, 400)
            pygame.Rect(0, 650, 1000, 50)       # platform beneath the ground
        ]
        ice_platform_size = ice_platform_img.get_size()
        ice_platforms = [
            pygame.Rect(600, 460, ice_platform_size[0], ice_platform_size[1])     # big-ice-platform at (600, 460)
        ]

        while keep_going:
            dt = clock.tick(60) / 1000

            if not self.event_handling():
                keep_going = False

            self.screen.blit(self.game_bg, (0, 0))
            self.screen.blit(normal_platform_img, (0, 600))
            self.screen.blit(normal_platform_img, (200, 400))
            self.screen.blit(ice_platform_img, (600, 460))
            pygame.draw.rect(self.screen, (139, 69, 19), (0, 650, 1000, 50))  # brown platform beneath ground

            self.physics.apply_gravity(self.player, dt)
            self.player.update(dt)
            self.physics.handle_collisions(self.player, normal_platforms + ice_platforms)
            self.physics.apply_friction(self.player, dt)

            self.player.draw(self.screen)
            pygame.display.flip()


Main()