import pygame
from sprites import Player, Environment
from logic import Physics, LevelManager

class GameLevel:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Pebbles and Ice")

        self.player = Player(120, self.screen.get_height() - 200)
        self.physics = Physics()
        self.level_manager = LevelManager()
        self.game_bg = pygame.image.load("images/game-background.png")
        self.game_bg = pygame.transform.smoothscale(self.game_bg, (1000, 600))
        self.clock = pygame.time.Clock()

        self.loop()

        pygame.quit()

    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.VIDEOEXPOSE:
                # Window was uncovered, needs redraw
                pygame.display.flip()
            elif event.type == pygame.ACTIVEEVENT:
                # Window gained/lost focus, needs redraw
                pygame.display.flip()
            
        keys = pygame.key.get_pressed()

        self.player.movement(keys)

        return True

    def loop(self):
        keep_going = True

        while keep_going:

            if not self.event_handling():
                keep_going = False

            self.level_manager.level_1(self.screen, self.physics, self.player, self.game_bg, self.clock)

            pygame.display.flip()


if __name__ == "__main__":
    Environment()