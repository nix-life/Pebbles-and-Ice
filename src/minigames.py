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
            DodgingGame()
class IcePuzzle(Minigame):
    def __init__(self):
        super().__init__()

        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Ice Puzzle")

        self.loop()

        pygame.quit()

    def loop(self):
        clock = pygame.time.Clock()
        keep_going = True

        while keep_going:
            clock.tick(60)
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keep_going = False
                    break

class DodgingGame(Minigame):
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
        self.game_duration = 900  # 15 seconds at 60 FPS
        self.game_over = False
        self.game_won = False
        self.game_over_timer = 0
        
        # Visual effects
        self.screen_shake = 0
        self.flash_alpha = 0
        self.combo = 0
        self.combo_timer = 0
        self.particles = []
        
        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)

        self.loop()

        pygame.quit()

    def spawn_ball(self):
        """Create a new falling ball at the top of the screen"""
        ball_type = random.choice(self.ball_types)
        
        # As time progresses, favor faster ball types
        progress = self.game_time / self.game_duration
        if progress > 0.5 and random.random() < 0.4:
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

    def spawn_particle(self, x, y, color):
        """Create particle effects"""
        for _ in range(5):
            particle = {
                'x': x,
                'y': y,
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-5, -1),
                'life': 30,
                'color': color,
                'size': random.randint(3, 8)
            }
            self.particles.append(particle)

    def update_particles(self):
        """Update particle positions and lifetime"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.2  # gravity
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)

    def draw_particles(self):
        """Draw all particles"""
        for particle in self.particles:
            alpha = int((particle['life'] / 30) * 255)
            size = int(particle['size'] * (particle['life'] / 30))
            if size > 0:
                pygame.draw.circle(self.screen, particle['color'], 
                                   (int(particle['x']), int(particle['y'])), size)

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
                self.combo += 1
                self.combo_timer = 60
                # Spawn particles at bottom
                self.spawn_particle(ball['x'], 580, ball['color'])

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
        # Timer bar at top
        bar_width = 800
        bar_height = 25
        bar_x = 100
        bar_y = 20
        progress = max(0, 1 - self.game_time / self.game_duration)
        
        # Background bar
        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=10)
        
        # Progress bar with color gradient based on time
        if progress > 0.5:
            bar_color = (100, 255, 100)
        elif progress > 0.25:
            bar_color = (255, 255, 100)
        else:
            bar_color = (255, 100, 100)
        
        pygame.draw.rect(self.screen, bar_color, 
                         (bar_x, bar_y, int(bar_width * progress), bar_height), border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 3, border_radius=10)
        
        # Time text
        time_remaining = max(0, (self.game_duration - self.game_time) / 60)
        time_text = self.font_medium.render("%.1fs" % time_remaining, True, (255, 255, 255))
        self.screen.blit(time_text, (bar_x + bar_width // 2 - time_text.get_width() // 2, bar_y - 5))
        
        # Score
        score_text = self.font_medium.render("Score: %d" % self.score, True, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0, 150), (10, 55, score_text.get_width() + 20, 40), border_radius=5)
        self.screen.blit(score_text, (20, 60))
        
        # Balls dodged
        dodged_text = self.font_small.render("Dodged: %d" % self.balls_dodged, True, (200, 200, 200))
        self.screen.blit(dodged_text, (20, 100))
        
        # Combo display
        if self.combo >= 3 and self.combo_timer > 0:
            combo_alpha = int((self.combo_timer / 60) * 255)
            combo_text = self.font_medium.render("Combo x%d!" % self.combo, True, (255, 200, 50))
            combo_text.set_alpha(combo_alpha)
            self.screen.blit(combo_text, (500 - combo_text.get_width() // 2, 120))
        
        # Instructions at bottom
        if self.game_time < 180:  # Show for first 3 seconds
            alpha = max(0, 255 - (self.game_time - 120) * 4) if self.game_time > 120 else 255
            inst_text = self.font_small.render("Use LEFT/RIGHT arrows to dodge!", True, (255, 255, 255))
            inst_text.set_alpha(alpha)
            self.screen.blit(inst_text, (500 - inst_text.get_width() // 2, 560))

    def draw_game_over(self):
        """Draw game over or victory screen"""
        # Darken background
        overlay = pygame.Surface((1000, 600))
        overlay.set_alpha(min(200, self.game_over_timer * 5))
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        if self.game_over_timer > 20:
            if self.game_won:
                title_text = self.font_large.render("YOU SURVIVED!", True, (100, 255, 100))
                subtitle_text = self.font_medium.render("Congratulations!", True, (200, 255, 200))
            else:
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
                
                # Decrease combo timer
                if self.combo_timer > 0:
                    self.combo_timer -= 1
                else:
                    self.combo = 0
                
                # Decrease screen shake
                if self.screen_shake > 0:
                    self.screen_shake -= 1
                
                # Increase difficulty over time
                progress = self.game_time / self.game_duration
                self.spawn_delay = max(15, self.base_spawn_delay - int(progress * 25))
                
                # Spawn new balls
                if self.spawn_timer >= self.spawn_delay:
                    self.spawn_ball()
                    self.spawn_timer = 0
                    # Occasionally spawn multiple balls later in the game
                    if progress > 0.6 and random.random() < 0.3:
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

                # Update balls and particles
                self.update_balls()
                self.update_particles()

                # Check collision
                hit_ball = self.check_collision()
                if hit_ball:
                    self.game_over = True
                    self.game_won = False
                    self.screen_shake = 10
                    self.spawn_particle(self.player_x + 40, self.player_y + 50, (255, 0, 0))

                # Check if player survived
                if self.game_time >= self.game_duration:
                    self.game_over = True
                    self.game_won = True
            else:
                self.game_over_timer += 1
                self.update_particles()
                
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
            self.draw_particles()
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


class BlizzardSurvival(Minigame):
    def __init__(self):
        super().__init__()

        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Blizzard Survival")

        self.loop()

        pygame.quit()

    def loop(self):
        clock = pygame.time.Clock()
        keep_going = True

        while keep_going:
            clock.tick(60)
            
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


DodgingGame()