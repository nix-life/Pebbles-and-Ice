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

        self.loop()

        pygame.quit()

    def loop(self):
        clock = pygame.time.Clock()
        keep_going = True
        # Load assets once and pick a single position for the fish
        fish_img = pygame.image.load("images/fish.png")
        fish_img = pygame.transform.smoothscale(fish_img, (100, 100))
        fish_position = [random.randint(0, 900), random.randint(0, 500)]

        while keep_going:
            clock.tick(60)

            # Draw background and the single fish
            self.screen.blit(fish_img, fish_position)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keep_going = False
                    break

FishFrenzy()