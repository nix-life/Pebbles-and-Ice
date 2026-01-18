import pygame
from data import PlayerStats
from sprites import Player
class Logic:
    def __init__(self):
        pass

class GameController:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.boxes = {} 
        self.level = 1

    def update_game(self, screen, events):
    
        small_font = pygame.font.SysFont("verdana", 48, bold=True)
        title_font = pygame.font.SysFont("Helvetica", 72, bold=True)
        text_surface = title_font.render("LEVELS", True, (0, 0, 160))
        text_rect = text_surface.get_rect(center=(500, 100))
        screen.blit(text_surface, text_rect)

        for i in range(3):
            x = 120 + i * 325
            y = 200
            level_num = i + 1
            box_rect = pygame.Rect(x, y, 125, 125)
            self.boxes[level_num] = box_rect  
            
            pygame.draw.rect(screen, (150, 150, 150), (x-10, y-10, 145, 145), border_radius=10)
            pygame.draw.rect(screen, (137, 207, 240), box_rect, border_radius=10)
            text_surface = small_font.render(str(level_num), True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(x + 62, y + 62))
            screen.blit(text_surface, text_rect)

        for i in range(2):
            x = 270 + i * 325
            y = 425
            level_num = i + 4
            box_rect = pygame.Rect(x, y, 125, 125)
            self.boxes[level_num] = box_rect 
            
            pygame.draw.rect(screen, (150, 150, 150), (x-10, y-10, 145, 145), border_radius=10)
            pygame.draw.rect(screen, (137, 207, 240), box_rect, border_radius=10)
            text_surface = small_font.render(str(level_num), True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(x + 62, y + 62))
            screen.blit(text_surface, text_rect)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.boxes[1].collidepoint(event.pos):
                    self.level = 1
                    return "start_game"
                elif self.boxes[2].collidepoint(event.pos): 
                    self.level = 2
                    print("Level 2 selected")
                elif self.boxes[3].collidepoint(event.pos):
                    self.level = 3
                    print("Level 3 selected")
                elif self.boxes[4].collidepoint(event.pos):
                    self.level = 4
                    print("Level 4 selected")
                elif self.boxes[5].collidepoint(event.pos):
                    self.level = 5
                    print("Level 5 selected")
                    
    def start_game(self):
        pass

    def end_game(self):
        pass

    def load_level(self, level_number):
        pass

class Physics:
    def __init__(self):
        self.gravity = 2000
        self.max_fall_speed = 1600
        self.ground_friction = 1800

    def apply_gravity(self, player, dt):
        player.vel.y += self.gravity * dt
        if player.vel.y > self.max_fall_speed:
            player.vel.y = self.max_fall_speed

    def apply_friction(self, player, dt, surface_friction=None):
        if not getattr(player, "on_ground", False):
            return

        friction = self.ground_friction if surface_friction is None else surface_friction
        if player.vel.x > 0:
            player.vel.x = max(0, player.vel.x - friction * dt)
        elif player.vel.x < 0:
            player.vel.x = min(0, player.vel.x + friction * dt)

    def handle_collisions(self, player, objects):
        colliders = []
        for obj in objects:
            if hasattr(obj, "rect"):
                colliders.append(obj.rect)
            else:
                colliders.append(obj)

        player.on_ground = False

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

class LevelManager:
    def __init__(self):
        self.water_x = 0
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

    def level_1(self, screen, physics, player, game_bg, clock):
        # Use pre-loaded images
        water_img = self.water_img
        water_speed = 150  # pixels per second
        water_y = screen.get_height() - water_img.get_height()

        dt = clock.tick(60) / 1000

        # Resize big platform for level 1 only
        big_platform = pygame.transform.scale(self.big_platform_img, (250, 80))

        # Level 1: 7 platforms with variety - ascending to portal at top
        platforms = [
            {'img': self.small_platform_img, 'x': 435, 'y': 450, 'w': 150, 'h': 50},
            {'img': self.ice_platform_img, 'x': 650, 'y': 380, 'w': self.ice_platform_img.get_width(), 'h': self.ice_platform_img.get_height()},
            {'img': big_platform, 'x': 130, 'y': 300, 'w': 250, 'h': 70},
            {'img': big_platform, 'x': 50, 'y': 535, 'w': 250, 'h': 70},
            {'img': self.small_platform_img, 'x': 600, 'y': 250, 'w': 150, 'h': 50},
            {'img': self.small_platform_img, 'x': 750, 'y': 100, 'w': 150, 'h': 50},
        ]
        
        # Create collision rects
        platform_rects = [pygame.Rect(p['x'], p['y'], p['w'], p['h']) for p in platforms]

        # Add invisible walls around the screen
        left_wall = pygame.Rect(-10, 0, 10, screen.get_height())
        right_wall = pygame.Rect(screen.get_width(), 0, 10, screen.get_height())
        ceiling = pygame.Rect(0, -10, screen.get_width(), 10)

        water_hitbox = pygame.Rect(0, screen.get_height() - water_img.get_height(), screen.get_width(), water_img.get_height())

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
        screen.blit(self.portal_img, (portal_x, portal_y))

        physics.apply_gravity(player, dt)
        player.update(dt)
        physics.handle_collisions(player, platform_rects + [water_hitbox, left_wall, right_wall, ceiling])
        physics.apply_friction(player, dt)

        player.draw(screen)

    def level_2(self):
        pass

    def level_3(self):
        pass

    def level_4(self):
        pass

    def level_5(self):
        pass

    def check_level_completion(self):
        if self.level > 1:
            PlayerStats.unlock_ability(self.level)
        elif self.level > 3:
            PlayerStats.unlock_ability(self.level)

    def unlock_ability(self):
        pass