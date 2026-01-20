"""
Date: Janurary 19, 2026
Author: Charlie Shao and Anson Xiao
Description:

This program stores all the information and player stats
to save even after logging out. It uses a text file and 
a login logic for players to save their progress. It also
keeps data for all other important things like characters
and minigames.
"""

from platform import uname
import pygame
import logic 

class Data:
    def __init__(self):
        """Base data class for shared save/data behaviors."""
        pass

class PlayerStats(Data):
    def __init__(self):
        """Initialize player stats UI state and unlocks."""
        pygame.init()
        self.boxes = {}
        self.game_controller = logic.GameController()
        self.double_jump_unlocked = False

    def unlock_ability(self, level):
        """Unlock abilities based on completed level."""
        if level >= 2:
            self.double_jump_unlocked = True
        elif level > 3:
            pass

    def intelligence_level(self):
        """Placeholder for intelligence progression."""
        pass

    def add_fish(self):
        """Placeholder for fish collection tracking."""
        pass
    
    def get_text_input(self, screen, prompt):
        """Simple text input screen"""
        input_text = ""
        font = pygame.font.SysFont("verdana", 36)
        title_font = pygame.font.SysFont("verdana", 48, bold=True)
        
        while True:
            screen.fill((50, 80, 120))
            
            # Draw prompt
            title = title_font.render(prompt, True, (255, 255, 255))
            screen.blit(title, (500 - title.get_width() // 2, 150))
            
            # Draw input box
            input_box = pygame.Rect(250, 300, 500, 60)
            pygame.draw.rect(screen, (255, 255, 255), input_box)
            pygame.draw.rect(screen, (0, 0, 0), input_box, 3)
            
            text_surface = font.render(input_text, True, (0, 0, 0))
            screen.blit(text_surface, (input_box.x + 10, input_box.y + 15))
            
            # Instructions
            inst_font = pygame.font.SysFont("verdana", 24)
            inst = inst_font.render("Press ENTER to continue, ESC to cancel", True, (200, 200, 200))
            screen.blit(inst, (500 - inst.get_width() // 2, 450))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return input_text
                    elif event.key == pygame.K_ESCAPE:
                        return None
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
    
    def login_screen(self, screen, save_data):
        """Screen for returning players to login"""
        username = self.get_text_input(screen, "Enter Username:")
        if username is None:
            return False
        
        password = self.get_text_input(screen, "Enter Password:")
        if password is None:
            return False
        
        # Verify credentials
        if save_data.verify_login(username, password):
            screen.fill((50, 80, 120))
            font = pygame.font.SysFont("verdana", 48, bold=True)
            success = font.render("Login Successful!", True, (100, 255, 100))
            screen.blit(success, (500 - success.get_width() / 2, 250))
            pygame.display.flip()
            pygame.time.wait(1500)
            return True
        else:
            screen.fill((50, 80, 120))
            font = pygame.font.SysFont("verdana", 48, bold=True)
            fail = font.render("Invalid Credentials!", True, (255, 100, 100))
            screen.blit(fail, (500 - fail.get_width() / 2, 250))
            pygame.display.flip()
            pygame.time.wait(1500)
            return False
    
    def register_screen(self, screen, save_data):
        """Screen for new players to create account"""
        username = self.get_text_input(screen, "Create Username:")
        if username is None or username == "":
            return False
        
        password = self.get_text_input(screen, "Create Password:")
        if password is None or password == "":
            return False
    
        # Create account
        if save_data.create_account(username, password):
            screen.fill((50, 80, 120))
            font = pygame.font.SysFont("verdana", 48, bold=True)
            success = font.render("Account Created!", True, (100, 255, 100))
            screen.blit(success, (500 - success.get_width() / 2, 250))
            pygame.display.flip()
            pygame.time.wait(1500)
            return True
        else:
            screen.fill((50, 80, 120))
            font = pygame.font.SysFont("verdana", 48, bold=True)
            error = font.render("Username already exists!", True, (255, 100, 100))
            screen.blit(error, (500 - error.get_width() / 2, 250))
            pygame.display.flip()
            pygame.time.wait(1500)
            return False

    def update_level(self, screen, events):
        """Show returning player prompt and handle selection."""
        small_font = pygame.font.SysFont("verdana", 48, bold=True)
        title_font = pygame.font.SysFont("Helvetica", 72, bold=True)
        text_surface = title_font.render("Returning Player?", True, (0, 0, 160))
        text_rect = text_surface.get_rect(center=(500, 100))
        screen.blit(text_surface, text_rect)
        confirmation = ["Yes", "No"]

        for i in range(2):
            x = 240 + i * 400
            y = 275
            confirmation_num = i + 1
            box_rect = pygame.Rect(x, y, 125, 125)
            self.boxes[confirmation_num] = box_rect  
            
            pygame.draw.rect(screen, (150, 150, 150), (x-10, y-10, 145, 145), border_radius=10)
            pygame.draw.rect(screen, (137, 207, 240), box_rect, border_radius=10)
            text_surface = small_font.render(confirmation[i], True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(x + 62, y + 62))
            screen.blit(text_surface, text_rect)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.boxes[1].collidepoint(event.pos):
                    return "returning"
                elif self.boxes[2].collidepoint(event.pos): 
                    return "new"

        return None
class SaveData(Data):
    """Persistent save data for a player profile."""
    SAVE_FILE = "savedata.txt"
    
    def __init__(self):
        """Initialize default save fields for a new profile."""
        self.game_controller = logic.GameController()
        
        # Default save data
        self.username = ""
        self.password = ""
        self.player_name = ""
        self.levels_reached = 1
        self.highest_level_completed = 0
        self.fish_collected = 0
        self.total_fish_ever = 0
        self.double_jump_unlocked = False
        self.intelligence_boost_unlocked = False
        self.blizzard_survival_best_time = 0.0
        self.ice_puzzle_best_attempts = 0
        self.fish_frenzy_high_score = 0
        self.logic_trial_best_score = 0
        self.achievements = ""
        self.total_deaths = 0
        self.total_playtime = 0.0

    def load_game(self, username):
        """Load a user's saved data by username."""
        savefile = None
        try:
            savefile = open(self.SAVE_FILE, "r")
            lines = savefile.readlines()
            savefile.close()
            
            # Find the user's section
            in_user_section = False
            for line in lines:
                line = line.strip()
                
                # Check for user section marker
                if len(line) > 7 and line[:6] == "[USER:" and line[-1] == "]":
                    current_user = line[6:-1]  # Extract username from [USER:username]
                    in_user_section = (current_user == username)
                    continue
                
                # Only process lines in this user's section
                if in_user_section and "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if key == "username":
                        self.username = value
                    elif key == "password":
                        self.password = value
                    elif key == "player_name":
                        self.player_name = value
                    elif key == "levels_reached":
                        self.levels_reached = int(value)
                    elif key == "highest_level_completed":
                        self.highest_level_completed = int(value)
                    elif key == "fish_collected":
                        self.fish_collected = int(value)
                    elif key == "total_fish_ever":
                        self.total_fish_ever = int(value)
                    elif key == "double_jump_unlocked":
                        self.double_jump_unlocked = value == "True"
                    elif key == "intelligence_boost_unlocked":
                        self.intelligence_boost_unlocked = value == "True"
                    elif key == "blizzard_survival_best_time":
                        self.blizzard_survival_best_time = float(value)
                    elif key == "ice_puzzle_best_attempts":
                        self.ice_puzzle_best_attempts = int(value)
                    elif key == "fish_frenzy_high_score":
                        self.fish_frenzy_high_score = int(value)
                    elif key == "logic_trial_best_score":
                        self.logic_trial_best_score = int(value)
                    elif key == "achievements":
                        self.achievements = value
                    elif key == "total_deaths":
                        self.total_deaths = int(value)
                    elif key == "total_playtime":
                        self.total_playtime = float(value)
            
            return self.username == username
        except:
            if savefile:
                savefile.close()
            return False

    def save_game(self):
        """Save current game data to file (update or append)"""
        # Read all existing data
        all_users_data = {}
        savefile = None

        try:
            savefile = open(self.SAVE_FILE, "r")
            lines = savefile.readlines()
            savefile.close()
            
            current_user = None
            user_lines = []
            
            for line in lines:
                stripped = line.strip()
                # Skip empty lines
                if len(stripped) == 0:
                    continue
                    
                if len(stripped) > 7 and stripped[:6] == "[USER:" and stripped[-1] == "]":
                    # Save previous user's data
                    if current_user:
                        all_users_data[current_user] = user_lines
                    current_user = stripped[6:-1]
                    user_lines = []
                else:
                    user_lines.append(line)
            
            # Save last user's data
            if current_user:
                all_users_data[current_user] = user_lines

        except:
            if savefile:
                savefile.close()

        current_user_data = []
        current_user_data.append("username = %s\n" % self.username)
        current_user_data.append("password = %s\n" % self.password)
        current_user_data.append("player_name = %s\n" % self.player_name)
        current_user_data.append("levels_reached = %d\n" % self.levels_reached)
        current_user_data.append("highest_level_completed = %d\n" % self.highest_level_completed)
        current_user_data.append("fish_collected = %d\n" % self.fish_collected)
        current_user_data.append("total_fish_ever = %d\n" % self.total_fish_ever)
        current_user_data.append("double_jump_unlocked = %s\n" % self.double_jump_unlocked)
        current_user_data.append("intelligence_boost_unlocked = %s\n" % self.intelligence_boost_unlocked)
        current_user_data.append("blizzard_survival_best_time = %.2f\n" % self.blizzard_survival_best_time)
        current_user_data.append("ice_puzzle_best_attempts = %d\n" % self.ice_puzzle_best_attempts)
        current_user_data.append("fish_frenzy_high_score = %d\n" % self.fish_frenzy_high_score)
        current_user_data.append("logic_trial_best_score = %d\n" % self.logic_trial_best_score)
        current_user_data.append("achievements = %s\n" % self.achievements)
        current_user_data.append("total_deaths = %d\n" % self.total_deaths)
        current_user_data.append("total_playtime = %.2f\n" % self.total_playtime)
        
        all_users_data[self.username] = current_user_data

        # Write all users back to file
        savefile = None
        try:
            savefile = open(self.SAVE_FILE, "w")
            for username in all_users_data:
                savefile.write("[USER:%s]\n" % username)
                for line in all_users_data[username]:
                    savefile.write(line)
                savefile.write("\n")
            savefile.close()
            return True
        except:
            if savefile:
                savefile.close()
            return False

    def verify_login(self, username, password):
        """Check if username and password match saved data"""
        if self.load_game(username):
            return self.username == username and self.password == password
        return False

    
    def create_account(self, username, password):
        """Create new account with username and password"""
        if self.load_game(username):
            return False
        
        self.username = username
        self.password = password
        return self.save_game()
    
    # Setters for updating save data
    def set_level_reached(self, level):
        """Update the furthest level reached if higher."""
        if level > self.levels_reached:
            self.levels_reached = level

    def complete_level(self, level):
        """Update highest completed level if higher."""
        if level > self.highest_level_completed:
            self.highest_level_completed = level

    def add_fish(self, amount=1):
        """Increment fish counters for the current session and total."""
        self.fish_collected += amount
        self.total_fish_ever += amount

    def unlock_ability(self, ability_name):
        """Unlock a specific ability by name."""
        if ability_name == "double_jump":
            self.double_jump_unlocked = True
        elif ability_name == "intelligence_boost":
            self.intelligence_boost_unlocked = True

    def update_blizzard_time(self, time_survived):
        """Update best survival time if higher."""
        if time_survived > self.blizzard_survival_best_time:
            self.blizzard_survival_best_time = time_survived

    def update_ice_puzzle_attempts(self, attempts):
        """Update best (lowest) attempt count for ice puzzle."""
        if self.ice_puzzle_best_attempts == 0 or attempts < self.ice_puzzle_best_attempts:
            self.ice_puzzle_best_attempts = attempts

    def update_fish_frenzy_score(self, score):
        """Update fish frenzy high score if higher."""
        if score > self.fish_frenzy_high_score:
            self.fish_frenzy_high_score = score

    def update_logic_trial_score(self, score):
        """Update logic trial high score if higher."""
        if score > self.logic_trial_best_score:
            self.logic_trial_best_score = score

    def add_death(self):
        """Increment total death counter."""
        self.total_deaths += 1

    def add_playtime(self, seconds):
        """Accumulate total playtime in seconds."""
        self.total_playtime += seconds

    def unlock_achievement(self, achievement_name):
        """Add an achievement to the comma-separated list."""
        if achievement_name not in self.achievements:
            if self.achievements == "":
                self.achievements = achievement_name
            else:
                self.achievements = self.achievements + "," + achievement_name

    # Getters for accessing save data
    def get_player_name(self):
        """Return the player display name."""
        return self.player_name

    def get_level_reached(self):
        """Return the furthest level reached."""
        return self.levels_reached

    def get_fish_count(self):
        """Return fish collected in current profile."""
        return self.fish_collected

    def has_ability(self, ability_name):
        """Check if a named ability is unlocked."""
        if ability_name == "double_jump":
            return self.double_jump_unlocked
        elif ability_name == "intelligence_boost":
            return self.intelligence_boost_unlocked
        return False

    def get_minigame_stats(self):
        """Return a dict of best minigame stats."""
        return {
            "blizzard_survival_best_time": self.blizzard_survival_best_time,
            "ice_puzzle_best_attempts": self.ice_puzzle_best_attempts,
            "fish_frenzy_high_score": self.fish_frenzy_high_score,
            "logic_trial_best_score": self.logic_trial_best_score
        }

    def leaderboard(self):
        """Return formatted leaderboard data"""
        return {
            "name": self.player_name,
            "fish": self.total_fish_ever,
            "level": self.highest_level_completed,
            "blizzard_time": self.blizzard_survival_best_time
        }

class TutorialData(Data):
    def __init__(self):
        """Initialize tutorial data container."""
        super().__init__()

    def load_tutorial(self, screen):
        """Display tutorial text over game background"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Pebbles and Ice")
        
        # Load background
        game_bg = pygame.image.load("images/game-background.png")
        game_bg = pygame.transform.smoothscale(game_bg, (1000, 600))
        
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return
            
            # Draw background
            screen.blit(game_bg, (0, 0))

            overlay = pygame.Surface((1000, 600))
            overlay.set_alpha(100)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            # Display tutorial text
            title_font = pygame.font.SysFont("verdana", 60, bold=True)
            text_font = pygame.font.SysFont("verdana", 28)
            
            title = title_font.render("TUTORIAL", True, (255, 255, 255))
            title_rect = title.get_rect(center=(500, 40))
            screen.blit(title, title_rect)
            
            tutorial_lines = [
                "CONTROLS:",
                "A/D - Move left/right     W/SPACE - Jump     S - Save Game",
                "",
                "STORY:",
                "You are a penguin named Tux.",
                "Your goal is to bring a pebble to your friend Domino.",
                "Collect fish to score high on the leaderboard!",
                "",
                "Press any key or click to continue..."
            ]
            
            y_offset = 120
            for line in tutorial_lines:
                text_surface = text_font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(500, y_offset))
                screen.blit(text_surface, text_rect)
                y_offset += 50
            
            pygame.display.flip()
            clock.tick(60)