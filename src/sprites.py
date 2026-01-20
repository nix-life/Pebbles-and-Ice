import pygame

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
        player_image = pygame.transform.smoothscale(player_image, (40, 60))
        super().__init__(x=x, y=y, width=40, height=60, image=player_image)
        self.health = 3
        self.lives = 3
        self.speed = 310
        self.jump = 800
        self.abilities = []
        self.on_ground = True
        self.on_ice = False  # Track if player is on ice platform
        self.spawn_x = x  # Store spawn position
        self.spawn_y = y
        self.fish_collected_this_level = 0  # Track fish collected in current level attempt

        self.base = pygame.image.load("images/basetux.png").convert_alpha()
        self.base = pygame.transform.smoothscale(self.base, (40, 60))

        self.tux_left = pygame.image.load("images/tux-left.png").convert_alpha()
        self.tux_left = pygame.transform.smoothscale(self.tux_left, (40, 60))
        
        self.tux_right = pygame.image.load("images/tux-right.png").convert_alpha()
        self.tux_right = pygame.transform.smoothscale(self.tux_right, (40, 60))

        self.falling_tux = pygame.image.load("images/falling-tux.png").convert_alpha()
        self.falling_tux = pygame.transform.smoothscale(self.falling_tux, (60, 60))

    def movement(self, keys):
        # Check if on ice - sliding movement with momentum
        if self.on_ice and self.on_ground:
            # On ice: gradual acceleration, player slides and keeps momentum
            ice_accel = 12
            if keys[pygame.K_a]:
                self.vel.x -= ice_accel
            if keys[pygame.K_d]:
                self.vel.x += ice_accel
            # Clamp max speed on ice
            max_ice_speed = self.speed * 1.2
            if self.vel.x > max_ice_speed:
                self.vel.x = max_ice_speed
            elif self.vel.x < -max_ice_speed:
                self.vel.x = -max_ice_speed
            # Note: friction is applied separately in Physics.apply_friction()
        else:
            # Normal ground - instant directional control
            if keys[pygame.K_a]:
                self.vel.x = -self.speed
            elif keys[pygame.K_d]:
                self.vel.x = self.speed
            else:
                # Only stop instantly if on ground and not on ice
                if self.on_ground:
                    self.vel.x = 0

        if (keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vel.y = -self.jump
            self.on_ground = False

        # Update sprite based on state
        self.update_sprite()

    def update_sprite(self):
        # Use velocity check to prevent glitching
        if abs(self.vel.y) > 50:
            # Falling or jumping with significant velocity
            self.direction = "down"
        elif self.vel.x < 0:
            # Moving left
            self.direction = "left"
        elif self.vel.x > 0:
            # Moving right
            self.direction = "right"
        else:
            # Standing still
            self.direction = "normal"
        
        self.change_direction()

    def change_direction(self):
        if self.direction == "normal":
            player_image = self.base
        elif self.direction == "right":
            player_image = self.tux_right
        elif self.direction == "left":
            player_image = self.tux_left
        elif self.direction == "down":
            player_image = self.falling_tux
        
        self.image = player_image
        self.rect = self.image.get_rect(topleft=(int(self.pos.x), int(self.pos.y)))

    def take_damage(self):
        self.lives -= 1
        if self.lives <= 0:
            return "game_over"
        return "respawn"

    def reset_position(self):
        self.pos.x = self.spawn_x
        self.pos.y = self.spawn_y
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        self.vel.x = 0
        self.vel.y = 0
        self.on_ground = True
        self.on_ice = False

    def reset_lives(self):
        self.lives = 3
    
    def reset_fish_count(self):
        """Reset fish collected for current level attempt"""
        self.fish_collected_this_level = 0
    
    def collect_fish(self):
        """Add a fish to the current level count"""
        self.fish_collected_this_level += 1

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
        import logic, data
        pygame.init()
        pygame.display.set_caption("Pebbles and Ice")
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
        """Main enter screen - shows loading screen with button"""
        self.current_bg = self.before
        self.button_rect = pygame.Rect(405, 462, 150, 53)
        clicked_button = False
        flash_timer = 0

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
                """Move to returning player screen"""
                result = self.loading.update_level(self.screen, self.events)
                self.current_bg = self.game_bg
                self.current_screen = "selection"
                
                # Handle returning player decision
                if result == "returning":
                    """Yes - Login required"""
                    if self.loading.login_screen(self.screen, self.load_data):
                        self.level_selection_loop()
                        return
                    else:
                        clicked_button = False
                        self.current_bg = self.before
                elif result == "new":
                    """No - Create account and open tutorial"""
                    if self.loading.register_screen(self.screen, self.load_data):
                        self.tut.load_tutorial(self.screen)
                        self.level_selection_loop()
                        return
                    else:
                        # Registration failed, restart
                        clicked_button = False
                        self.current_bg = self.before

            pygame.display.flip()

    def level_selection_loop(self):
        """temporary"""
        while True:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
            self.screen.blit(self.game_bg, (0, 0))
            result = self.game_control.update_game(self.screen, self.events, self.load_data)
            if result == "start_game":
                from main import GameLevel
                GameLevel(save_data=self.load_data, start_level=self.game_control.level)
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
        self.hint = ""

    def talk(self):
        pass

    def start_minigame(self):
        pass