"""
Date: Janurary 19, 2026
Authors: Charlie Shao and Anxon Xiao
Description:
This file creates sprites and objects for pebbles and ice. 
It includes many different sprites, including the main character, 
the platforms and npcs, and much more. Each sprites has its own characteristics,
described in its method.
"""

# Import module
import pygame

class Sprites(pygame.sprite.Sprite):
    """
    This class creates an parent class for all other sprites. Everything
    is connected to this class.
    """
    def __init__(self, x=0, y=0, width=32, height=32, image=None, *groups):
        """Initialize a generic sprite with position, velocity, and image."""
        super().__init__(*groups)
        # Floating-point position and velocity
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)

        if image is None:
            # Create a default placeholder surface if no image is provided
            image = pygame.Surface((width, height), pygame.SRCALPHA)
            image.fill((255, 255, 255, 255))

        # Store the active image and update the rect
        self.image = image
        self.rect = self.image.get_rect(topleft=(int(self.pos.x), int(self.pos.y)))

    def update(self, dt=0.0):
        """Update position based on velocity and delta time."""
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def draw(self, surface):
        """Draw sprite to the given surface."""
        surface.blit(self.image, self.rect)

    def velocity(self):
        """Return current velocity vector."""
        return self.vel

    def position(self):
        """Return current position vector."""
        return self.pos

    def set_position(self, x, y):
        """Set position and update rect."""
        self.pos.update(x, y)
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def set_velocity(self, vx, vy):
        """Set velocity vector."""
        self.vel.update(vx, vy)

class Player(Sprites):
    """
    This class defines and initializes all information for the main
    character tux. It includes the image, health, speed, jump power, 
    abilities, gravity and much more.
    """
    def __init__(self, x=120, y=120):
        """Initialize player sprite, movement stats, and animation frames."""
        # Load base player sprite
        player_image = pygame.image.load("images/basetux.png").convert_alpha()
        player_image = pygame.transform.smoothscale(player_image, (40, 60))
        super().__init__(x=x, y=y, width=40, height=60, image=player_image)
        # Core player stats and movement settings
        self.health = 3
        self.lives = 3
        self.speed = 310
        self.jump = 800
        self.on_ground = True
        self.on_ice = False  # Track if player is on ice platform
        self.spawn_x = x  # Store spawn position
        self.spawn_y = y

        # Load animation frames
        self.base = pygame.image.load("images/basetux.png").convert_alpha()
        self.base = pygame.transform.smoothscale(self.base, (40, 60))

        self.tux_left = pygame.image.load("images/tux-left.png").convert_alpha()
        self.tux_left = pygame.transform.smoothscale(self.tux_left, (40, 60))
        
        self.tux_right = pygame.image.load("images/tux-right.png").convert_alpha()
        self.tux_right = pygame.transform.smoothscale(self.tux_right, (40, 60))

        self.falling_tux = pygame.image.load("images/falling-tux.png").convert_alpha()
        self.falling_tux = pygame.transform.smoothscale(self.falling_tux, (60, 60))
        
        # Initialize direction state
        self.direction = "normal"
        
        # Load jump sound effect
        self.jump_sound = pygame.mixer.Sound("sound/jump.mp3")

    def movement(self, keys):
        """Handle player input and apply movement intent to velocity."""
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
            # Only allow jumps when grounded
            self.vel.y = -self.jump
            self.on_ground = False
            self.jump_sound.play()  # Play jump sound effect

        # Update sprite based on state
        self.update_sprite()

    def update_sprite(self):
        """Select animation frame based on current velocity state."""
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
        """Swap sprite image based on current direction state."""
        # Choose the frame based on direction state
        if self.direction == "normal":
            player_image = self.base
        elif self.direction == "right":
            player_image = self.tux_right
        elif self.direction == "left":
            player_image = self.tux_left
        elif self.direction == "down":
            player_image = self.falling_tux
        else:
            # Default to base if direction is unknown
            player_image = self.base
        
        self.image = player_image
        self.rect = self.image.get_rect(topleft=(int(self.pos.x), int(self.pos.y)))

    def take_damage(self):
        """Reduce life count and return state transition string."""
        self.lives -= 1
        if self.lives <= 0:
            return "game_over"
        return "respawn"

    def reset_position(self):
        """Return player to spawn position and reset movement state."""
        self.pos.x = self.spawn_x
        self.pos.y = self.spawn_y
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        self.vel.x = 0
        self.vel.y = 0
        self.on_ground = True
        self.on_ice = False

    def reset_lives(self):
        """Reset life count to default."""
        self.lives = 3

    def reload_images(self):
        """Reload all player images after display mode change."""
        self.base = pygame.image.load("images/basetux.png").convert_alpha()
        self.base = pygame.transform.smoothscale(self.base, (40, 60))

        self.tux_left = pygame.image.load("images/tux-left.png").convert_alpha()
        self.tux_left = pygame.transform.smoothscale(self.tux_left, (40, 60))
        
        self.tux_right = pygame.image.load("images/tux-right.png").convert_alpha()
        self.tux_right = pygame.transform.smoothscale(self.tux_right, (40, 60))

        self.falling_tux = pygame.image.load("images/falling-tux.png").convert_alpha()
        self.falling_tux = pygame.transform.smoothscale(self.falling_tux, (60, 60))
        
        # Reset direction and update current image
        self.direction = "normal"
        self.image = self.base
        self.rect = self.image.get_rect(topleft=(int(self.pos.x), int(self.pos.y)))

class Enemy(Sprites):
    """
    This class creates sprites for enemies against tux. They spawn
    as red penguins, killing tux when it is touched.
    """
    def __init__(self):
        """Initialize base enemy stats."""
        super().__init__(width=40, height=40)
        # Default values; specific enemies may override these
        self.damage = 1
        self.speed = 0
        self.detection_range = 0

class Environment(Sprites):
    """
    This sprite includes all of the environment behind the scenes.
    It includes the main level screens and main screen that is loaded.
    """
    def __init__(self):
        """Initialize main menu environment and assets."""
        import logic, data
        pygame.init()
        pygame.mixer.init()  # Initialize sound mixer
        pygame.display.set_caption("Pebbles and Ice")
        
        # Load sound effects
        self.click_sound = pygame.mixer.Sound("sound/click.mp3")
        self.death_sound = pygame.mixer.Sound("sound/death.wav")
        self.jump_sound = pygame.mixer.Sound("sound/jump.mp3")
        self.win_sound = pygame.mixer.Sound("sound/win.mp3")
        
        # Start background music (loops indefinitely)
        pygame.mixer.music.load("sound/background-music.mp3")
        pygame.mixer.music.set_volume(0.5)  # Set to 50% volume
        pygame.mixer.music.play(-1)  # -1 means loop forever
        
        # Load/save handlers and controllers
        self.loading = data.PlayerStats()
        self.load_data = data.SaveData()
        self.game_control = logic.GameController()
        self.tut = data.TutorialData()
        self.screen = pygame.display.set_mode((1000, 600))
        self.clock = pygame.time.Clock()
        # Current selection state for menu flow
        self.selection = ""
        
        # Lists for environment objects (reserved for future use)
        self.platforms_list = []
        self.hazards_list = []
        
        # Menu/background images
        self.before = pygame.image.load("images/mainloading-beforeclick.png")
        self.clicked = pygame.image.load("images/mainloading-clicked.png")
        self.game_bg = pygame.image.load("images/game-background.png")

        self.before = pygame.transform.smoothscale(self.before, (1000, 600))
        self.clicked = pygame.transform.smoothscale(self.clicked, (1000, 600))
        self.game_bg = pygame.transform.smoothscale(self.game_bg, (1000, 600))
         
        self.starting()

    def starting(self):
        """Main enter screen - shows loading screen with button."""
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
                        # Visual feedback when the start button is pressed
                        self.click_sound.play()
                        self.current_bg = self.clicked
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # Start the transition once the mouse is released
                    clicked_button = True
                    flash_timer = 0.4

            self.screen.blit(self.current_bg, (0, 0))
            
            if clicked_button and flash_timer > 0:
                # Short flash delay before moving to the next screen
                flash_timer -= dt
            elif clicked_button and flash_timer <= 0:
                # Move to returning player screen
                result = self.loading.update_level(self.screen, self.events)
                self.current_bg = self.game_bg
                self.current_screen = "selection"
                
                # Handle returning player decision
                if result == "returning":
                    # Yes - login required
                    if self.loading.login_screen(self.screen, self.load_data):
                        self.level_selection_loop()
                        return
                    else:
                        clicked_button = False
                        self.current_bg = self.before
                elif result == "new":
                    # No - create account and open tutorial
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
        """This includes all level loading information."""
        while True:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
            self.screen.blit(self.game_bg, (0, 0))
            # Draw level selection UI and process clicks
            result = self.game_control.update_game(self.screen, self.events, self.load_data)
            if result == "start_game":
                # Import locally to avoid circular imports
                from main import GameLevel
                GameLevel(save_data=self.load_data, start_level=self.game_control.level)
                
                # After returning from GameLevel (after minigame), reinitialize pygame and screen
                pygame.init()
                self.screen = pygame.display.set_mode((1000, 600))
                pygame.display.set_caption("Pebbles and Ice")
                self.game_bg = pygame.image.load("images/game-background.png")
                self.game_bg = pygame.transform.smoothscale(self.game_bg, (1000, 600))
                # Continue loop to show level selection again
                
            pygame.display.flip()