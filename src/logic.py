"""
Date: Janurary 19, 2026
Author: Charlie Shao and Anson Xiao
Description: 

This program creates all of the logic behind the scenes. This includes
things like gravity, jumping, collection, information and much more.
"""

# Import Modules
import pygame
from data import PlayerStats
from minigames import BlizzardSurvival
from sprites import Player
class Logic:
    """Base logic class placeholder for shared logic utilities."""
    def __init__(self):
        """Base logic class placeholder."""
        pass

class GameController:
    """Handles level selection UI and menu interactions."""
    def __init__(self):
        """Initialize level selection controller state."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.boxes = {} 
        self.level = 1
        self.view_stats_button = None
        self.showing_stats = False

    def update_game(self, screen, events, save_data=None):
        """Render level selection screen and handle selection input."""
    
        # Fonts used for UI elements
        small_font = pygame.font.SysFont("verdana", 48, bold=True)
        title_font = pygame.font.SysFont("Helvetica", 72, bold=True)
        button_font = pygame.font.SysFont("verdana", 24, bold=True)
        lock_font = pygame.font.SysFont("verdana", 60, bold=True)
        text_surface = title_font.render("LEVELS", True, (0, 0, 160))
        text_rect = text_surface.get_rect(center=(500, 100))
        screen.blit(text_surface, text_rect)

        # Determine highest unlocked level
        max_unlocked = 1
        if save_data:
            max_unlocked = save_data.highest_level_completed + 1

        # Top row (levels 1-3)
        for i in range(3):
            x = 120 + i * 325
            y = 200
            level_num = i + 1
            box_rect = pygame.Rect(x, y, 125, 125)
            self.boxes[level_num] = box_rect  
            
            # Check if level is locked
            is_locked = level_num > max_unlocked
            
            pygame.draw.rect(screen, (150, 150, 150), (x-10, y-10, 145, 145), border_radius=10)
            if is_locked:
                # Draw locked level in gray
                pygame.draw.rect(screen, (100, 100, 100), box_rect, border_radius=10)
                # Draw lock icon
                lock_text = lock_font.render("", True, (50, 50, 50))
                lock_rect = lock_text.get_rect(center=(x + 62, y + 62))
                screen.blit(lock_text, lock_rect)
            else:
                # Draw unlocked level
                pygame.draw.rect(screen, (137, 207, 240), box_rect, border_radius=10)
                text_surface = small_font.render(str(level_num), True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(x + 62, y + 62))
                screen.blit(text_surface, text_rect)

        # Bottom row (levels 4-5)
        for i in range(2):
            x = 270 + i * 325
            y = 425
            level_num = i + 4
            box_rect = pygame.Rect(x, y, 125, 125)
            self.boxes[level_num] = box_rect 
            
            # Check if level is locked
            is_locked = level_num > max_unlocked
            
            pygame.draw.rect(screen, (150, 150, 150), (x-10, y-10, 145, 145), border_radius=10)
            if is_locked:
                # Draw locked level in gray
                pygame.draw.rect(screen, (100, 100, 100), box_rect, border_radius=10)
                # Draw lock icon
                lock_text = lock_font.render("🔒", True, (50, 50, 50))
                lock_rect = lock_text.get_rect(center=(x + 62, y + 62))
                screen.blit(lock_text, lock_rect)
            else:
                # Draw unlocked level
                pygame.draw.rect(screen, (137, 207, 240), box_rect, border_radius=10)
                text_surface = small_font.render(str(level_num), True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(x + 62, y + 62))
                screen.blit(text_surface, text_rect)
        
        # Draw View Stats button in bottom right
        self.view_stats_button = pygame.Rect(820, 520, 160, 60)
        pygame.draw.rect(screen, (50, 50, 150), self.view_stats_button, border_radius=8)
        pygame.draw.rect(screen, (100, 100, 255), self.view_stats_button, 3, border_radius=8)
        stats_text = button_font.render("View Stats", True, (255, 255, 255))
        stats_text_rect = stats_text.get_rect(center=self.view_stats_button.center)
        screen.blit(stats_text, stats_text_rect)

        # Handle clicks on buttons/level boxes
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.view_stats_button and self.view_stats_button.collidepoint(event.pos):
                    if save_data:
                        self.display_stats_screen(screen, save_data)
                elif self.boxes[1].collidepoint(event.pos):
                    # Level 1 is always unlocked
                    self.level = 1
                    return "start_game"
                elif self.boxes[2].collidepoint(event.pos):
                    if save_data and save_data.highest_level_completed >= 1:
                        self.level = 2
                        return "start_game"
                elif self.boxes[3].collidepoint(event.pos):
                    if save_data and save_data.highest_level_completed >= 2:
                        self.level = 3
                        return "start_game"
                elif self.boxes[4].collidepoint(event.pos):
                    if save_data and save_data.highest_level_completed >= 3:
                        self.level = 4
                        return "start_game"
                elif self.boxes[5].collidepoint(event.pos):
                    if save_data and save_data.highest_level_completed >= 4:
                        self.level = 5
                        return "start_game"
                    
    def display_stats_screen(self, screen, save_data):
        """Display player statistics in a popup overlay"""
        overlay = pygame.Surface((1000, 600))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Stats panel
        panel_rect = pygame.Rect(150, 50, 700, 500)
        pygame.draw.rect(screen, (30, 30, 60), panel_rect, border_radius=15)
        pygame.draw.rect(screen, (100, 150, 255), panel_rect, 4, border_radius=15)
        
        # Title
        title_font = pygame.font.SysFont("verdana", 36, bold=True)
        title = title_font.render("Player Statistics", True, (100, 200, 255))
        screen.blit(title, (500 - title.get_width() / 2, 70))
        
        # Stats content
        stats_font = pygame.font.SysFont("verdana", 20)
        y_offset = 120
        
        stats_lines = [
            "Username: %s" % save_data.username,
            "Highest Level Completed: %d" % save_data.highest_level_completed,
            "Current Level: %d" % save_data.levels_reached,
            "Fish Collected: %d" % save_data.fish_collected,
            "Total Fish Ever: %d" % save_data.total_fish_ever,
            "Total Deaths: %d" % save_data.total_deaths,
            "Playtime: %.1f minutes" % (save_data.total_playtime / 60),
            "",
            "Abilities:",
            "  Double Jump: %s" % ("Unlocked" if save_data.double_jump_unlocked else "Locked"),
            "  Intelligence Boost: %s" % ("Unlocked" if save_data.intelligence_boost_unlocked else "Locked"),
            "",
            "Minigame Records:",
            "  Logic Trial: %d" % save_data.logic_trial_best_score,
            "  Blizzard Survival: %.1fs" % save_data.blizzard_survival_best_time,
            "  Fish Frenzy: %d" % save_data.fish_frenzy_high_score,
        ]
        
        for line in stats_lines:
            text = stats_font.render(line, True, (255, 255, 255))
            screen.blit(text, (200, y_offset))
            y_offset += 25
        
        # Close instruction
        close_font = pygame.font.SysFont("verdana", 20)
        close_text = close_font.render("Click anywhere to close", True, (200, 200, 200))
        screen.blit(close_text, (500 - close_text.get_width() / 2, 520))
        
        pygame.display.flip()
        
        # Wait for click to close
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    waiting = False
    
    def start_game(self):
        """Placeholder for start-game hook."""
        pass

    def end_game(self):
        """Placeholder for end-game hook."""
        pass

    def load_level(self, level_number):
        """Placeholder for loading a specific level by number."""
        pass

class Physics:
    """Physics helper for gravity, friction, and collision resolution."""
    def __init__(self):
        """Initialize physics constants for gravity and friction."""
        self.gravity = 2000
        self.max_fall_speed = 1600
        self.ground_friction = 1800
        self.ice_friction = 200  # Low friction for ice - some sliding but more control

    def apply_gravity(self, player, dt):
        """Apply gravity to a player using delta time."""
        # Gravity affects vertical velocity every frame
        player.vel.y += self.gravity * dt
        if player.vel.y > self.max_fall_speed:
            player.vel.y = self.max_fall_speed

    def apply_friction(self, player, dt, surface_friction=None):
        """Apply horizontal friction when grounded and not actively moving."""
        # Only apply friction when on ground
        if not getattr(player, "on_ground", False):
            return
        
        # Don't apply friction if player is actively pressing movement keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_d]:
            return

        # Use ice friction if on ice, otherwise normal ground friction
        if getattr(player, "on_ice", False):
            friction = self.ice_friction
        else:
            friction = self.ground_friction if surface_friction is None else surface_friction
        
        if player.vel.x > 0:
            player.vel.x = max(0, player.vel.x - friction * dt)
        elif player.vel.x < 0:
            player.vel.x = min(0, player.vel.x + friction * dt)

    def handle_collisions(self, player, platforms, ice_platforms=None):
        """Resolve collisions and set grounded/ice state."""
        if ice_platforms is None:
            ice_platforms = []
        
        colliders = []
        for obj in platforms:
            if hasattr(obj, "rect"):
                colliders.append(obj.rect)
            else:
                colliders.append(obj)

        player.on_ground = False
        player.on_ice = False

        # Find the best collision to resolve
        for rect in colliders:
            if player.rect.colliderect(rect):
                # Calculate overlap on each side
                overlap_top = player.rect.bottom - rect.top
                overlap_bottom = rect.bottom - player.rect.top
                overlap_left = player.rect.right - rect.left
                overlap_right = rect.right - player.rect.left

                # Find the smallest overlap (direction to push out)
                min_overlap = min(overlap_top, overlap_bottom, overlap_left, overlap_right)

                # Resolve collision based on smallest overlap
                if min_overlap == overlap_top and player.vel.y > 0:
                    player.rect.bottom = rect.top
                    player.pos.y = player.rect.y
                    player.vel.y = 0
                    player.on_ground = True
                    # Check if standing on any ice platform by checking collision with each
                    for ice_rect in ice_platforms:
                        if player.rect.colliderect(ice_rect) or (abs(player.rect.bottom - ice_rect.top) <= 5 and 
                            player.rect.right > ice_rect.left and player.rect.left < ice_rect.right):
                            player.on_ice = True
                            break
                elif min_overlap == overlap_bottom and player.vel.y < 0:
                    player.rect.top = rect.bottom
                    player.pos.y = player.rect.y
                    player.vel.y = 0
                elif min_overlap == overlap_left and player.vel.x > 0:
                    player.rect.right = rect.left
                    player.pos.x = player.rect.x
                    player.vel.x = 0
                elif min_overlap == overlap_right and player.vel.x < 0:
                    player.rect.left = rect.right
                    player.pos.x = player.rect.x
                    player.vel.x = 0

    def check_water_collision(self, player, water_rect):
        """Return True if the player collides with water."""
        return player.rect.colliderect(water_rect)

class LevelManager:
    """Loads and runs level logic, hazards, and enemy behavior."""
    def __init__(self):
        """Initialize level assets, enemy state, and timers."""
        self.water_x = 0
        self.font = None  # Will be initialized when needed
        self.current_level = 1
        self.level_complete = False
        
        # Load all images once
        self.water_img = pygame.image.load("images/water.png")
        self.water_img = pygame.transform.smoothscale(self.water_img, (50, 50))
        
        self.big_platform_img = pygame.image.load("images/big-platform.png")
        self.big_platform_img = pygame.transform.scale(self.big_platform_img, (350, 100))
        
        self.small_platform_img = pygame.image.load("images/small-platform.png")
        self.small_platform_img = pygame.transform.scale(self.small_platform_img, (150, 50))
        
        self.ice_platform_img = pygame.image.load("images/big-ice-platform.png")
        
        self.portal_img = pygame.image.load("images/portal.png")
        self.portal_img = pygame.transform.smoothscale(self.portal_img, (80, 100))
        
        # Evil tux enemy
        self.evil_tux_img = pygame.image.load("images/evil-penguin.png").convert_alpha()
        self.evil_tux_img = pygame.transform.smoothscale(self.evil_tux_img, (40, 60))
        
        # Level 3 enemy state
        self.evil_tux_x = 0
        self.evil_tux_y = 0
        self.evil_tux_speed = 100
        self.evil_tux_direction = 1  
        self.evil_tux_platform = None 
        
        # Level 5 multiple enemies state
        self.level5_enemies = []  # List of enemy dicts with x, y, speed, direction, platform
        self.level5_enemies_initialized = False
        
        # Death animation state
        self.death_timer = 0
        self.is_dying = False
        self.feedback_timer = 0

    def draw_lives(self, screen, player):
        """Draw life counter and heart icons."""
        if self.font is None:
            self.font = pygame.font.Font(None, 36)
        
        lives_text = self.font.render("Lives: " + str(player.lives), True, (255, 255, 255))
        # Draw background box for visibility
        bg_rect = pygame.Rect(10, 10, lives_text.get_width() + 20, 35)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect, border_radius=5)
        pygame.draw.rect(screen, (100, 100, 100), bg_rect, 2, border_radius=5)
        screen.blit(lives_text, (20, 15))
        
        # Draw heart icons
        for i in range(player.lives):
            heart_x = 130 + i * 30
            pygame.draw.polygon(screen, (255, 50, 50), [
                (heart_x, 25),
                (heart_x - 8, 18),
                (heart_x - 10, 12),
                (heart_x - 6, 8),
                (heart_x, 12),
                (heart_x + 6, 8),
                (heart_x + 10, 12),
                (heart_x + 8, 18)
            ])

    def level_1(self, screen, physics, player, game_bg, clock, save_data=None):
        """Run and render level 1."""
        # Handle death animation
        if self.is_dying:
            self.death_timer -= 1
            if self.death_timer <= 0:
                self.is_dying = False
                result = player.take_damage()
                if result == "game_over":
                    # Reset lives and restart
                    player.reset_lives()
                    player.reset_fish_count()
                player.reset_position()
                # Track death in save data
                if save_data:
                    save_data.add_death()
        
        # Use pre-loaded images
        water_img = self.water_img
        water_speed = 150  # pixels per second
        water_y = screen.get_height() - water_img.get_height()

        dt = clock.tick(60) / 1000

        # Resize big platform for level 1 only
        big_platform = pygame.transform.scale(self.big_platform_img, (250, 80))

        # Level 1: 7 platforms with variety - ascending to portal at top
        # Mark which platforms are ice with 'ice': True - ice platforms are slippery!
        platforms = [
            {'img': self.small_platform_img, 'x': 435, 'y': 450, 'w': 150, 'h': 50, 'ice': False},
            {'img': self.ice_platform_img, 'x': 650, 'y': 380, 'w': self.ice_platform_img.get_width(), 'h': self.ice_platform_img.get_height(), 'ice': True},
            {'img': big_platform, 'x': 130, 'y': 300, 'w': 250, 'h': 70, 'ice': False},
            {'img': big_platform, 'x': 50, 'y': 535, 'w': 250, 'h': 70, 'ice': False},
            {'img': self.ice_platform_img, 'x': 580, 'y': 250, 'w': self.ice_platform_img.get_width(), 'h': self.ice_platform_img.get_height(), 'ice': True},
            {'img': self.small_platform_img, 'x': 750, 'y': 100, 'w': 150, 'h': 50, 'ice': False},
        ]
        
        # Create collision rects and identify ice platforms
        platform_rects = []
        for p in platforms:
            platform_rects.append(pygame.Rect(p['x'], p['y'], p['w'], p['h']))
        
        ice_platform_rects = []
        for p in platforms:
            if p['ice']:
                ice_platform_rects.append(pygame.Rect(p['x'], p['y'], p['w'], p['h']))

        # Add invisible walls around the screen
        left_wall = pygame.Rect(-10, 0, 10, screen.get_height())
        right_wall = pygame.Rect(screen.get_width(), 0, 10, screen.get_height())
        ceiling = pygame.Rect(0, -10, screen.get_width(), 10)

        water_hitbox = pygame.Rect(0, screen.get_height() - water_img.get_height() + 20, screen.get_width(), water_img.get_height())

        # Update water position (move left)
        self.water_x -= water_speed * dt
        
        # Reset water position when one tile cycle is complete
        water_width = water_img.get_width()
        if self.water_x <= -water_width:
            self.water_x = 0

        screen.blit(game_bg, (0, 0))
        
        # Draw water tiles continuously to fill entire screen width
        screen_width = screen.get_width()
        tiles_needed = (screen_width // water_width) + 2
        
        for i in range(tiles_needed):
            screen.blit(water_img, (int(self.water_x + water_width * i), int(water_y)))
        
        # Draw all platforms
        for p in platforms:
            screen.blit(p['img'], (p['x'], p['y']))
        
        # Draw portal on the highest platform
        portal_x = platforms[-1]['x'] + (platforms[-1]['w'] // 2) - 40
        portal_y = platforms[-1]['y'] - 100
        portal_rect = pygame.Rect(portal_x, portal_y, 80, 100)
        screen.blit(self.portal_img, (portal_x, portal_y))

        # Only update player if not dying
        if not self.is_dying:
            physics.apply_gravity(player, dt)
            player.update(dt)
            physics.handle_collisions(player, platform_rects + [left_wall, right_wall, ceiling], ice_platform_rects)
            physics.apply_friction(player, dt)
            
            # Check water collision (death)
            if physics.check_water_collision(player, water_hitbox):
                self.is_dying = True
                self.death_timer = 30  # Half second death animation
            
            # Check portal collision (level complete)
            if player.rect.colliderect(portal_rect):
                self.level_complete = True
                

        player.draw(screen)
        
        # Draw lives UI
        self.draw_lives(screen, player)
        
        # Draw death message if dying
        if self.is_dying:
            if self.font is None:
                self.font = pygame.font.Font(None, 72)
            death_text = self.font.render("Splash!", True, (255, 100, 100))
            text_rect = death_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            
            # Draw semi-transparent background
            bg_surface = pygame.Surface((text_rect.width + 40, text_rect.height + 20))
            bg_surface.fill((0, 0, 0))
            bg_surface.set_alpha(180)
            screen.blit(bg_surface, (text_rect.x - 20, text_rect.y - 10))
            
            # Draw text
            screen.blit(death_text, text_rect)
        
        if self.level_complete:
            win_text = self.font.render("Level 1 Finished!", True, (100, 255, 100))
            text_rect = win_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            
            # Draw semi-transparent background
            bg_surface = pygame.Surface((text_rect.width + 40, text_rect.height + 20))
            bg_surface.fill((0, 0, 0))
            bg_surface.set_alpha(180)
            screen.blit(bg_surface, (text_rect.x - 20, text_rect.y - 10))
            
            # Draw text
            screen.blit(win_text, text_rect)

            self.feedback_timer += 1
            if self.feedback_timer >= 90:
                self.feedback_timer = 0
                return "done"


    def level_2(self, screen, physics, player, game_bg, clock, save_data=None):
        """Run and render level 2."""
        # Handle death animation
        if self.is_dying:
            self.death_timer -= 1
            if self.death_timer <= 0:
                self.is_dying = False
                result = player.take_damage()
                if result == "game_over":
                    # Reset lives and restart
                    player.reset_lives()
                    player.reset_fish_count()
                player.reset_position()
                # Track death in save data
                if save_data:
                    save_data.add_death()
        
        # Use pre-loaded images
        water_img = self.water_img
        water_speed = 180  # Faster water than level 1
        water_y = screen.get_height() - water_img.get_height()

        dt = clock.tick(60) / 1000

        # Resize platforms for level 2
        big_platform = pygame.transform.scale(self.big_platform_img, (200, 70))
        small_platform = pygame.transform.scale(self.small_platform_img, (120, 40))

        # Level 2: Harder layout with ice platforms and more gaps - watch your momentum!
        platforms = [
            {'img': big_platform, 'x': 50, 'y': 480, 'w': 200, 'h': 70, 'ice': False},
            {'img': self.ice_platform_img, 'x': 280, 'y': 420, 'w': self.ice_platform_img.get_width(), 'h': self.ice_platform_img.get_height(), 'ice': True},
            {'img': small_platform, 'x': 200, 'y': 330, 'w': 120, 'h': 40, 'ice': False},
            {'img': self.ice_platform_img, 'x': 380, 'y': 250, 'w': self.ice_platform_img.get_width(), 'h': self.ice_platform_img.get_height(), 'ice': True},
            {'img': self.ice_platform_img, 'x': 600, 'y': 180, 'w': self.ice_platform_img.get_width(), 'h': self.ice_platform_img.get_height(), 'ice': True},
            {'img': big_platform, 'x': 780, 'y': 120, 'w': 200, 'h': 70, 'ice': False},
        ]
        
        # Create collision rects and identify ice platforms
        platform_rects = []
        for p in platforms:
            p['w'] = p['img'].get_width()
            p['h'] = p['img'].get_height()
            platform_rects.append(pygame.Rect(p['x'], p['y'], p['w'], p['h']))
        
        ice_platform_rects = []
        for p in platforms:
            if p['ice']:
                ice_platform_rects.append(pygame.Rect(p['x'], p['y'], p['w'], p['h']))

        # Add invisible walls around the screen
        left_wall = pygame.Rect(-10, 0, 10, screen.get_height())
        right_wall = pygame.Rect(screen.get_width(), 0, 10, screen.get_height())
        ceiling = pygame.Rect(0, -10, screen.get_width(), 10)

        water_hitbox = pygame.Rect(0, screen.get_height() - water_img.get_height() + 20, screen.get_width(), water_img.get_height())

        # Update water position (move left)
        self.water_x -= water_speed * dt
        
        # Reset water position when one tile cycle is complete
        water_width = water_img.get_width()
        if self.water_x <= -water_width:
            self.water_x = 0

        screen.blit(game_bg, (0, 0))
        
        # Draw water tiles continuously to fill entire screen width
        screen_width = screen.get_width()
        tiles_needed = (screen_width // water_width) + 2
        
        for i in range(tiles_needed):
            screen.blit(water_img, (int(self.water_x + water_width * i), int(water_y)))
        
        # Draw all platforms
        for p in platforms:
            screen.blit(p['img'], (p['x'], p['y']))
        
        # Draw portal on the highest platform (top right)
        portal_x = platforms[-1]['x'] + (platforms[-1]['w'] // 2) - 40
        portal_y = platforms[-1]['y'] - 100
        portal_rect = pygame.Rect(portal_x, portal_y, 80, 100)
        screen.blit(self.portal_img, (portal_x, portal_y))

        # Only update player if not dying
        if not self.is_dying:
            physics.apply_gravity(player, dt)
            player.update(dt)
            physics.handle_collisions(player, platform_rects + [left_wall, right_wall, ceiling], ice_platform_rects)
            physics.apply_friction(player, dt)
            
            # Check water collision (death)
            if physics.check_water_collision(player, water_hitbox):
                self.is_dying = True
                self.death_timer = 30  # Half second death animation
            
            # Check portal collision (level complete)
            if player.rect.colliderect(portal_rect):
                self.level_complete = True
                

        player.draw(screen)
        
        # Draw lives UI
        self.draw_lives(screen, player)
        
        # Draw death message if dying
        if self.is_dying:
            if self.font is None:
                self.font = pygame.font.Font(None, 72)
            death_text = self.font.render("Splash!", True, (255, 100, 100))
            text_rect = death_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            
            # Draw semi-transparent background
            bg_surface = pygame.Surface((text_rect.width + 40, text_rect.height + 20))
            bg_surface.fill((0, 0, 0))
            bg_surface.set_alpha(180)
            screen.blit(bg_surface, (text_rect.x - 20, text_rect.y - 10))
            
            # Draw text
            screen.blit(death_text, text_rect)
        
        if self.level_complete:
            if self.font is None:
                self.font = pygame.font.Font(None, 72)
            win_text = self.font.render("Level 2 Finished!", True, (100, 255, 100))
            text_rect = win_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            
            # Draw semi-transparent background
            bg_surface = pygame.Surface((text_rect.width + 40, text_rect.height + 20))
            bg_surface.fill((0, 0, 0))
            bg_surface.set_alpha(180)
            screen.blit(bg_surface, (text_rect.x - 20, text_rect.y - 10))
            
            # Draw text
            screen.blit(win_text, text_rect)

            self.feedback_timer += 1
            if self.feedback_timer >= 90:
                self.feedback_timer = 0
                return "done"

    def level_3(self, screen, physics, player, game_bg, clock, save_data=None):
        """Run and render level 3 with enemy patrol."""
        # Handle death animation
        if self.is_dying:
            self.death_timer -= 1
            if self.death_timer <= 0:
                self.is_dying = False
                result = player.take_damage()
                if result == "game_over":
                    # Reset lives and restart
                    player.reset_lives()
                    player.reset_fish_count()
                player.reset_position()
                # Track death in save data
                if save_data:
                    save_data.add_death()
        
        # Use pre-loaded images
        water_img = self.water_img
        water_speed = 200  # Even faster water
        water_y = screen.get_height() - water_img.get_height()

        dt = clock.tick(60) / 1000

        # Smaller platforms for level 3
        small_platform = pygame.transform.scale(self.small_platform_img, (110, 38))
        tiny_platform = pygame.transform.scale(self.small_platform_img, (85, 32))
        medium_platform = pygame.transform.scale(self.big_platform_img, (160, 50))

        # Level 3: Longer layout with smaller platforms and ice - watch for sliding!
        ice_small = pygame.transform.scale(self.ice_platform_img, (110, 38))
        platforms = [
            {'img': medium_platform, 'x': 30, 'y': 520, 'w': 160, 'h': 50, 'ice': False},
            {'img': ice_small, 'x': 360, 'y': 425, 'w': 110, 'h': 38, 'ice': True},
            {'img': tiny_platform, 'x': 340, 'y': 295, 'w': 85, 'h': 32, 'ice': False},
            {'img': medium_platform, 'x': 380, 'y': 165, 'w': 160, 'h': 35, 'ice': False, 'has_enemy': True},
            {'img': ice_small, 'x': 600, 'y': 100, 'w': 110, 'h': 38, 'ice': True},
            {'img': small_platform, 'x': 750, 'y': 90, 'w': 110, 'h': 38, 'ice': False},
        ]
        
        # Create collision rects and identify ice platforms
        platform_rects = []
        for p in platforms:
            platform_rects.append(pygame.Rect(p['x'], p['y'], p['w'], p['h']))
        
        ice_platform_rects = []
        for p in platforms:
            if p['ice']:
                ice_platform_rects.append(pygame.Rect(p['x'], p['y'], p['w'], p['h']))
        
        # Find enemy platform
        enemy_platform = None
        for p in platforms:
            if p.get('has_enemy', False):
                enemy_platform = p
                break
        
        # Initialize evil tux position on first run
        if enemy_platform and self.evil_tux_platform is None:
            self.evil_tux_platform = enemy_platform
            self.evil_tux_x = enemy_platform['x']
            self.evil_tux_y = enemy_platform['y'] - 60

        # Add invisible walls around the screen
        left_wall = pygame.Rect(-10, 0, 10, screen.get_height())
        right_wall = pygame.Rect(screen.get_width(), 0, 10, screen.get_height())
        ceiling = pygame.Rect(0, -10, screen.get_width(), 10)

        water_hitbox = pygame.Rect(0, screen.get_height() - water_img.get_height() + 20, screen.get_width(), water_img.get_height())

        # Update water position (move left)
        self.water_x -= water_speed * dt
        
        # Reset water position when one tile cycle is complete
        water_width = water_img.get_width()
        if self.water_x <= -water_width:
            self.water_x = 0

        screen.blit(game_bg, (0, 0))
        
        # Draw water tiles continuously to fill entire screen width
        screen_width = screen.get_width()
        tiles_needed = (screen_width // water_width) + 2
        
        for i in range(tiles_needed):
            screen.blit(water_img, (int(self.water_x + water_width * i), int(water_y)))
        
        # Draw all platforms
        for p in platforms:
            screen.blit(p['img'], (p['x'], p['y']))
        
        # Update and draw evil tux
        if enemy_platform and not self.is_dying:
            # Move evil tux along platform
            self.evil_tux_x += self.evil_tux_speed * self.evil_tux_direction * dt
            
            # Bounce at platform edges
            platform_left = enemy_platform['x']
            platform_right = enemy_platform['x'] + enemy_platform['w'] - 40
            
            if self.evil_tux_x <= platform_left:
                self.evil_tux_x = platform_left
                self.evil_tux_direction = 1
            elif self.evil_tux_x >= platform_right:
                self.evil_tux_x = platform_right
                self.evil_tux_direction = -1
            
            self.evil_tux_y = enemy_platform['y'] - 60
        
        # Draw evil tux (flip based on direction)
        if self.evil_tux_direction == 1:
            evil_img = pygame.transform.flip(self.evil_tux_img, True, False)
        else:
            evil_img = self.evil_tux_img
        screen.blit(evil_img, (int(self.evil_tux_x), int(self.evil_tux_y)))
        
        # Evil tux collision rect
        evil_tux_rect = pygame.Rect(int(self.evil_tux_x), int(self.evil_tux_y), 40, 60)
        
        # Draw portal on the highest platform (top right)
        portal_x = platforms[-1]['x'] + (platforms[-1]['w'] // 2) - 40
        portal_y = platforms[-1]['y'] - 100
        portal_rect = pygame.Rect(portal_x, portal_y, 80, 100)
        screen.blit(self.portal_img, (portal_x, portal_y))

        # Only update player if not dying
        if not self.is_dying:
            physics.apply_gravity(player, dt)
            player.update(dt)
            physics.handle_collisions(player, platform_rects + [left_wall, right_wall, ceiling], ice_platform_rects)
            physics.apply_friction(player, dt)
            
            # Check water collision (death)
            if physics.check_water_collision(player, water_hitbox):
                self.is_dying = True
                self.death_timer = 30
            
            # Check evil tux collision (death)
            if player.rect.colliderect(evil_tux_rect):
                self.is_dying = True
                self.death_timer = 30
            
            # Check portal collision (level complete)
            if player.rect.colliderect(portal_rect):
                self.level_complete = True
                # Reset enemy for next time
                self.evil_tux_platform = None
                

        player.draw(screen)
        
        # Draw lives UI
        self.draw_lives(screen, player)
        
        # Draw death message if dying
        if self.is_dying:
            if self.font is None:
                self.font = pygame.font.Font(None, 72)
            death_text = self.font.render("Ouch!", True, (255, 100, 100))
            text_rect = death_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            
            # Draw semi-transparent background
            bg_surface = pygame.Surface((text_rect.width + 40, text_rect.height + 20))
            bg_surface.fill((0, 0, 0))
            bg_surface.set_alpha(180)
            screen.blit(bg_surface, (text_rect.x - 20, text_rect.y - 10))
            
            # Draw text
            screen.blit(death_text, text_rect)
        
        if self.level_complete:
            if self.font is None:
                self.font = pygame.font.Font(None, 72)
            win_text = self.font.render("Level 3 Finished!", True, (100, 255, 100))
            text_rect = win_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            
            # Draw semi-transparent background
            bg_surface = pygame.Surface((text_rect.width + 40, text_rect.height + 20))
            bg_surface.fill((0, 0, 0))
            bg_surface.set_alpha(180)
            screen.blit(bg_surface, (text_rect.x - 20, text_rect.y - 10))
            
            # Draw text
            screen.blit(win_text, text_rect)

            self.feedback_timer += 1
            if self.feedback_timer >= 90:
                self.feedback_timer = 0
                return "done"

    def level_4(self, screen, physics, player, game_bg, clock, save_data=None):
        """Run and render level 4 with lower jump and enemy patrol."""
        # Handle death animation
        if self.is_dying:
            self.death_timer -= 1
            if self.death_timer <= 0:
                self.is_dying = False
                result = player.take_damage()
                if result == "game_over":
                    player.reset_lives()
                    player.reset_fish_count()
                player.reset_position()
                if save_data:
                    save_data.add_death()
        
        water_img = self.water_img
        water_speed = 220  # Same as level 3
        water_y = screen.get_height() - water_img.get_height()

        dt = clock.tick(60) / 1000

        # Platform sizes
        tiny_platform = pygame.transform.scale(self.small_platform_img, (80, 30))
        small_platform = pygame.transform.scale(self.small_platform_img, (110, 38))
        medium_platform = pygame.transform.scale(self.big_platform_img, (150, 45))

        # Reduce jump height for level 4 only
        original_jump = player.jump
        player.jump = 600  # Lower jump height
        
        # Level 4: Complex zigzag layout with enemy and slippery ice platforms
        ice_tiny = pygame.transform.scale(self.ice_platform_img, (80, 30))
        ice_small = pygame.transform.scale(self.ice_platform_img, (110, 38))
        platforms = [
            # Start bottom left
            {'img': medium_platform, 'x': 30, 'y': 520, 'w': 150, 'h': 45, 'ice': False},
            # Go right first - some ice platforms make it tricky!
            {'img': ice_small, 'x': 250, 'y': 460, 'w': 110, 'h': 38, 'ice': True},
            {'img': tiny_platform, 'x': 420, 'y': 410, 'w': 80, 'h': 30, 'ice': False},
            {'img': medium_platform, 'x': 580, 'y': 360, 'w': 150, 'h': 45, 'ice': False, 'has_enemy': True},
            # Now must go back left to continue up
            {'img': ice_tiny, 'x': 420, 'y': 280, 'w': 80, 'h': 30, 'ice': True},
            {'img': small_platform, 'x': 250, 'y': 250, 'w': 110, 'h': 38, 'ice': False},
            {'img': tiny_platform, 'x': 100, 'y': 190, 'w': 80, 'h': 30, 'ice': False},
            # Now go right again to reach portal - more ice!
            {'img': ice_small, 'x': 280, 'y': 140, 'w': 110, 'h': 38, 'ice': True},
            {'img': tiny_platform, 'x': 450, 'y': 100, 'w': 80, 'h': 30, 'ice': False},
            {'img': ice_small, 'x': 600, 'y': 60, 'w': 110, 'h': 38, 'ice': True},
            {'img': medium_platform, 'x': 780, 'y': 100, 'w': 150, 'h': 45, 'ice': False},
        ]
        
        # Create collision rects and identify ice platforms
        platform_rects = []
        for p in platforms:
            platform_rects.append(pygame.Rect(p['x'], p['y'], p['w'], p['h']))
        
        ice_platform_rects = []
        for p in platforms:
            if p['ice']:
                ice_platform_rects.append(pygame.Rect(p['x'], p['y'], p['w'], p['h']))

        # Invisible walls
        left_wall = pygame.Rect(-10, 0, 10, screen.get_height())
        right_wall = pygame.Rect(screen.get_width(), 0, 10, screen.get_height())
        ceiling = pygame.Rect(0, -10, screen.get_width(), 10)
        
        all_collision_rects = platform_rects + [left_wall, right_wall, ceiling]

        water_hitbox = pygame.Rect(0, screen.get_height() - water_img.get_height() + 20, screen.get_width(), water_img.get_height())

        # Update water position
        self.water_x -= water_speed * dt
        water_width = water_img.get_width()
        if self.water_x <= -water_width:
            self.water_x = 0

        screen.blit(game_bg, (0, 0))
        
        # Draw water
        screen_width = screen.get_width()
        tiles_needed = (screen_width // water_width) + 2
        for i in range(tiles_needed):
            screen.blit(water_img, (int(self.water_x + water_width * i), int(water_y)))
        
        # Draw platforms
        for p in platforms:
            screen.blit(p['img'], (p['x'], p['y']))
        
        # Find and initialize evil tux enemy
        enemy_platform = None
        for p in platforms:
            if p.get('has_enemy', False):
                enemy_platform = p
                break
        
        # Initialize evil tux position on first run
        if enemy_platform and self.evil_tux_platform is None:
            self.evil_tux_platform = enemy_platform
            self.evil_tux_x = enemy_platform['x']
            self.evil_tux_y = enemy_platform['y'] - 60
        
        # Update and draw evil tux
        if enemy_platform and not self.is_dying:
            # Move evil tux along platform
            self.evil_tux_x += self.evil_tux_speed * self.evil_tux_direction * dt
            
            # Bounce at platform edges
            platform_left = enemy_platform['x']
            platform_right = enemy_platform['x'] + enemy_platform['w'] - 40
            
            if self.evil_tux_x <= platform_left:
                self.evil_tux_x = platform_left
                self.evil_tux_direction = 1
            elif self.evil_tux_x >= platform_right:
                self.evil_tux_x = platform_right
                self.evil_tux_direction = -1
            
            self.evil_tux_y = enemy_platform['y'] - 60
        
        # Draw evil tux (flip based on direction)
        if self.evil_tux_direction == 1:
            evil_img = pygame.transform.flip(self.evil_tux_img, True, False)
        else:
            evil_img = self.evil_tux_img
        screen.blit(evil_img, (int(self.evil_tux_x), int(self.evil_tux_y)))
        
        # Evil tux collision rect
        evil_tux_rect = pygame.Rect(int(self.evil_tux_x), int(self.evil_tux_y), 40, 60)
        
        # Draw portal on top right platform
        portal_x = platforms[-1]['x'] + (platforms[-1]['w'] // 2) - 40
        portal_y = platforms[-1]['y'] - 100
        portal_rect = pygame.Rect(portal_x, portal_y, 80, 100)
        screen.blit(self.portal_img, (portal_x, portal_y))

        # Update player
        if not self.is_dying:
            physics.apply_gravity(player, dt)
            player.update(dt)
            physics.handle_collisions(player, all_collision_rects, ice_platform_rects)
            physics.apply_friction(player, dt)
            
            if physics.check_water_collision(player, water_hitbox):
                self.is_dying = True
                self.death_timer = 30
            
            # Check evil tux collision
            if player.rect.colliderect(evil_tux_rect):
                self.is_dying = True
                self.death_timer = 30
            
            if player.rect.colliderect(portal_rect):
                self.level_complete = True
                # Reset enemy for next time
                self.evil_tux_platform = None
                # Restore original jump height
                player.jump = original_jump
        
        # Restore jump height if dying
        if self.is_dying:
            player.jump = original_jump

        player.draw(screen)
        self.draw_lives(screen, player)
        
        if self.is_dying:
            if self.font is None:
                self.font = pygame.font.Font(None, 72)
            death_text = self.font.render("Ouch!", True, (255, 100, 100))
            text_rect = death_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            bg_surface = pygame.Surface((text_rect.width + 40, text_rect.height + 20))
            bg_surface.fill((0, 0, 0))
            bg_surface.set_alpha(180)
            screen.blit(bg_surface, (text_rect.x - 20, text_rect.y - 10))
            screen.blit(death_text, text_rect)
        
        if self.level_complete:
            if self.font is None:
                self.font = pygame.font.Font(None, 72)
            win_text = self.font.render("Level 4 Finished!", True, (100, 255, 100))
            text_rect = win_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            bg_surface = pygame.Surface((text_rect.width + 40, text_rect.height + 20))
            bg_surface.fill((0, 0, 0))
            bg_surface.set_alpha(180)
            screen.blit(bg_surface, (text_rect.x - 20, text_rect.y - 10))
            screen.blit(win_text, text_rect)

            self.feedback_timer += 1
            if self.feedback_timer >= 90:
                self.feedback_timer = 0
                return "done"

    def level_5(self, screen, physics, player, game_bg, clock, save_data=None):
        """Run and render the final level with multiple enemies."""
        # Handle death animation
        if self.is_dying:
            self.death_timer -= 1
            if self.death_timer <= 0:
                self.is_dying = False
                result = player.take_damage()
                if result == "game_over":
                    player.reset_lives()
                    player.reset_fish_count()
                    # Reset enemies on game over
                    self.level5_enemies_initialized = False
                player.reset_position()
                if save_data:
                    save_data.add_death()
        
        water_img = self.water_img
        water_speed = 250  # Fastest water speed
        water_y = screen.get_height() - water_img.get_height()

        dt = clock.tick(60) / 1000

        # Small but manageable platforms for a challenging but fair final level
        tiny_platform = pygame.transform.scale(self.small_platform_img, (100, 35))
        small_platform = pygame.transform.scale(self.small_platform_img, (120, 40))
        ice_tiny = pygame.transform.scale(self.ice_platform_img, (110, 38))
        
        # Level 5: The Final Challenge - small platforms, strategic enemies, spread out jumps
        platforms = [
            # Starting area - bottom left
            {'img': small_platform, 'x': 10, 'y': 520, 'w': 120, 'h': 40, 'ice': False, 'enemy': False},
            # First jump series going right - spread out
            {'img': tiny_platform, 'x': 200, 'y': 450, 'w': 100, 'h': 35, 'ice': False, 'enemy': False},
            {'img': ice_tiny, 'x': 400, 'y': 380, 'w': 110, 'h': 38, 'ice': True, 'enemy': False},
            {'img': small_platform, 'x': 620, 'y': 320, 'w': 120, 'h': 40, 'ice': False, 'enemy': True, 'enemy_speed': 90},
            # Middle section - go back left and up
            {'img': tiny_platform, 'x': 400, 'y': 250, 'w': 100, 'h': 35, 'ice': False, 'enemy': False},
            {'img': small_platform, 'x': 150, 'y': 190, 'w': 120, 'h': 40, 'ice': False, 'enemy': True, 'enemy_speed': 100},
            # Upper section - back right to portal
            {'img': ice_tiny, 'x': 380, 'y': 160, 'w': 110, 'h': 38, 'ice': True, 'enemy': False},
            {'img': small_platform, 'x': 620, 'y': 110, 'w': 120, 'h': 40, 'ice': False, 'enemy': True, 'enemy_speed': 110},
            # Final platform with portal
            {'img': small_platform, 'x': 850, 'y': 80, 'w': 120, 'h': 40, 'ice': False, 'enemy': False},
        ]
        
        # Create collision rects and identify ice platforms
        platform_rects = []
        for p in platforms:
            platform_rects.append(pygame.Rect(p['x'], p['y'], p['w'], p['h']))
        
        ice_platform_rects = []
        for p in platforms:
            if p['ice']:
                ice_platform_rects.append(pygame.Rect(p['x'], p['y'], p['w'], p['h']))
        
        # Initialize enemies on platforms that have them
        if not self.level5_enemies_initialized:
            self.level5_enemies = []
            for p in platforms:
                if p.get('enemy', False):
                    enemy = {
                        'x': p['x'],
                        'y': p['y'] - 60,
                        'speed': p.get('enemy_speed', 100),
                        'direction': 1,
                        'platform': p
                    }
                    self.level5_enemies.append(enemy)
            self.level5_enemies_initialized = True

        # Invisible walls
        left_wall = pygame.Rect(-10, 0, 10, screen.get_height())
        right_wall = pygame.Rect(screen.get_width(), 0, 10, screen.get_height())
        ceiling = pygame.Rect(0, -10, screen.get_width(), 10)
        
        all_collision_rects = platform_rects + [left_wall, right_wall, ceiling]

        water_hitbox = pygame.Rect(0, screen.get_height() - water_img.get_height() + 20, screen.get_width(), water_img.get_height())

        # Update water position
        self.water_x -= water_speed * dt
        water_width = water_img.get_width()
        if self.water_x <= -water_width:
            self.water_x = 0

        screen.blit(game_bg, (0, 0))
        
        # Draw water
        screen_width = screen.get_width()
        tiles_needed = (screen_width // water_width) + 2
        for i in range(tiles_needed):
            screen.blit(water_img, (int(self.water_x + water_width * i), int(water_y)))
        
        # Draw platforms
        for p in platforms:
            screen.blit(p['img'], (p['x'], p['y']))
        
        # Update and draw all enemies
        enemy_rects = []
        if not self.is_dying:
            for enemy in self.level5_enemies:
                # Move enemy along its platform
                enemy['x'] += enemy['speed'] * enemy['direction'] * dt
                
                # Bounce at platform edges
                plat = enemy['platform']
                platform_left = plat['x']
                platform_right = plat['x'] + plat['w'] - 40
                
                if enemy['x'] <= platform_left:
                    enemy['x'] = platform_left
                    enemy['direction'] = 1
                elif enemy['x'] >= platform_right:
                    enemy['x'] = platform_right
                    enemy['direction'] = -1
                
                enemy['y'] = plat['y'] - 60
        
        # Draw all enemies and create collision rects
        for enemy in self.level5_enemies:
            if enemy['direction'] == 1:
                evil_img = pygame.transform.flip(self.evil_tux_img, True, False)
            else:
                evil_img = self.evil_tux_img
            screen.blit(evil_img, (int(enemy['x']), int(enemy['y'])))
            enemy_rects.append(pygame.Rect(int(enemy['x']), int(enemy['y']), 40, 60))
        
        # Draw portal on final platform
        portal_x = platforms[-1]['x'] + (platforms[-1]['w'] // 2) - 40
        portal_y = platforms[-1]['y'] - 100
        portal_rect = pygame.Rect(portal_x, portal_y, 80, 100)
        screen.blit(self.portal_img, (portal_x, portal_y))

        # Update player
        if not self.is_dying:
            physics.apply_gravity(player, dt)
            player.update(dt)
            physics.handle_collisions(player, all_collision_rects, ice_platform_rects)
            physics.apply_friction(player, dt)
            
            if physics.check_water_collision(player, water_hitbox):
                self.is_dying = True
                self.death_timer = 30
            
            # Check collision with all enemies
            for enemy_rect in enemy_rects:
                if player.rect.colliderect(enemy_rect):
                    self.is_dying = True
                    self.death_timer = 30
                    break
            
            if player.rect.colliderect(portal_rect):
                self.level_complete = True
                self.level5_enemies_initialized = False

        player.draw(screen)
        self.draw_lives(screen, player)
        
        # Draw level indicator
        if self.font is None:
            self.font = pygame.font.Font(None, 36)
        level_text = self.font.render("FINAL LEVEL", True, (255, 50, 50))
        screen.blit(level_text, (screen.get_width() - 150, 15))
        
        if self.is_dying:
            if self.font is None:
                self.font = pygame.font.Font(None, 72)
            death_text = self.font.render("Ouch!", True, (255, 100, 100))
            text_rect = death_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            bg_surface = pygame.Surface((text_rect.width + 40, text_rect.height + 20))
            bg_surface.fill((0, 0, 0))
            bg_surface.set_alpha(180)
            screen.blit(bg_surface, (text_rect.x - 20, text_rect.y - 10))
            screen.blit(death_text, text_rect)
        
        if self.level_complete:
            if self.font is None:
                self.font = pygame.font.Font(None, 72)
            win_text = self.font.render("GAME COMPLETE!", True, (255, 215, 0))
            text_rect = win_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            bg_surface = pygame.Surface((text_rect.width + 40, text_rect.height + 20))
            bg_surface.fill((0, 0, 0))
            bg_surface.set_alpha(180)
            screen.blit(bg_surface, (text_rect.x - 20, text_rect.y - 10))
            screen.blit(win_text, text_rect)

            self.feedback_timer += 1
            if self.feedback_timer >= 120:  # Longer display for final level
                self.feedback_timer = 0
                return "done"

    def check_level_completion(self):
        """Unlock abilities based on current level milestone."""
        if self.level > 1:
            PlayerStats.unlock_ability(self.level)
        elif self.level > 3:
            PlayerStats.unlock_ability(self.level)

    def unlock_ability(self):
        """Placeholder for manual ability unlocks."""
        pass