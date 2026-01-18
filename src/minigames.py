import pygame
import random

class Minigame:
    def __init__(self):
        pass

    def check_minigame(self, minigame):
        # TODO: Add transition later for all minigames between level + minigame
        if minigame == "ice":
            IcePuzzle()

        if minigame == "blizzard":
            BlizzardSurvival()

        if minigame == "fish":
            FishFrenzy()

        if minigame == "dodge":
            BlizzardSurvival()
class IcePuzzle(Minigame):
    def __init__(self):
        super().__init__()

        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Ice Puzzle - Find the Path!")
        
        # Grid settings
        self.grid_cols = 20
        self.grid_rows = 5
        self.tile_size = 45
        self.grid_x = (1000 - self.grid_cols * self.tile_size) // 2  # Center horizontally
        self.grid_y = 180
        
        # Create the grid and path
        self.grid = []  # 0 = fake ice, 1 = solid ice (path)
        self.path = []  # List of (col, row) tuples for the correct path
        self.generate_path()
        
        # Player state
        self.player_pos = self.path[0]  # Start at beginning of path
        self.visited = [self.path[0]]  # Track visited tiles
        self.previous_pos = None  # Can't go back here
        
        # Game state
        self.game_state = "playing"  # "playing", "falling", "won", "restart"
        self.fall_timer = 0
        self.win_timer = 0
        self.attempts = 0
        
        # Hint flash system
        self.hint_timer = 0
        self.hint_duration = 45  # How long the hint shows (frames) - 0.75 seconds
        self.hint_interval = 120  # How often hints appear (2 seconds)
        self.hint_index = 0  # Which part of path to hint
        
        # Visual effects
        self.hover_tile = None
        self.fall_offset = 0
        
        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)

        self.loop()

        pygame.quit()

    def generate_path(self):
        """Generate a random path from left to right through the grid"""
        self.grid = [[0 for _ in range(self.grid_cols)] for _ in range(self.grid_rows)]
        self.path = []
        
        # Start from a random row on the left side
        current_row = random.randint(1, self.grid_rows - 2)
        current_col = 0
        
        self.path.append((current_col, current_row))
        self.grid[current_row][current_col] = 1
        
        # Track consecutive same-direction moves to force variety
        consecutive_right = 0
        max_consecutive_right = 2  # Force vertical movement after 2 rights
        
        while current_col < self.grid_cols - 1:
            # Possible moves: right, up, down
            possible_vertical = []
            
            # Can move up if not at top
            if current_row > 0 and (current_col, current_row - 1) not in self.path:
                possible_vertical.append((current_col, current_row - 1))
            
            # Can move down if not at bottom
            if current_row < self.grid_rows - 1 and (current_col, current_row + 1) not in self.path:
                possible_vertical.append((current_col, current_row + 1))
            
            # Decide movement
            # Force vertical if we've gone right too many times
            if consecutive_right >= max_consecutive_right and possible_vertical:
                next_pos = random.choice(possible_vertical)
                consecutive_right = 0
            # Near the end, must go right
            elif current_col >= self.grid_cols - 2:
                next_pos = (current_col + 1, current_row)
                consecutive_right += 1
            # Otherwise, 40% right, 60% vertical (if possible)
            elif possible_vertical and random.random() < 0.6:
                next_pos = random.choice(possible_vertical)
                consecutive_right = 0
            else:
                next_pos = (current_col + 1, current_row)
                consecutive_right += 1
            
            current_col, current_row = next_pos
            self.path.append(next_pos)
            self.grid[current_row][current_col] = 1

    def get_adjacent_tiles(self, col, row):
        """Get valid adjacent tiles (up, down, left, right)"""
        adjacent = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # up, down, left, right
        
        for dx, dy in directions:
            new_col, new_row = col + dx, row + dy
            if 0 <= new_col < self.grid_cols and 0 <= new_row < self.grid_rows:
                adjacent.append((new_col, new_row))
        
        return adjacent

    def get_tile_rect(self, col, row):
        """Get the pygame Rect for a tile"""
        x = self.grid_x + col * self.tile_size
        y = self.grid_y + row * self.tile_size
        return pygame.Rect(x, y, self.tile_size, self.tile_size)

    def get_tile_at_pos(self, mouse_pos):
        """Get the grid position (col, row) at mouse position, or None"""
        mx, my = mouse_pos
        col = (mx - self.grid_x) // self.tile_size
        row = (my - self.grid_y) // self.tile_size
        
        if 0 <= col < self.grid_cols and 0 <= row < self.grid_rows:
            return (col, row)
        return None

    def is_valid_move(self, target_pos):
        """Check if moving to target position is valid"""
        if target_pos is None:
            return False
        
        # Must be adjacent to current position
        adjacent = self.get_adjacent_tiles(self.player_pos[0], self.player_pos[1])
        if target_pos not in adjacent:
            return False
        
        # Can't go back to previous position
        if target_pos == self.previous_pos:
            return False
        
        # Can't revisit tiles (except if we're checking path validity)
        if target_pos in self.visited:
            return False
        
        return True

    def restart_puzzle(self):
        """Restart the puzzle after falling"""
        self.player_pos = self.path[0]
        self.visited = [self.path[0]]
        self.previous_pos = None
        self.game_state = "playing"
        self.fall_offset = 0
        self.attempts += 1

    def draw_grid(self):
        """Draw the ice grid"""
        # Determine if we're showing a hint
        showing_hint = self.hint_timer > 0
        
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                rect = self.get_tile_rect(col, row)
                tile_pos = (col, row)
                
                # Base ice color
                if tile_pos in self.visited:
                    # Visited tiles - show as solid
                    color = (100, 180, 255)
                    border_color = (50, 130, 200)
                elif tile_pos == self.player_pos:
                    # Player position
                    color = (150, 220, 255)
                    border_color = (100, 180, 230)
                else:
                    # Unvisited tiles - all look the same (mysterious)
                    color = (200, 230, 255)
                    border_color = (150, 200, 230)
                    
                    # Hint flash for path tiles
                    if showing_hint:
                        # Find the next few tiles in the path after current position
                        try:
                            current_path_index = self.path.index(self.player_pos)
                            hint_range = range(current_path_index + 1, min(current_path_index + 4, len(self.path)))
                            if any(self.path[i] == tile_pos for i in hint_range):
                                # Visible hint - pulsing cyan/green color
                                pulse = abs((self.hint_timer % 20) - 10) / 10  # Pulse 0-1
                                hint_r = int(100 + pulse * 50)
                                hint_g = int(220 + pulse * 35)
                                hint_b = int(180 + pulse * 50)
                                color = (hint_r, hint_g, hint_b)
                                border_color = (80, 200, 160)
                        except ValueError:
                            pass
                
                # Hover effect - shows clickable tiles (neutral color, doesn't indicate safety)
                if tile_pos == self.hover_tile and self.game_state == "playing":
                    if self.is_valid_move(tile_pos):
                        # Valid move - light highlight (not green, since we don't know if it's safe)
                        color = (220, 240, 255)
                        border_color = (180, 200, 230)
                    elif tile_pos != self.previous_pos and tile_pos not in self.visited:
                        # Not adjacent - can't click
                        color = (200, 200, 210)
                        border_color = (170, 170, 180)
                
                # Draw the tile
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, border_color, rect, 2)
                
                # Add ice texture (simple lines)
                if random.random() < 0.3:
                    crack_x = rect.x + random.randint(5, self.tile_size - 5)
                    crack_y1 = rect.y + random.randint(5, self.tile_size // 2)
                    crack_y2 = rect.y + random.randint(self.tile_size // 2, self.tile_size - 5)
                    pygame.draw.line(self.screen, (180, 210, 240), (crack_x, crack_y1), (crack_x, crack_y2), 1)

    def draw_player(self):
        """Draw the player marker"""
        if self.game_state == "falling":
            # Falling animation
            rect = self.get_tile_rect(self.player_pos[0], self.player_pos[1])
            center_x = rect.centerx
            center_y = rect.centery + self.fall_offset
            
            # Shrinking circle as player falls
            size = max(5, 15 - self.fall_offset // 10)
            alpha = max(0, 255 - self.fall_offset * 3)
            
            pygame.draw.circle(self.screen, (50, 100, 200), (center_x, center_y), size)
        else:
            rect = self.get_tile_rect(self.player_pos[0], self.player_pos[1])
            # Player is a penguin-like circle
            pygame.draw.circle(self.screen, (30, 30, 30), rect.center, 15)
            pygame.draw.circle(self.screen, (255, 255, 255), (rect.centerx - 3, rect.centery - 3), 5)
            pygame.draw.circle(self.screen, (255, 255, 255), (rect.centerx + 3, rect.centery - 3), 5)
            pygame.draw.circle(self.screen, (0, 0, 0), (rect.centerx - 3, rect.centery - 3), 2)
            pygame.draw.circle(self.screen, (0, 0, 0), (rect.centerx + 3, rect.centery - 3), 2)
            pygame.draw.polygon(self.screen, (255, 180, 0), [
                (rect.centerx, rect.centery + 2),
                (rect.centerx - 5, rect.centery + 8),
                (rect.centerx + 5, rect.centery + 8)
            ])

    def draw_ui(self):
        """Draw UI elements"""
        # Title
        title_text = self.font_medium.render("Find the Safe Path!", True, (0, 0, 0))
        self.screen.blit(title_text, (500 - title_text.get_width() // 2, 20))
        
        # Instructions
        inst_text = self.font_small.render("Watch for the GREEN GLOW - it shows the safe path!", True, (50, 50, 50))
        self.screen.blit(inst_text, (500 - inst_text.get_width() // 2, 70))
        
        # Hint indicator
        if self.hint_timer > 0:
            hint_text = self.font_small.render(">>> HINT ACTIVE <<<", True, (0, 180, 100))
            self.screen.blit(hint_text, (500 - hint_text.get_width() // 2, 100))
        else:
            # Show countdown to next hint
            time_to_hint = (self.hint_interval + self.hint_timer) / 60
            countdown_text = self.font_small.render("Next hint in: %.1fs" % time_to_hint, True, (150, 150, 150))
            self.screen.blit(countdown_text, (500 - countdown_text.get_width() // 2, 100))
        
        # Start and End markers
        start_rect = self.get_tile_rect(self.path[0][0], self.path[0][1])
        end_rect = self.get_tile_rect(self.path[-1][0], self.path[-1][1])
        
        start_text = self.font_small.render("START", True, (0, 150, 0))
        end_text = self.font_small.render("END", True, (200, 0, 0))
        
        self.screen.blit(start_text, (start_rect.centerx - start_text.get_width() // 2, start_rect.y - 30))
        self.screen.blit(end_text, (end_rect.centerx - end_text.get_width() // 2, end_rect.y - 30))
        
        # Attempts counter
        attempts_text = self.font_small.render("Attempts: %d" % self.attempts, True, (100, 100, 100))
        self.screen.blit(attempts_text, (20, 560))
        
        # Progress
        progress = len(self.visited) / len(self.path) * 100
        progress_text = self.font_small.render("Progress: %.0f%%" % progress, True, (100, 100, 100))
        self.screen.blit(progress_text, (850, 560))

    def draw_game_over(self):
        """Draw falling or winning screen"""
        if self.game_state == "falling":
            # Falling message
            fall_text = self.font_large.render("You fell through!", True, (200, 50, 50))
            self.screen.blit(fall_text, (500 - fall_text.get_width() // 2, 480))
            
            restart_text = self.font_small.render("Restarting...", True, (150, 50, 50))
            self.screen.blit(restart_text, (500 - restart_text.get_width() // 2, 540))
        
        elif self.game_state == "won":
            # Overlay
            overlay = pygame.Surface((1000, 600))
            overlay.set_alpha(min(180, self.win_timer * 4))
            overlay.fill((0, 50, 100))
            self.screen.blit(overlay, (0, 0))
            
            if self.win_timer > 20:
                win_text = self.font_large.render("You Made It!", True, (100, 255, 150))
                self.screen.blit(win_text, (500 - win_text.get_width() // 2, 250))
                
                stats_text = self.font_medium.render("Completed in %d attempts" % (self.attempts + 1), True, (200, 255, 220))
                self.screen.blit(stats_text, (500 - stats_text.get_width() // 2, 330))

    def loop(self):
        clock = pygame.time.Clock()
        keep_going = True

        while keep_going:
            clock.tick(60)
            
            # Update hint timer
            self.hint_timer -= 1
            if self.hint_timer <= -self.hint_interval:
                self.hint_timer = self.hint_duration
            
            # Handle falling animation
            if self.game_state == "falling":
                self.fall_timer += 1
                self.fall_offset += 5
                
                if self.fall_timer >= 60:  # 1 second fall animation
                    self.restart_puzzle()
            
            # Handle win state
            if self.game_state == "won":
                self.win_timer += 1
                if self.win_timer >= 180:  # 3 seconds then close
                    keep_going = False
            
            # Get hover tile
            mouse_pos = pygame.mouse.get_pos()
            self.hover_tile = self.get_tile_at_pos(mouse_pos)
            
            # Draw everything
            # Background - icy blue gradient
            for y in range(600):
                ratio = y / 600
                r = int(200 + (180 - 200) * ratio)
                g = int(230 + (220 - 230) * ratio)
                b = int(255 + (250 - 255) * ratio)
                pygame.draw.line(self.screen, (r, g, b), (0, y), (1000, y))
            
            # Draw grid and player
            self.draw_grid()
            self.draw_player()
            self.draw_ui()
            
            # Draw game over states
            if self.game_state in ["falling", "won"]:
                self.draw_game_over()
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keep_going = False
                    break
                
                elif event.type == pygame.MOUSEBUTTONDOWN and self.game_state == "playing":
                    if event.button == 1:  # Left click
                        clicked_tile = self.get_tile_at_pos(event.pos)
                        
                        if clicked_tile and self.is_valid_move(clicked_tile):
                            # Check if it's a safe tile (part of the path)
                            if self.grid[clicked_tile[1]][clicked_tile[0]] == 1:
                                # Safe! Move to this tile
                                self.previous_pos = self.player_pos
                                self.player_pos = clicked_tile
                                self.visited.append(clicked_tile)
                                
                                # Check for win
                                if clicked_tile == self.path[-1]:
                                    self.game_state = "won"
                            else:
                                # Fell through!
                                self.player_pos = clicked_tile
                                self.game_state = "falling"
                                self.fall_timer = 0
                                self.fall_offset = 0

class BlizzardSurvival(Minigame):
    def __init__(self):
        super().__init__()

        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Dodging Game - Survive!")
        
        # Load Tux images
        self.tux_right = pygame.image.load("images/tux-right.png")
        self.tux_left = pygame.image.load("images/tux-left.png")
        self.tux_right = pygame.transform.smoothscale(self.tux_right, (80, 100))
        self.tux_left = pygame.transform.smoothscale(self.tux_left, (80, 100))
        self.current_tux = self.tux_right
        
        # Player properties
        self.player_x = 460
        self.player_y = 480
        self.player_width = 80
        self.player_height = 100
        self.player_speed = 7
        self.player_velocity_x = 0
        self.acceleration = 0.8
        self.friction = 0.85
        
        # Falling balls
        self.falling_balls = []
        self.spawn_timer = 0
        self.base_spawn_delay = 45  # frames between spawns
        self.spawn_delay = self.base_spawn_delay
        
        # Ball types with different properties
        self.ball_types = [
            {'color': (255, 100, 100), 'size': 30, 'speed': 5, 'points': 1},   # Red - normal
            {'color': (100, 100, 255), 'size': 50, 'speed': 3, 'points': 2},   # Blue - big slow
            {'color': (255, 255, 100), 'size': 20, 'speed': 9, 'points': 3},   # Yellow - small fast
            {'color': (150, 50, 200), 'size': 40, 'speed': 6, 'points': 2},    # Purple - medium
            {'color': (255, 150, 50), 'size': 25, 'speed': 7, 'points': 2},    # Orange - fast small
        ]
        
        # Game metrics
        self.score = 0
        self.balls_dodged = 0
        self.game_time = 0
        self.game_over = False
        self.game_over_timer = 0
        
        # Visual effects
        self.screen_shake = 0
        
        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)

        self.loop()

        pygame.quit()

    def spawn_ball(self):
        """Create a new falling ball at the top of the screen"""
        ball_type = random.choice(self.ball_types)
        
        # As time progresses, favor faster ball types (after 15 seconds)
        time_seconds = self.game_time / 60
        if time_seconds > 15 and random.random() < 0.5:
            ball_type = random.choice([b for b in self.ball_types if b['speed'] >= 6])
        
        ball = {
            'x': random.randint(50, 920),
            'y': -50,
            'speed': ball_type['speed'] + random.uniform(-1, 1),
            'size': ball_type['size'],
            'color': ball_type['color'],
            'points': ball_type['points'],
            'rotation': 0,
            'rotation_speed': random.uniform(-5, 5),
            'wobble': random.uniform(0, 6.28),
            'wobble_speed': random.uniform(0.05, 0.15),
            'wobble_amount': random.uniform(0, 2),
            'rect': pygame.Rect(0, 0, ball_type['size'], ball_type['size'])
        }
        self.falling_balls.append(ball)

    def update_balls(self):
        """Update positions of all falling balls"""
        for ball in self.falling_balls[:]:
            ball['y'] += ball['speed']
            ball['rotation'] += ball['rotation_speed']
            ball['wobble'] += ball['wobble_speed']
            ball['x'] += ball['wobble_amount'] * pygame.math.Vector2(1, 0).rotate(ball['wobble'] * 57.3).x
            
            # Update collision rectangle (slightly smaller for fairness)
            shrink = ball['size'] * 0.15
            ball['rect'].x = ball['x'] - ball['size'] // 2 + shrink
            ball['rect'].y = ball['y'] - ball['size'] // 2 + shrink
            ball['rect'].width = ball['size'] - shrink * 2
            ball['rect'].height = ball['size'] - shrink * 2
            
            # Remove balls that have fallen off the screen and count as dodged
            if ball['y'] > 650:
                self.falling_balls.remove(ball)
                self.balls_dodged += 1
                self.score += ball['points']

    def check_collision(self):
        """Check if player collided with any ball"""
        # Player hitbox (slightly smaller for fairness)
        shrink_x = self.player_width * 0.2
        shrink_y = self.player_height * 0.1
        player_rect = pygame.Rect(
            self.player_x + shrink_x,
            self.player_y + shrink_y,
            self.player_width - shrink_x * 2,
            self.player_height - shrink_y * 2
        )
        
        for ball in self.falling_balls:
            if player_rect.colliderect(ball['rect']):
                return ball
        return None

    def draw_player(self):
        """Draw Tux character"""
        # Apply screen shake offset
        shake_x = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        shake_y = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        
        self.screen.blit(self.current_tux, (self.player_x + shake_x, self.player_y + shake_y))

    def draw_balls(self):
        """Draw all falling balls with visual effects"""
        for ball in self.falling_balls:
            # Draw ball with gradient effect
            center_x = int(ball['x'])
            center_y = int(ball['y'])
            
            # Outer glow
            glow_color = tuple(min(255, c + 50) for c in ball['color'])
            pygame.draw.circle(self.screen, glow_color, (center_x, center_y), ball['size'] // 2 + 3)
            
            # Main ball
            pygame.draw.circle(self.screen, ball['color'], (center_x, center_y), ball['size'] // 2)
            
            # Highlight
            highlight_x = center_x - ball['size'] // 6
            highlight_y = center_y - ball['size'] // 6
            highlight_size = ball['size'] // 5
            if highlight_size > 0:
                pygame.draw.circle(self.screen, (255, 255, 255), (highlight_x, highlight_y), highlight_size)

    def draw_ui(self):
        """Draw game UI elements"""
        # Time elapsed display at top
        time_elapsed = self.game_time / 60
        time_text = self.font_large.render("%.1fs" % time_elapsed, True, (255, 255, 255))
        time_bg = pygame.Rect(500 - time_text.get_width() // 2 - 15, 10, time_text.get_width() + 30, 50)
        pygame.draw.rect(self.screen, (0, 0, 0), time_bg, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), time_bg, 3, border_radius=10)
        self.screen.blit(time_text, (500 - time_text.get_width() // 2, 15))
        
        # Score
        score_text = self.font_medium.render("Score: %d" % self.score, True, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (10, 10, score_text.get_width() + 20, 40), border_radius=5)
        self.screen.blit(score_text, (20, 15))
        
        # Balls dodged
        dodged_text = self.font_small.render("Dodged: %d" % self.balls_dodged, True, (200, 200, 200))
        self.screen.blit(dodged_text, (20, 55))
        
        # Instructions at bottom
        if self.game_time < 180:  # Show for first 3 seconds
            alpha = max(0, 255 - (self.game_time - 120) * 4) if self.game_time > 120 else 255
            inst_text = self.font_small.render("Use LEFT/RIGHT arrows to dodge!", True, (255, 255, 255))
            inst_text.set_alpha(alpha)
            self.screen.blit(inst_text, (500 - inst_text.get_width() // 2, 560))

    def draw_game_over(self):
        """Draw game over screen"""
        # Darken background
        overlay = pygame.Surface((1000, 600))
        overlay.set_alpha(min(200, self.game_over_timer * 5))
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        if self.game_over_timer > 20:
            title_text = self.font_large.render("GAME OVER!", True, (255, 100, 100))
            subtitle_text = self.font_medium.render("You got hit!", True, (255, 150, 150))
            
            self.screen.blit(title_text, (500 - title_text.get_width() // 2, 180))
            self.screen.blit(subtitle_text, (500 - subtitle_text.get_width() // 2, 260))
            
            # Stats
            score_text = self.font_medium.render("Final Score: %d" % self.score, True, (255, 255, 255))
            dodged_text = self.font_small.render("Balls Dodged: %d" % self.balls_dodged, True, (200, 200, 200))
            time_text = self.font_small.render("Time Survived: %.1fs" % (self.game_time / 60), True, (200, 200, 200))
            
            self.screen.blit(score_text, (500 - score_text.get_width() // 2, 320))
            self.screen.blit(dodged_text, (500 - dodged_text.get_width() // 2, 380))
            self.screen.blit(time_text, (500 - time_text.get_width() // 2, 420))

    def loop(self):
        clock = pygame.time.Clock()
        keep_going = True

        while keep_going:
            clock.tick(60)
            
            if not self.game_over:
                self.game_time += 1
                self.spawn_timer += 1
                
                # Decrease screen shake
                if self.screen_shake > 0:
                    self.screen_shake -= 1
                
                # Progressive difficulty - gets harder over time
                time_seconds = self.game_time / 60
                
                # Spawn delay decreases over time (more balls spawn)
                # Starts at 45 frames, goes down to 5 frames by 30 seconds
                self.spawn_delay = max(5, int(self.base_spawn_delay - time_seconds * 1.5))
                
                # Spawn new balls
                if self.spawn_timer >= self.spawn_delay:
                    self.spawn_ball()
                    self.spawn_timer = 0
                    
                    # Spawn multiple balls as time progresses
                    if time_seconds > 10 and random.random() < 0.3:
                        self.spawn_ball()
                    if time_seconds > 20 and random.random() < 0.4:
                        self.spawn_ball()
                    if time_seconds > 25 and random.random() < 0.5:
                        self.spawn_ball()

                # Handle player movement with acceleration
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.player_velocity_x -= self.acceleration
                    self.current_tux = self.tux_left
                elif keys[pygame.K_RIGHT]:
                    self.player_velocity_x += self.acceleration
                    self.current_tux = self.tux_right
                
                # Apply friction
                self.player_velocity_x *= self.friction
                
                # Clamp velocity
                self.player_velocity_x = max(-self.player_speed, min(self.player_speed, self.player_velocity_x))
                
                # Update position
                self.player_x += self.player_velocity_x
                self.player_x = max(0, min(920, self.player_x))

                # Update balls
                self.update_balls()

                # Check collision
                hit_ball = self.check_collision()
                if hit_ball:
                    self.game_over = True
                    self.screen_shake = 10
            else:
                self.game_over_timer += 1
                
                # Auto-close after 4 seconds
                if self.game_over_timer >= 240:
                    keep_going = False

            # Draw everything
            # Sky gradient background
            for y in range(600):
                color_ratio = y / 600
                r = int(135 + (100 - 135) * color_ratio)
                g = int(206 + (150 - 206) * color_ratio)
                b = int(235 + (200 - 235) * color_ratio)
                pygame.draw.line(self.screen, (r, g, b), (0, y), (1000, y))
            
            # Ground
            pygame.draw.rect(self.screen, (100, 150, 100), (0, 580, 1000, 20))
            pygame.draw.rect(self.screen, (80, 120, 80), (0, 580, 1000, 5))
            
            # Draw game elements
            self.draw_balls()
            self.draw_balls()
            self.draw_player()
            self.draw_ui()
            
            # Draw game over screen if applicable
            if self.game_over:
                self.draw_game_over()
            
            # Flash effect
            if self.flash_alpha > 0:
                flash_surface = pygame.Surface((1000, 600))
                flash_surface.fill((255, 255, 255))
                flash_surface.set_alpha(self.flash_alpha)
                self.screen.blit(flash_surface, (0, 0))
                self.flash_alpha -= 10
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keep_going = False
                    break

class FishFrenzy(Minigame):
    def __init__(self):
        super().__init__()

        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Fish Frenzy")
        
        # Load fish image
        self.fish_img = pygame.image.load("images/fish.png")
        self.fish_img = pygame.transform.smoothscale(self.fish_img, (250, 250))
        
        # List to store falling fish
        self.falling_fish = []
        self.spawn_timer = 0
        self.spawn_delay = random.randint(20, 150) # frames
        
        # Score counter
        self.score = 0
        self.font = pygame.font.Font(None, 48)

        self.loop()

        pygame.quit()

    def spawn_fish(self):
        """Create a new falling fish at the top of the screen"""
        fish = {
            'x': random.randint(0, 920),
            'y': -80,  # Start above the screen
            'speed': random.randint(3, 8),  # Random falling speed
            'rotation': random.randint(0, 360),  # Random rotation
            'rect': pygame.Rect(0, 0, 250, 250)  # Collision rectangle
        }
        self.falling_fish.append(fish)

    def update_fish(self):
        """Update positions of all falling fish"""
        for fish in self.falling_fish[:]:
            fish['y'] += fish['speed']
            # Update collision rectangle position
            fish['rect'].x = fish['x']
            fish['rect'].y = fish['y']
            # Remove fish that have fallen off the screen
            if fish['y'] > 600:
                self.falling_fish.remove(fish)

    def draw_fish(self):
        """Draw all falling fish"""
        for fish in self.falling_fish:
            # Rotate the fish image
            rotated_fish = pygame.transform.rotate(self.fish_img, fish['rotation'])
            fish_rect = rotated_fish.get_rect(center=(fish['x'] + 125, fish['y'] + 125))
            self.screen.blit(rotated_fish, fish_rect)
    
    def check_fish_click(self, mouse_pos):
        for fish in self.falling_fish[:]:
            if fish['rect'].collidepoint(mouse_pos):
                self.falling_fish.remove(fish)
                self.score += 1
                break

    def loop(self):
        clock = pygame.time.Clock()
        keep_going = True

        while keep_going:
            clock.tick(60)

            # Spawn new fish periodically
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_delay:
                self.spawn_fish()
                self.spawn_timer = 0

            # Update fish positions
            self.update_fish()

            # Clear screen (sky blue background)
            self.screen.fill((135, 206, 235))
            
            # Draw all falling fish
            self.draw_fish()
            
            # Draw score
            score_text = self.font.render("Score: %s" % self.score, True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keep_going = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        self.check_fish_click(event.pos)


IcePuzzle()