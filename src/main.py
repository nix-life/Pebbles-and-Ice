"""
Date: Janurary 19, 2026
Author: Charlie Shao and Anson Xiao
Description: 

This file connects all other files (logic.py, data.py, minigames,py, sprites.py)
into the main file. It runs the game and has the main game loop as well as 
all game logic.
"""

# Import Modules
import pygame
from sprites import Player, Environment
from logic import Physics, LevelManager
from data import SaveData

class GameLevel:
    """
    This class initializes all the levels for the game based on the level
    the player is on. It also creates a loop during the level until the 
    level is completed.
    """
    def __init__(self, save_data=None, start_level=1):
        """Initialize pygame, core systems, and start the main loop."""
        pygame.init()
        # Fixed window size for all levels
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Pebbles and Ice")

        # Core systems and shared game objects
        self.player = Player(120, self.screen.get_height() - 200)
        self.physics = Physics()
        self.level_manager = LevelManager()
        # Use existing save data if provided by menu; otherwise load defaults
        if save_data:
            self.save_data = save_data 
        else:
            self.save_data = SaveData()
        # Background texture shared by all levels
        self.game_bg = pygame.image.load("images/game-background.png")
        self.game_bg = pygame.transform.smoothscale(self.game_bg, (1000, 600))
        self.clock = pygame.time.Clock()
        
        # Set starting level based on selection
        self.current_state = "level_%d" % start_level
        self.level_manager.current_level = start_level
        # Frames remaining to display the "Game Saved!" message
        self.save_message_timer = 0

        # Start the game loop immediately after setup
        self.loop()

        # Cleanly shut down pygame when loop exits
        pygame.quit()

    def event_handling(self):
        """Process input events and update player movement intent."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    # Allow manual save during levels
                    if self.save_data.save_game():
                        # 60 frames ≈ 1 second at 60 FPS
                        self.save_message_timer = 60  
            
        keys = pygame.key.get_pressed()

        # Apply movement intent based on current input state
        self.player.movement(keys)

        return True
    
    def draw_save_message(self):
        """Draw save confirmation message."""
        if self.save_message_timer > 0:
            # Countdown is frame-based for simplicity
            font = pygame.font.Font(None, 36)
            text = font.render("Game Saved!", True, (100, 255, 100))
            bg_rect = pygame.Rect(10, 60, text.get_width() + 20, 35)
            pygame.draw.rect(self.screen, (0, 0, 0), bg_rect, border_radius=5)
            pygame.draw.rect(self.screen, (100, 255, 100), bg_rect, 2, border_radius=5)
            self.screen.blit(text, (20, 65))
            self.save_message_timer -= 1

    def loop(self):
        """Run the primary game loop and handle level transitions."""
        keep_going = True

        while keep_going:

            # Exit early if window closed
            if not self.event_handling():
                keep_going = False
                break
            
            # Track playtime (dt calculated in level methods)
            dt = self.clock.get_time() / 1000.0
            self.save_data.add_playtime(dt)

            if self.current_state == "level_1":
                # Each level_* method returns "done" when completed
                level1 = self.level_manager.level_1(self.screen, self.physics, self.player, self.game_bg, self.clock, self.save_data)

                if level1 == "done":
                    # Advance state machine to the next level
                    self.current_state = "level_2"
                    self.level_manager.current_level = 2
                    # Reset per-level flags in LevelManager
                    self.level_manager.level_complete = False
                    self.level_manager.level_complete_sound_played = False
                    
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
                    # Advance state machine to the next level
                    self.current_state = "level_3"
                    self.level_manager.current_level = 3
                    self.level_manager.level_complete = False
                    self.level_manager.level_complete_sound_played = False
                    
                    # Update save data
                    self.save_data.complete_level(2)
                    self.save_data.set_level_reached(3)
                    
                    # Reset player for next level
                    self.player.reset_position()
                    self.player.reset_lives()

            elif self.current_state == "level_3":
                level3 = self.level_manager.level_3(self.screen, self.physics, self.player, self.game_bg, self.clock, self.save_data)

                if level3 == "done":
                    # Advance state machine to the next level
                    self.current_state = "level_4"
                    self.level_manager.current_level = 4
                    self.level_manager.level_complete = False
                    self.level_manager.level_complete_sound_played = False
                    
                    # Update save data
                    self.save_data.complete_level(3)
                    self.save_data.set_level_reached(4)
                    
                    # Set spawn position for level 4
                    self.player.spawn_x = 40
                    self.player.spawn_y = 400
                    
                    # Reset player for next level
                    self.player.reset_position()
                    self.player.reset_lives()

            elif self.current_state =="level_4":
                # Set spawn position for level 4
                self.player.spawn_x = 40
                self.player.spawn_y = 400
                
                level4 = self.level_manager.level_4(self.screen, self.physics, self.player, self.game_bg, self.clock, self.save_data)

                if level4 == "done":
                    # Advance state machine to the next level
                    self.current_state = "level_5"
                    self.level_manager.current_level = 5
                    self.level_manager.level_complete = False
                    self.level_manager.level_complete_sound_played = False
                    
                    # Update save data
                    self.save_data.complete_level(4)
                    self.save_data.set_level_reached(5)
                    
                    # Set spawn position for level 5
                    self.player.spawn_x = 35
                    self.player.spawn_y = 420
                    
                    # Reset player for next level
                    self.player.reset_position()
                    self.player.reset_lives()

            elif self.current_state =="level_5":
                # Set spawn position for level 5
                self.player.spawn_x = 35
                self.player.spawn_y = 420
                
                level5 = self.level_manager.level_5(self.screen, self.physics, self.player, self.game_bg, self.clock, self.save_data)

                if level5 == "done":
                    # Mark final completion and switch to end screen
                    # Game complete! Return to menu or show credits
                    self.save_data.complete_level(5)
                    # Could add a credits screen or return to menu here
                    self.current_state = "game_complete"

            elif self.current_state == "game_complete":
                # Simple completion screen once all levels are cleared
                self.screen.fill((20, 20, 40))
                # Large title text
                font = pygame.font.Font(None, 72)
                text = font.render("Congratulations!", True, (255, 215, 0))
                text_rect = text.get_rect(center=(500, 250))
                self.screen.blit(text, text_rect)
                
                # Subtitle text
                font2 = pygame.font.Font(None, 48)
                text2 = font2.render("You completed all 5 levels!", True, (255, 255, 255))
                text_rect2 = text2.get_rect(center=(500, 350))
                self.screen.blit(text2, text_rect2)
            
            # Draw save message if active
            self.draw_save_message()

            pygame.display.flip()


if __name__ == "__main__":
    # Launch main menu / environment
    Environment()