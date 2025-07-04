import pygame
import sys
import random
import os
import math
import time

# --- Constants ---
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10

# Colors
BG_COLOR = (20, 20, 30)  # Darker background
GRID_COLOR = (40, 40, 50)
SNAKE_HEAD = (50, 255, 50)  # Brighter green
SNAKE_BODY = (30, 200, 30)
FOOD_COLOR = (255, 100, 100)  # Brighter red
TEXT_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (120, 120, 120)
PARTICLE_COLOR = (255, 255, 0)  # Yellow particles
GLOW_COLOR = (100, 255, 100)  # Green glow

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

HIGH_SCORE_FILE = "highscore.txt"
OBSTACLE_COUNT = 10

# Particle system
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = 30
        self.max_life = 30
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.vy += 0.1  # Gravity
        
    def draw(self, surface):
        alpha = self.life / self.max_life
        color = (255, int(255 * alpha), int(100 * alpha))
        size = max(1, int(4 * alpha))
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), size)

# Sound manager
class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.create_sounds()
        
    def create_sounds(self):
        # Create simple sound effects using pygame's sound generation
        try:
            # Eating sound (short beep)
            self.sounds['eat'] = self.create_beep(440, 0.1)
            # Game over sound (lower tone)
            self.sounds['game_over'] = self.create_beep(220, 0.5)
            # Background music (simple melody)
            self.sounds['bg_music'] = self.create_melody()
        except:
            # If sound creation fails, create empty sounds
            self.sounds = {'eat': None, 'game_over': None, 'bg_music': None}
    
    def create_beep(self, frequency, duration):
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = []
        for i in range(frames):
            wave = 4096 * math.sin(frequency * 2 * math.pi * i / sample_rate)
            arr.append([int(wave), int(wave)])
        sound = pygame.sndarray.make_sound(pygame.array.array('h', arr))
        return sound
    
    def create_melody(self):
        # Simple background melody
        return self.create_beep(330, 2.0)
    
    def play(self, sound_name):
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play()

particles = []
sound_manager = None
input_buffer = []  # Buffer for input commands

def draw_grid(surface):
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

def draw_snake(surface, snake):
    for idx, pos in enumerate(snake):
        color = SNAKE_HEAD if idx == 0 else SNAKE_BODY
        rect = pygame.Rect(pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        
        # Add glow effect for head
        if idx == 0:
            glow_rect = pygame.Rect(pos[0]*CELL_SIZE-2, pos[1]*CELL_SIZE-2, CELL_SIZE+4, CELL_SIZE+4)
            pygame.draw.rect(surface, GLOW_COLOR, glow_rect)
            pygame.draw.rect(surface, color, rect)
            # Add eyes
            eye1 = (pos[0]*CELL_SIZE + 5, pos[1]*CELL_SIZE + 5)
            eye2 = (pos[0]*CELL_SIZE + 15, pos[1]*CELL_SIZE + 5)
            pygame.draw.circle(surface, (255, 255, 255), eye1, 2)
            pygame.draw.circle(surface, (255, 255, 255), eye2, 2)
            pygame.draw.circle(surface, (0, 0, 0), eye1, 1)
            pygame.draw.circle(surface, (0, 0, 0), eye2, 1)
        else:
            pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, BG_COLOR, rect, 1)

def place_food(snake, obstacles=[]):
    while True:
        pos = (random.randint(0, GRID_WIDTH-1),
               random.randint(0, GRID_HEIGHT-1))
        if pos not in snake and pos not in obstacles:
            return pos

def create_food_particles(x, y):
    """Create particles when food is eaten"""
    for _ in range(8):
        particles.append(Particle(x * CELL_SIZE + CELL_SIZE//2, y * CELL_SIZE + CELL_SIZE//2))

def update_particles():
    """Update all particles"""
    global particles
    particles = [p for p in particles if p.life > 0]
    for particle in particles:
        particle.update()

def draw_particles(surface):
    """Draw all particles"""
    for particle in particles:
        particle.draw(surface)

def is_valid_direction_change(current_direction, new_direction):
    """Check if direction change is valid (not directly opposite)"""
    opposite_directions = {
        UP: DOWN,
        DOWN: UP,
        LEFT: RIGHT,
        RIGHT: LEFT
    }
    return new_direction != opposite_directions.get(current_direction)

def process_input_buffer(current_direction):
    """Process buffered input and return valid direction change"""
    global input_buffer
    
    for buffered_direction in input_buffer:
        if is_valid_direction_change(current_direction, buffered_direction):
            input_buffer.clear()  # Clear buffer after processing
            return buffered_direction
    
    input_buffer.clear()  # Clear invalid inputs
    return current_direction

def load_highscore():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def save_highscore(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

def show_title_screen(surface, font, high_score):
    surface.fill(BG_COLOR)
    
    # Animated title with glow effect
    title_color = (50 + int(50 * math.sin(time.time() * 3)), 255, 50)
    title = font.render("🐍 SNAKE GAME 🐍", True, title_color)
    
    hs_text = font.render(f"🏆 High Score: {high_score}", True, TEXT_COLOR)
    instr = font.render("Press any key to start", True, TEXT_COLOR)
    controls = font.render("Use arrow keys to move", True, (150, 150, 150))
    
    surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//3))
    surface.blit(hs_text, (SCREEN_WIDTH//2 - hs_text.get_width()//2, SCREEN_HEIGHT//3 + 50))
    surface.blit(instr, (SCREEN_WIDTH//2 - instr.get_width()//2, SCREEN_HEIGHT//3 + 90))
    surface.blit(controls, (SCREEN_WIDTH//2 - controls.get_width()//2, SCREEN_HEIGHT//3 + 130))
    
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif e.type == pygame.KEYDOWN:
                return

def generate_obstacles(snake, food):
    obs = []
    while len(obs) < OBSTACLE_COUNT:
        pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        if pos not in snake and pos != food and pos not in obs:
            obs.append(pos)
    return obs

def draw_obstacles(surface, obstacles):
    for pos in obstacles:
        rect = pygame.Rect(pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        # Add 3D effect to obstacles
        pygame.draw.rect(surface, OBSTACLE_COLOR, rect)
        pygame.draw.rect(surface, (150, 150, 150), rect, 2)
        # Add inner highlight
        inner_rect = pygame.Rect(pos[0]*CELL_SIZE+2, pos[1]*CELL_SIZE+2, CELL_SIZE-4, CELL_SIZE-4)
        pygame.draw.rect(surface, (80, 80, 80), inner_rect)

def draw_food_with_glow(surface, food_pos):
    """Draw food with pulsing glow effect"""
    glow_intensity = 0.5 + 0.5 * math.sin(time.time() * 5)
    
    # Draw glow
    glow_size = int(CELL_SIZE + 6 * glow_intensity)
    glow_rect = pygame.Rect(
        food_pos[0]*CELL_SIZE - (glow_size-CELL_SIZE)//2,
        food_pos[1]*CELL_SIZE - (glow_size-CELL_SIZE)//2,
        glow_size, glow_size
    )
    glow_color = (int(255 * glow_intensity), int(50 * glow_intensity), int(50 * glow_intensity))
    pygame.draw.rect(surface, glow_color, glow_rect)
    
    # Draw food
    food_rect = pygame.Rect(food_pos[0]*CELL_SIZE, food_pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, FOOD_COLOR, food_rect)
    # Add shine effect
    shine_rect = pygame.Rect(food_pos[0]*CELL_SIZE+2, food_pos[1]*CELL_SIZE+2, CELL_SIZE//3, CELL_SIZE//3)
    pygame.draw.rect(surface, (255, 200, 200), shine_rect)

def main():
    global sound_manager, input_buffer
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 24)
    pygame.display.set_caption("🐍 Enhanced Snake Game")
    
    # Initialize sound
    sound_manager = SoundManager()

    snake = [(GRID_WIDTH//2, GRID_HEIGHT//2),
             (GRID_WIDTH//2-1, GRID_HEIGHT//2),
             (GRID_WIDTH//2-2, GRID_HEIGHT//2)]
    direction = RIGHT
    food = place_food(snake)
    score = 0
    high_score = load_highscore()
    show_title_screen(screen, font, high_score)
    obstacles = generate_obstacles(snake, food)
    
    # Clear input buffer at start
    input_buffer.clear()

    while True:
        # Event handling
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                # Buffer input instead of changing direction immediately
                if e.key == pygame.K_UP:
                    input_buffer.append(UP)
                elif e.key == pygame.K_DOWN:
                    input_buffer.append(DOWN)
                elif e.key == pygame.K_LEFT:
                    input_buffer.append(LEFT)
                elif e.key == pygame.K_RIGHT:
                    input_buffer.append(RIGHT)
                
                # Keep only the latest input if buffer gets too long
                if len(input_buffer) > 2:
                    input_buffer = input_buffer[-2:]

        # Process buffered input and update direction
        direction = process_input_buffer(direction)

        # Move snake
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        head = (head[0] % GRID_WIDTH, head[1] % GRID_HEIGHT)

        if head in snake or head in obstacles:
            sound_manager.play('game_over')
            break

        snake.insert(0, head)
        if head == food:
            score += 1
            sound_manager.play('eat')
            create_food_particles(food[0], food[1])
            food = place_food(snake, obstacles)
            obstacles = generate_obstacles(snake, food)
        else:
            snake.pop()

        # Update particles
        update_particles()

        # Draw
        screen.fill(BG_COLOR)
        draw_grid(screen)
        draw_snake(screen, snake)
        draw_obstacles(screen, obstacles)
        
        # Draw food with glow
        draw_food_with_glow(screen, food)
        
        # Draw particles
        draw_particles(screen)

        # Draw score with better styling
        score_surf = font.render(f"Score: {score}", True, TEXT_COLOR)
        level_surf = small_font.render(f"Level: {score // 5 + 1}", True, (200, 200, 200))
        speed_surf = small_font.render(f"Speed: {FPS + score // 5}", True, (200, 200, 200))
        
        screen.blit(score_surf, (10, 10))
        screen.blit(level_surf, (10, 50))
        screen.blit(speed_surf, (10, 75))

        pygame.display.flip()
        clock.tick(FPS + score // 5)

    # Game over screen with better visuals
    if score > high_score:
        save_highscore(score)
        high_score = score
    
    # Game over screen
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    screen.blit(overlay, (0, 0))
    
    game_over = font.render("💀 GAME OVER! 💀", True, (255, 100, 100))
    final_score = font.render(f"Final Score: {score}", True, TEXT_COLOR)
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 0))
    restart_text = font.render("Press R to restart or Q to quit", True, TEXT_COLOR)
    
    screen.blit(game_over, (SCREEN_WIDTH//2 - game_over.get_width()//2, SCREEN_HEIGHT//2 - 60))
    screen.blit(final_score, (SCREEN_WIDTH//2 - final_score.get_width()//2, SCREEN_HEIGHT//2 - 20))
    screen.blit(high_score_text, (SCREEN_WIDTH//2 - high_score_text.get_width()//2, SCREEN_HEIGHT//2 + 10))
    screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
    
    pygame.display.flip()
    
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    main()
                elif e.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()