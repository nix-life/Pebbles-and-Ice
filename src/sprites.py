import pygame
import logic, data

class Sprites(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, width=32, height=32, image=None, *groups):
        super().__init__(*groups)
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)

        if image is None:
            image = pygame.Surface((width, height), pygame.SRCALPHA)
            image.fill((255, 255, 255, 255))

        self.image = image
        self.rect = self.image.get_rect(topleft=(int(self.pos.x), int(self.pos.y)))

    def update(self, dt=0.0):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def velocity(self):
        return self.vel

    def position(self):
        return self.pos

    def set_position(self, x, y):
        self.pos.update(x, y)
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def set_velocity(self, vx, vy):
        self.vel.update(vx, vy)

class Player(Sprites):
    def __init__(self, x=120, y=120):
        player_image = pygame.image.load("images/basetux.png").convert_alpha()
        player_image = pygame.transform.smoothscale(player_image, (80, 120))
        super().__init__(x=x, y=y, width=40, height=60, image=player_image)
        self.health = 3
        self.speed = 310
        self.jump = 1000
        self.abilities = []
        self.on_ground = False

    def load_tux(self, direction):
        if direction == "up":
            pass
        elif direction == "down":
            pass
        elif direction == "left":
            pass
        elif direction == "right":
            pass

    def movement(self, keys):
        self.vel.x = 0

        if keys[pygame.K_a]:
            self.vel.x = -self.speed
        if keys[pygame.K_d]:
            self.vel.x = self.speed

        if (keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vel.y = -self.jump
            self.on_ground = False

    def take_damage(self):
        pass

    def reset_position(self):
        pass

class Enemy(Sprites):
    def __init__(self):
        super().__init__(width=40, height=40)
        self.damage = 1
        self.speed = 0
        self.detection_range = 0

    def hit_player(self, player):
        pass

    def detect_player(self, player):
        pass

    def move(self):
        pass

class Environment(Sprites):
    def __init__(self):
        pygame.init()
        self.loading = data.PlayerStats()
        self.load_data = data.SaveData()
        self.game_control = logic.GameController()
        self.tut = data.TutorialData()
        self.screen = pygame.display.set_mode((1000, 600))
        self.clock = pygame.time.Clock()
        self.selection = ""
        
        self.platforms_list = []
        self.hazards_list = []
        
        self.before = pygame.image.load("images/mainloading-beforeclick.png")
        self.clicked = pygame.image.load("images/mainloading-clicked.png")
        self.game_bg = pygame.image.load("images/game-background.png")

        self.before = pygame.transform.smoothscale(self.before, (1000, 600))
        self.clicked = pygame.transform.smoothscale(self.clicked, (1000, 600))
        self.game_bg = pygame.transform.smoothscale(self.game_bg, (1000, 600))
         
        self.starting()

    def starting(self):
        self.current_bg = self.before
        self.button_rect = pygame.Rect(405, 462, 150, 53)
        clicked_button = False
        flash_timer = 0
        self.current_screen = "loading" 
        result = ""

        while True:
            dt = self.clock.tick(60) / 1000
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.button_rect.collidepoint(event.pos) and not clicked_button:
                        self.current_bg = self.clicked
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    clicked_button = True
                    flash_timer = 0.4

            self.screen.blit(self.current_bg, (0, 0))
            
            if clicked_button and flash_timer > 0:
                flash_timer -= dt
            elif clicked_button and flash_timer <= 0:
                """temporary"""
                result = self.loading.update_level(self.screen, self.events)
                self.current_bg = self.game_bg
                self.current_screen = "selection"
            
            """temporary"""
            if result == "returning":
                self.level_selection_loop()
                return
            elif result == "new":
                self.show_tutorial()
                return

            pygame.display.flip()

    def show_tutorial(self):
        """Display tutorial text over game background"""
        while True:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return
            
            self.screen.blit(self.game_bg, (0, 0))
            
            # Display tutorial text
            title_font = pygame.font.SysFont("verdana", 60, bold=True)
            text_font = pygame.font.SysFont("verdana", 32)
            
            title = title_font.render("TUTORIAL", True, (255, 255, 255))
            title_rect = title.get_rect(center=(500, 80))
            self.screen.blit(title, title_rect)
            
            tutorial_lines = [
                "A/D - Move left/right",
                "W/SPACE - Jump",
                "Avoid obstacles and reach the end!",
                "",
                "write more later"
            ]
            
            y_offset = 200
            for line in tutorial_lines:
                text_surface = text_font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(500, y_offset))
                self.screen.blit(text_surface, text_rect)
                y_offset += 80
            
            pygame.display.flip()
            self.clock.tick(60)

    def level_selection_loop(self):
        """temporary"""
        while True:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
            self.screen.blit(self.game_bg, (0, 0))
            result = self.game_control.update_game(self.screen, self.events)
            if result == "start_game":
                pygame.quit()
                import main
                main.Main()
                return
            pygame.display.flip()

    def platforms(self):
        pass

    def update_environment(self):
        pass

class NPC(Sprites):
    def __init__(self):
        super().__init__(width=40, height=60)
        self.dialogue = []
        self.has_minigame = False
        self.hint = ""

    def talk(self):
        pass

    def give_hint(self):
        pass

    def start_minigame(self):
        pass

if __name__ == "__main__":
    Environment()