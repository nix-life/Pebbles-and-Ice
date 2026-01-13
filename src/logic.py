import pygame
class Logic:
    def __init__(self):
        pass

class GameController:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.boxes = {} 

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
                    return "start_game"
                elif self.boxes[2].collidepoint(event.pos): 
                    print("Level 2 selected")
                elif self.boxes[3].collidepoint(event.pos):
                    print("Level 3 selected")
                elif self.boxes[4].collidepoint(event.pos):
                    print("Level 4 selected")
                elif self.boxes[5].collidepoint(event.pos):
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
        super().__init__()

    def start_level(self):
        pass

    def reset_level(self):
        pass

    def check_level_completion(self):
        pass
    
    def unlock_ability(self, level_number):
        pass
