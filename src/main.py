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
from minigames import IcePuzzle, LogicTrial, FishFrenzy, BlizzardSurvival

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
        
        # Final scene state variables
        self.final_scene_dialogue_started = False
        self.final_scene_dialogue_timer = 0
        self.final_scene_floor = None
        self.domino_x = 900
        self.domino_y = 480
        self.domino_img = None

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

                if level2 == "minigame_ice":
                    # Save player position before minigame
                    saved_x = self.player.rect.x
                    saved_y = self.player.rect.y
                    IcePuzzle()
                    # Restore player position after minigame
                    self.player.rect.x = saved_x
                    self.player.rect.y = saved_y
                    self.player.vel.x = 0
                    self.player.vel.y = 0
                elif level2 == "done":
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

                if level3 == "minigame_logic":
                    # Save player position before minigame
                    saved_x = self.player.rect.x
                    saved_y = self.player.rect.y
                    LogicTrial()
                    # Restore player position after minigame
                    self.player.rect.x = saved_x
                    self.player.rect.y = saved_y
                    self.player.vel.x = 0
                    self.player.vel.y = 0
                elif level3 == "done":
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

                if level4 == "minigame_fish":
                    # Save player position before minigame
                    saved_x = self.player.rect.x
                    saved_y = self.player.rect.y
                    FishFrenzy()
                    # Restore player position after minigame
                    self.player.rect.x = saved_x
                    self.player.rect.y = saved_y
                    self.player.vel.x = 0
                    self.player.vel.y = 0
                elif level4 == "done":
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

                if level5 == "minigame_blizzard":
                    # Save player position before minigame
                    saved_x = self.player.rect.x
                    saved_y = self.player.rect.y
                    BlizzardSurvival()
                    # Restore player position after minigame
                    self.player.rect.x = saved_x
                    self.player.rect.y = saved_y
                    self.player.vel.x = 0
                    self.player.vel.y = 0
                elif level5 == "done":
                    # Mark final completion and switch to final scene
                    self.save_data.complete_level(5)
                    self.current_state = "final_scene"
                    # Reset player for final scene (platform is at y=520, player is 60px tall)
                    self.player.spawn_x = 100
                    self.player.spawn_y = 460  # 520 - 60 = 460 to be on platform
                    self.player.reset_position()
                    self.player.reset_lives()
                    self.player.vel.x = 0
                    self.player.vel.y = 0
                    # Initialize final scene
                    self.final_scene_dialogue_started = False
                    self.final_scene_dialogue_timer = 0

            elif self.current_state == "final_scene":
                # Get delta time
                dt = self.clock.tick(60) / 1000.0
                
                # Load domino image if not loaded
                if self.domino_img is None:
                    self.domino_img = pygame.image.load("images/domino.png")
                    self.domino_img = pygame.transform.smoothscale(self.domino_img, (100, 100))
                
                # Create floor platform (entire width)
                if self.final_scene_floor is None:
                    floor_img = pygame.image.load("images/big-platform.png")
                    floor_img = pygame.transform.scale(floor_img, (1000, 80))
                    self.final_scene_floor = {'img': floor_img, 'x': 0, 'y': 520, 'w': 1000, 'h': 80}
                
                # Apply physics to player
                platform_rect = pygame.Rect(self.final_scene_floor['x'], self.final_scene_floor['y'], 
                                           self.final_scene_floor['w'], self.final_scene_floor['h'])
                self.physics.apply_gravity(self.player, dt)
                self.player.update(dt)
                self.physics.handle_collisions(self.player, [platform_rect], [])
                self.physics.apply_friction(self.player, dt)
                
                # Draw background
                self.screen.blit(self.game_bg, (0, 0))
                
                # Draw floor platform
                self.screen.blit(self.final_scene_floor['img'], (self.final_scene_floor['x'], self.final_scene_floor['y']))
                
                # Draw player
                self.player.draw(self.screen)
                
                # Draw lives counter to verify rendering
                self.level_manager.draw_lives(self.screen, self.player)
                
                # Draw domino character at the end
                self.screen.blit(self.domino_img, (self.domino_x, self.domino_y))
                
                # Check proximity to domino (20 pixels)
                distance_to_domino = abs(self.player.rect.x - self.domino_x)
                
                if distance_to_domino <= 20 and not self.final_scene_dialogue_started:
                    self.final_scene_dialogue_started = True
                    self.final_scene_dialogue_timer = pygame.time.get_ticks()
                
                # Show dialogue
                if self.final_scene_dialogue_started:
                    elapsed_time = (pygame.time.get_ticks() - self.final_scene_dialogue_timer) / 1000.0
                    
                    if elapsed_time < 10:
                        # Show domino's dialogue for 10 seconds
                        dialogue_font = pygame.font.Font(None, 32)
                        dialogue_lines = [
                            "Domino: You made it, my friend!",
                            "The perfect pebble, shaped by ice and time.",
                            "No matter how far the ice stretches, you'll always be my friend."
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