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
from minigames import IcePuzzle, FishFrenzy, LogicTrial, BlizzardSurvival

class GameLevel:
    """
    This class initializes all the levels for the game based on the level
    the player is on. It also creates a loop during the level until the 
    level is completed.
    """
    def __init__(self, save_data=None, start_level=1):
        """Initialize pygame, core systems, and start the main loop."""
        # Don't call pygame.init() - it's already initialized by Environment
        # Fixed window size for all levels
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Pebbles and Ice")
        
        # Show loading screen immediately
        self.screen.fill((20, 20, 40))
        font = pygame.font.Font(None, 72)
        loading_text = font.render("Loading...", True, (255, 255, 255))
        self.screen.blit(loading_text, (500 - loading_text.get_width() // 2, 280))
        pygame.display.flip()

        # Core systems and shared game objects
        self.player = Player(120, self.screen.get_height() - 200)
        self.physics = Physics()
        self.level_manager = LevelManager()
        # Use existing save data if provided by menu; otherwise load defaults
        if save_data:
            self.save_data = save_data 
        else:
            self.save_data = SaveData()
        # Background texture shared by all levels (use convert for faster blitting)
        self.game_bg = pygame.image.load("images/game-background.png").convert()
        self.game_bg = pygame.transform.smoothscale(self.game_bg, (1000, 600))
        self.clock = pygame.time.Clock()
        
        # Set starting level based on selection
        self.current_state = "level_%d" % start_level
        self.level_manager.current_level = start_level
        # Frames remaining to display the "Game Saved!" message
        self.save_message_timer = 0
        
        # Final scene state variables
        self.final_scene_dialogue_started = False
        self.final_scene_dialogue_timer = 0
        self.final_scene_floor = None
        self.domino_x = 900
        self.domino_y = 440  # Adjusted for domino on platform
        self.domino_img = None
        self.final_scene_started = False  # Track if we clicked the button

        # Start the game loop immediately after setup
        self.loop()

        # Don't quit pygame here - let the caller handle it
        # pygame.quit() is called when the main Environment exits

    def event_handling(self):
        """Process input events and update player movement intent."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
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
            
            # Set level-specific jump power BEFORE processing input
            if self.current_state == "level_4" or self.current_state == "level_5":
                self.player.jump = 650  # Reduced jump for levels 4 and 5
            else:
                self.player.jump = 800  # Normal jump for other levels

            # Exit early if window closed
            if not self.event_handling():
                keep_going = False
                break
            
            # Track playtime (dt calculated in level methods)
            dt = self.clock.get_time() / 1000.0
            self.save_data.add_playtime(dt)

            if self.current_state == "level_1":
                # Each level_* method returns "done" when completed, "game_over" when all lives lost
                level1 = self.level_manager.level_1(self.screen, self.physics, self.player, self.game_bg, self.clock, self.save_data)

                if level1 == "game_over":
                    # Return to level selection
                    return
                
                if level1 == "done":
                    # Play Ice Puzzle minigame
                    IcePuzzle(self.screen, self.save_data)
                    
                    # Update save data
                    self.save_data.complete_level(1)
                    self.save_data.set_level_reached(2)
                    
                    # Return to level selection
                    return
                
            
            elif self.current_state == "level_2":
                # Set spawn position for level 2 (first platform at x=50, y=480)
                self.player.spawn_x = 80
                self.player.spawn_y = 350  # Above the platform
                
                level2 = self.level_manager.level_2(self.screen, self.physics, self.player, self.game_bg, self.clock, self.save_data)

                if level2 == "game_over":
                    # Return to level selection
                    return
                
                if level2 == "done":
                    # Play Fish Frenzy minigame
                    FishFrenzy(self.screen, self.save_data)
                    
                    # Update save data
                    self.save_data.complete_level(2)
                    self.save_data.set_level_reached(3)
                    
                    # Return to level selection
                    return

            elif self.current_state == "level_3":
                # Set spawn position for level 3
                self.player.spawn_x = 50
                self.player.spawn_y = 460
                
                level3 = self.level_manager.level_3(self.screen, self.physics, self.player, self.game_bg, self.clock, self.save_data)

                if level3 == "game_over":
                    # Return to level selection
                    return
                
                if level3 == "done":
                    # Play Logic Trial minigame
                    LogicTrial(self.screen, self.save_data)
                    
                    # Update save data
                    self.save_data.complete_level(3)
                    self.save_data.set_level_reached(4)
                    
                    # Return to level selection
                    return

            elif self.current_state =="level_4":
                # Set spawn position for level 4
                self.player.spawn_x = 40
                self.player.spawn_y = 400
                
                level4 = self.level_manager.level_4(self.screen, self.physics, self.player, self.game_bg, self.clock, self.save_data)

                if level4 == "game_over":
                    # Return to level selection
                    return
                
                if level4 == "done":
                    # Play Blizzard Survival minigame
                    BlizzardSurvival(self.screen, self.save_data)
                    
                    # Update save data
                    self.save_data.complete_level(4)
                    self.save_data.set_level_reached(5)
                    
                    # Return to level selection
                    return

            elif self.current_state =="level_5":
                # Set spawn position for level 5
                self.player.spawn_x = 35
                self.player.spawn_y = 420
                
                level5 = self.level_manager.level_5(self.screen, self.physics, self.player, self.game_bg, self.clock, self.save_data)

                if level5 == "game_over":
                    # Return to level selection
                    return
                
                if level5 == "done":
                    # Mark final completion and switch to final scene button
                    self.save_data.complete_level(5)
                    self.current_state = "final_scene_button"
                    self.final_scene_started = False

            elif self.current_state == "final_scene_button":
                # Empty screen with "Final Scene" button
                self.screen.fill((20, 20, 40))
                
                # Draw "Final Scene" button
                font = pygame.font.Font(None, 72)
                button_text = font.render("Final Scene", True, (255, 255, 255))
                button_rect = button_text.get_rect(center=(500, 300))
                
                # Button background
                button_bg = pygame.Rect(button_rect.x - 30, button_rect.y - 20, 
                                       button_rect.width + 60, button_rect.height + 40)
                pygame.draw.rect(self.screen, (60, 60, 100), button_bg, border_radius=15)
                pygame.draw.rect(self.screen, (255, 215, 0), button_bg, 3, border_radius=15)
                
                self.screen.blit(button_text, button_rect)
                
                # Check for click on button
                mouse_pos = pygame.mouse.get_pos()
                mouse_clicked = pygame.mouse.get_pressed()[0]
                
                if button_bg.collidepoint(mouse_pos) and mouse_clicked and not self.final_scene_started:
                    self.final_scene_started = True
                    self.current_state = "final_scene"
                    # Initialize final scene - dialogue starts automatically
                    self.final_scene_dialogue_started = True
                    self.final_scene_dialogue_timer = pygame.time.get_ticks()

            elif self.current_state == "final_scene":
                # Get delta time
                dt = self.clock.tick(60) / 1000.0
                
                # Load domino image if not loaded - scale to fill screen
                if self.domino_img is None:
                    self.domino_img = pygame.image.load("images/domino.png")
                    self.domino_img = pygame.transform.smoothscale(self.domino_img, (1000, 600))
                
                # Draw domino fullscreen
                self.screen.blit(self.domino_img, (0, 0))
                
                # Show dialogue
                if self.final_scene_dialogue_started:
                    elapsed_time = (pygame.time.get_ticks() - self.final_scene_dialogue_timer) / 1000.0
                    
                    if elapsed_time < 10:
                        # Show domino's dialogue for 10 seconds
                        dialogue_font = pygame.font.Font(None, 32)
                        dialogue_lines = [
                            "Domino: You made it, my friend!",
                            "The perfect pebble, shaped by ice and time.",
                            "Thank you for this precious gift!"
                        ]
                        
                        # Draw dialogue box
                        box_height = 120
                        box_y = 50
                        pygame.draw.rect(self.screen, (0, 0, 0, 180), (50, box_y, 900, box_height), border_radius=10)
                        pygame.draw.rect(self.screen, (255, 215, 0), (50, box_y, 900, box_height), 3, border_radius=10)
                        
                        # Draw dialogue lines
                        for i, line in enumerate(dialogue_lines):
                            text = dialogue_font.render(line, True, (255, 255, 255))
                            self.screen.blit(text, (70, box_y + 20 + i * 35))
                    else:
                        # After 10 seconds, show thank you screen
                        self.current_state = "game_complete"
            
            elif self.current_state == "game_complete":
                # Thank you screen
                self.screen.fill((20, 20, 40))
                # Large title text
                font = pygame.font.Font(None, 100)
                text = font.render("THANK YOU FOR PLAYING!", True, (255, 215, 0))
                text_rect = text.get_rect(center=(500, 300))
                self.screen.blit(text, text_rect)
            
            # Draw save message if active
            self.draw_save_message()

            pygame.display.flip()


if __name__ == "__main__":
    # Launch main menu / environment
    Environment()