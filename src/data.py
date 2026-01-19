import pygame
import logic 
import os

class Data:
    def __init__(self):
        pass

class PlayerStats(Data):
    def __init__(self):
        pygame.init()
        self.boxes = {}
        self.game_controller = logic.GameController()
        self.double_jump_unlocked = False

    def unlock_ability(self, level):
        if level >= 2:
            self.double_jump_unlocked = True
            print("Double Jump ability unlocked!")
        elif level > 3:
            pass

    def intelligence_level(self):
        pass

    def add_fish(self):
        pass

    def update_level(self, screen, events):
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

class AchivementData(Data):
    def __init__(self):
        super().__init__()

    def unlock_achivements(self):
        pass

    def minigame_record(self):
        pass

class SaveData(Data):
    SAVE_FILE = "savedata.txt"
    
    def __init__(self):
        self.game_controller = logic.GameController()
        
        # Default save data
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

    def load_game(self):
        f = None
        try:
            f = open(self.SAVE_FILE, "r")
            lines = f.readlines()
            f.close()
            
            for line in lines:
                line = line.strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if key == "player_name":
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
            
            print("Game loaded successfully!")
            return True
        except:
            if f:
                f.close()
            print("Error loading save file")
            return False

    def save_game(self):
        """Save current game data to file"""
        f = None
        try:
            f = open(self.SAVE_FILE, "w")
            f.write("player_name = %s\n" % self.player_name)
            f.write("levels_reached = %d\n" % self.levels_reached)
            f.write("highest_level_completed = %d\n" % self.highest_level_completed)
            f.write("fish_collected = %d\n" % self.fish_collected)
            f.write("total_fish_ever = %d\n" % self.total_fish_ever)
            f.write("double_jump_unlocked = %s\n" % self.double_jump_unlocked)
            f.write("intelligence_boost_unlocked = %s\n" % self.intelligence_boost_unlocked)
            f.write("blizzard_survival_best_time = %.2f\n" % self.blizzard_survival_best_time)
            f.write("ice_puzzle_best_attempts = %d\n" % self.ice_puzzle_best_attempts)
            f.write("fish_frenzy_high_score = %d\n" % self.fish_frenzy_high_score)
            f.write("logic_trial_best_score = %d\n" % self.logic_trial_best_score)
            f.write("achievements = %s\n" % self.achievements)
            f.write("total_deaths = %d\n" % self.total_deaths)
            f.write("total_playtime = %.2f\n" % self.total_playtime)
            f.close()
            print("Game saved successfully!")
            return True
        except:
            if f:
                f.close()
            print("Error saving game")
            return False

    # Setters for updating save data
    def set_player_name(self, name):
        self.player_name = name

    def set_level_reached(self, level):
        if level > self.levels_reached:
            self.levels_reached = level

    def complete_level(self, level):
        if level > self.highest_level_completed:
            self.highest_level_completed = level

    def add_fish(self, amount=1):
        self.fish_collected += amount
        self.total_fish_ever += amount

    def unlock_ability(self, ability_name):
        if ability_name == "double_jump":
            self.double_jump_unlocked = True
        elif ability_name == "intelligence_boost":
            self.intelligence_boost_unlocked = True

    def update_blizzard_time(self, time_survived):
        if time_survived > self.blizzard_survival_best_time:
            self.blizzard_survival_best_time = time_survived

    def update_ice_puzzle_attempts(self, attempts):
        if self.ice_puzzle_best_attempts == 0 or attempts < self.ice_puzzle_best_attempts:
            self.ice_puzzle_best_attempts = attempts

    def update_fish_frenzy_score(self, score):
        if score > self.fish_frenzy_high_score:
            self.fish_frenzy_high_score = score

    def update_logic_trial_score(self, score):
        if score > self.logic_trial_best_score:
            self.logic_trial_best_score = score

    def add_death(self):
        self.total_deaths += 1

    def add_playtime(self, seconds):
        self.total_playtime += seconds

    def unlock_achievement(self, achievement_name):
        if achievement_name not in self.achievements:
            if self.achievements == "":
                self.achievements = achievement_name
            else:
                self.achievements = self.achievements + "," + achievement_name

    # Getters for accessing save data
    def get_player_name(self):
        return self.player_name

    def get_level_reached(self):
        return self.levels_reached

    def get_fish_count(self):
        return self.fish_collected

    def has_ability(self, ability_name):
        if ability_name == "double_jump":
            return self.double_jump_unlocked
        elif ability_name == "intelligence_boost":
            return self.intelligence_boost_unlocked
        return False

    def get_minigame_stats(self):
        return {
            "blizzard_survival_best_time": self.blizzard_survival_best_time,
            "ice_puzzle_best_attempts": self.ice_puzzle_best_attempts,
            "fish_frenzy_high_score": self.fish_frenzy_high_score,
            "logic_trial_best_score": self.logic_trial_best_score
        }

    def get_achievements(self):
        if self.achievements == "":
            return []
        return self.achievements.split(",")

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
                "A/D - Move left/right     W/SPACE - Jump",
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