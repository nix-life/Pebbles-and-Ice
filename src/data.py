import pygame
import logic 

class Data:
    def __init__(self):
        pass

class PlayerStats(Data):
    def __init__(self):
        pygame.init()
        self.boxes = {}
        self.game_controller = logic.GameController()

    def unlock_ability(self):
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
    def __init__(self):
        self.game_controller = logic.GameController()

    def load_game(self, screen):
        pass

    def save_game(self):
        pass

    def leaderboard(self):
        pass

class TutorialData(Data):
    def __init__(self):
        super().__init__()

    def load_tutorial(self, screen):
        print("Loading tutorial...")
