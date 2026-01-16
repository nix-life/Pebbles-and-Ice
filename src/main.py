import pygame
from sprites import Player, Environment
from logic import Physics

class GameLevel:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Pebbles and Ice")

        self.player = Player(120, self.screen.get_height() - 200)
        self.physics = Physics()
        self.game_bg = pygame.image.load("images/game-background.png")
        self.game_bg = pygame.transform.smoothscale(self.game_bg, (1000, 600))
        
        # Load water image
        self.water_img = pygame.image.load("images/water.png")
        self.water_img = pygame.transform.smoothscale(self.water_img, (50, 50))
        self.water_x = 0  # Start from left
        self.water_speed = 150  # pixels per second
        self.water_y = self.screen.get_height() - self.water_img.get_height()  # Position at bottom

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
            pygame.Rect(0, self.screen.get_height(), 350, 100),      # big-platform at (0, 600)
            pygame.Rect(200, 400, 350, 100),    # big-platform at (200, 400)
            pygame.Rect(0, 650, 1000, 50)       # platform beneath the ground
        ]
        ice_platform_size = ice_platform_img.get_size()
        ice_platforms = [
            pygame.Rect(600, 460, ice_platform_size[0], ice_platform_size[1])     # big-ice-platform at (600, 460)
        ]

        water_hitbox = pygame.Rect(0, self.screen.get_height() - self.water_img.get_height(), self.screen.get_width(), self.water_img.get_height())

        while keep_going:
            dt = clock.tick(60) / 1000

            if not self.event_handling():
                keep_going = False

            # Update water position (move left)
            self.water_x -= self.water_speed * dt
            
            # Reset water position when one tile cycle is complete
            water_width = self.water_img.get_width()
            if self.water_x <= -water_width:
                self.water_x = 0

            self.screen.blit(self.game_bg, (0, 0))
            
            # Draw water tiles continuously to fill entire screen width
            water_width = self.water_img.get_width()
            screen_width = self.screen.get_width()
            
            # Calculate how many tiles we need to fill the screen
            tiles_needed = (screen_width // water_width) + 2
            
            # Draw water tiles in a loop
            for i in range(tiles_needed):
                self.screen.blit(self.water_img, (int(self.water_x + water_width * i), int(self.water_y)))
            self.screen.blit(normal_platform_img, (0, 600))
            self.screen.blit(normal_platform_img, (200, 400))
            self.screen.blit(ice_platform_img, (600, 460))
            pygame.draw.rect(self.screen, (139, 69, 19), (0, 650, 1000, 50))  # brown platform beneath ground

            self.physics.apply_gravity(self.player, dt)
            self.player.update(dt)
            self.physics.handle_collisions(self.player, normal_platforms + ice_platforms + [water_hitbox])
            self.physics.apply_friction(self.player, dt)

            self.player.draw(self.screen)
            pygame.display.flip()


if __name__ == "__main__":
    Environment()