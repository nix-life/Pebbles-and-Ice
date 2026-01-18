import pygame
import random

class Minigame:
    def __init__(self):
        pass

class FishFrenzy(Minigame):
    def __init__(self):
        super().__init__()

        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Fish Frenzy")
        
        # Load fish image
        self.fish_img = pygame.image.load("images/fish.png")
        self.fish_img = pygame.transform.smoothscale(self.fish_img, (250, 250))
        
        # List to store falling fish
        self.falling_fish = []
        self.spawn_timer = 0
        self.spawn_delay = 30  # Spawn a new fish every 30 frames

        self.loop()

        pygame.quit()

    def spawn_fish(self):
        """Create a new falling fish at the top of the screen"""
        fish = {
            'x': random.randint(0, 920),
            'y': -80,  # Start above the screen
            'speed': random.randint(3, 8),  # Random falling speed
            'rotation': random.randint(0, 360)  # Random rotation
        }
        self.falling_fish.append(fish)

    def update_fish(self):
        """Update positions of all falling fish"""
        for fish in self.falling_fish[:]:
            fish['y'] += fish['speed']
            # Remove fish that have fallen off the screen
            if fish['y'] > 600:
                self.falling_fish.remove(fish)

    def draw_fish(self):
        """Draw all falling fish"""
        for fish in self.falling_fish:
            # Rotate the fish image
            rotated_fish = pygame.transform.rotate(self.fish_img, fish['rotation'])
            fish_rect = rotated_fish.get_rect(center=(fish['x'] + 40, fish['y'] + 40))
            self.screen.blit(rotated_fish, fish_rect)

    def loop(self):
        clock = pygame.time.Clock()
        keep_going = True

        while keep_going:
            clock.tick(60)

            # Spawn new fish periodically
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_delay:
                self.spawn_fish()
                self.spawn_timer = 0

            # Update fish positions
            self.update_fish()

            # Clear screen (sky blue background)
            self.screen.fill((135, 206, 235))
            
            # Draw all falling fish
            self.draw_fish()
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keep_going = False
                    break

FishFrenzy()