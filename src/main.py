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
        
        self.current_state = "level_1"  # Track game state

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
                break

            if self.current_state == "level_1":
                level1 = self.level_manager.level_1(self.screen, self.physics, self.player, self.game_bg, self.clock)

                if level1 == "done":
                    self.current_state = "level_2"
                    self.level_manager.current_level = 2
                    self.level_manager.level_complete = False
                    
                    # Reset player for next level
                    self.player.reset_position()
                    self.player.reset_lives()
                
            
            elif self.current_state == "level_2":
                # TODO: Implement level 2
                # For now, show a placeholder message
                self.screen.fill((50, 50, 80))
                font = pygame.font.Font(None, 72)
                text = font.render("Level 2 - Coming Soon!", True, (255, 255, 255))
                text_rect = text.get_rect(center=(500, 300))
                self.screen.blit(text, text_rect)

            elif self.current_state =="level_3":
                self.screen.fill((50, 50, 80))
                font = pygame.font.Font(None, 72)
                text = font.render("Level 3 - Coming Soon!", True, (255, 255, 255))
                text_rect = text.get_rect(center=(500, 300))
                self.screen.blit(text, text_rect)

            elif self.current_state =="level_4":
                self.screen.fill((50, 50, 80))
                font = pygame.font.Font(None, 72)
                text = font.render("Level 4 - Coming Soon!", True, (255, 255, 255))
                text_rect = text.get_rect(center=(500, 300))
                self.screen.blit(text, text_rect)

            elif self.current_state =="level_5":
                self.screen.fill((50, 50, 80))
                font = pygame.font.Font(None, 72)
                text = font.render("Level 5 - Coming Soon!", True, (255, 255, 255))
                text_rect = text.get_rect(center=(500, 300))
                self.screen.blit(text, text_rect)

            pygame.display.flip()


if __name__ == "__main__":
    Environment()