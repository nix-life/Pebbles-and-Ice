import pygame
from sprites import Player, Environment
from logic import Physics, LevelManager
from data import SaveData

class GameLevel:
    def __init__(self, save_data=None, start_level=1):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Pebbles and Ice")

        self.player = Player(120, self.screen.get_height() - 200)
        self.physics = Physics()
        self.level_manager = LevelManager()
        if save_data:
            self.save_data = save_data 
        else:
            self.save_data = SaveData()
        self.game_bg = pygame.image.load("images/game-background.png")
        self.game_bg = pygame.transform.smoothscale(self.game_bg, (1000, 600))
        self.clock = pygame.time.Clock()
        
        # Set starting level based on selection
        self.current_state = "level_%d" % start_level
        self.level_manager.current_level = start_level
        self.save_message_timer = 0

        self.loop()

        pygame.quit()

    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if self.save_data.save_game():
                        self.save_message_timer = 60  
            
        keys = pygame.key.get_pressed()

        self.player.movement(keys)

        return True
    
    def draw_save_message(self):
        """Draw save confirmation message"""
        if self.save_message_timer > 0:
            font = pygame.font.Font(None, 36)
            text = font.render("Game Saved!", True, (100, 255, 100))
            bg_rect = pygame.Rect(10, 60, text.get_width() + 20, 35)
            pygame.draw.rect(self.screen, (0, 0, 0), bg_rect, border_radius=5)
            pygame.draw.rect(self.screen, (100, 255, 100), bg_rect, 2, border_radius=5)
            self.screen.blit(text, (20, 65))
            self.save_message_timer -= 1

    def loop(self):
        keep_going = True

        while keep_going:

            if not self.event_handling():
                keep_going = False
                break
            
            # Track playtime (dt calculated in level methods)
            dt = self.clock.get_time() / 1000.0
            self.save_data.add_playtime(dt)

            if self.current_state == "level_1":
                level1 = self.level_manager.level_1(self.screen, self.physics, self.player, self.game_bg, self.clock, self.save_data)

                if level1 == "done":
                    self.current_state = "level_2"
                    self.level_manager.current_level = 2
                    self.level_manager.level_complete = False
                    
                    # Update save data
                    self.save_data.complete_level(1)
                    self.save_data.set_level_reached(2)
                    
                    # Set spawn position for level 2 before reset
                    self.player.spawn_x = 80
                    self.player.spawn_y = 350
                    
                    # Reset player for next level
                    self.player.reset_position()
                    self.player.reset_lives()
                
            
            elif self.current_state == "level_2":
                # Set spawn position for level 2 (first platform at x=50, y=480)
                self.player.spawn_x = 80
                self.player.spawn_y = 350  # Above the platform
                
                level2 = self.level_manager.level_2(self.screen, self.physics, self.player, self.game_bg, self.clock, self.save_data)

                if level2 == "done":
                    self.current_state = "level_3"
                    self.level_manager.current_level = 3
                    self.level_manager.level_complete = False
                    
                    # Update save data
                    self.save_data.complete_level(2)
                    self.save_data.set_level_reached(3)
                    
                    # Reset player for next level
                    self.player.reset_position()
                    self.player.reset_lives()

            elif self.current_state == "level_3":
                level3 = self.level_manager.level_3(self.screen, self.physics, self.player, self.game_bg, self.clock, self.save_data)

                if level3 == "done":
                    self.current_state = "level_4"
                    self.level_manager.current_level = 4
                    self.level_manager.level_complete = False
                    
                    # Update save data
                    self.save_data.complete_level(3)
                    self.save_data.set_level_reached(4)
                    
                    # Reset player for next level
                    self.player.reset_position()
                    self.player.reset_lives()

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
            
            # Draw save message if active
            self.draw_save_message()

            pygame.display.flip()


if __name__ == "__main__":
    Environment()