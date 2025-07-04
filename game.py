import pygame
import sys
import random
import os
import math
import time
import numpy as np
from scipy import signal
try:
    from noise import pnoise1
    NOISE_AVAILABLE = True
except ImportError:
    NOISE_AVAILABLE = False

# --- Constants ---
CELL_SIZE = 20
GRID_WIDTH = 35
GRID_HEIGHT = 25
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 60  # Increased for smoother animation
GAME_SPEED = 8  # Separate game logic speed

# Colors with alpha support
BG_COLOR = (15, 15, 25)  # Darker background
GRID_COLOR = (35, 35, 45)
SNAKE_HEAD = (100, 255, 100)  # Brighter green
SNAKE_BODY = (60, 200, 60)
FOOD_COLOR = (255, 120, 120)  # Brighter red
TEXT_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (140, 140, 140)
PARTICLE_COLOR = (255, 255, 100)  # Yellow particles
GLOW_COLOR = (150, 255, 150)  # Green glow
TRAIL_COLOR = (50, 150, 50)  # Snake trail

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

HIGH_SCORE_FILE = "highscore.txt"
OBSTACLE_COUNT = 10

# UNFAIR GAME MECHANICS
UNFAIR_MODE = True
FAKE_FOOD_CHANCE = 0.15  # 15% chance food is fake
TELEPORT_OBSTACLES_CHANCE = 0.1  # 10% chance obstacles teleport
INVISIBLE_SNAKE_CHANCE = 0.08  # 8% chance snake becomes invisible
SPEED_BOOST_TRAP_CHANCE = 0.1  # 10% chance food gives unwanted speed boost
FAKE_WALLS_CHANCE = 0.05  # 5% chance fake walls appear
FOG_OF_WAR_CHANCE = 0.06  # 6% chance fog of war activates
FOG_VISION_RADIUS = 4  # How many cells visible around snake head

# Enhanced Particle system
class EnhancedParticle:
    def __init__(self, x, y, particle_type="food"):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        
        if particle_type == "food":
            self.vx = random.uniform(-4, 4)
            self.vy = random.uniform(-6, -2)
            self.life = 40
            self.color_base = (255, 255, 100)
        elif particle_type == "explosion":
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
            self.life = 30
            self.color_base = (255, 50, 50)
        elif particle_type == "trail":
            self.vx = random.uniform(-1, 1)
            self.vy = random.uniform(-1, 1)
            self.life = 20
            self.color_base = TRAIL_COLOR
            
        self.max_life = self.life
        self.gravity = 0.15
        self.bounce = 0.7
        self.particle_type = particle_type
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        
        # Add gravity for food particles
        if self.particle_type == "food":
            self.vy += self.gravity
            
            # Bounce off ground
            if self.y > SCREEN_HEIGHT - 5:
                self.y = SCREEN_HEIGHT - 5
                self.vy *= -self.bounce
                self.vx *= 0.9  # Friction
        
        # Noise-based movement for trail particles
        if self.particle_type == "trail" and NOISE_AVAILABLE:
            noise_x = pnoise1((time.time() + self.start_x) * 0.01) * 0.5
            noise_y = pnoise1((time.time() + self.start_y) * 0.01) * 0.5
            self.vx += noise_x
            self.vy += noise_y
            
    def draw(self, surface):
        alpha = max(0, self.life / self.max_life)
        
        if self.particle_type == "food":
            # Rainbow effect
            hue = (time.time() * 50 + self.start_x + self.start_y) % 360
            color = self.hsv_to_rgb(hue, 0.8, alpha)
            size = max(1, int(6 * alpha))
        elif self.particle_type == "explosion":
            color = (int(self.color_base[0] * alpha), 
                    int(self.color_base[1] * alpha), 
                    int(self.color_base[2] * alpha))
            size = max(1, int(4 * alpha))
        else:  # trail
            color = (int(self.color_base[0] * alpha * 0.5), 
                    int(self.color_base[1] * alpha * 0.5), 
                    int(self.color_base[2] * alpha * 0.5))
            size = max(1, int(3 * alpha))
            
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), size)
        
        # Add glow effect
        if alpha > 0.5:
            glow_size = size + 2
            glow_alpha = alpha * 0.3
            glow_color = (int(color[0] * glow_alpha), 
                         int(color[1] * glow_alpha), 
                         int(color[2] * glow_alpha))
            pygame.draw.circle(surface, glow_color, (int(self.x), int(self.y)), glow_size)
    
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB color space"""
        h = h % 360
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
            
        return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))

# Enhanced Sound manager with better synthesis
class EnhancedSoundManager:
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        self.sounds = {}
        self.music_channel = None
        self.create_sounds()
        
    def create_sounds(self):
        try:
            # Create more sophisticated sound effects
            self.sounds['eat'] = self.create_chord([440, 554, 659], 0.15)  # C major chord
            self.sounds['game_over'] = self.create_sweep(440, 220, 0.8)  # Descending sweep
            self.sounds['level_up'] = self.create_chord([523, 659, 784], 0.3)  # C major higher
            self.sounds['move'] = self.create_click(0.05)  # Subtle move sound
            self.sounds['bg_music'] = self.create_ambient_loop()
        except Exception as e:
            print(f"Sound creation failed: {e}")
            # Create silent sounds as fallback
            self.sounds = {name: None for name in ['eat', 'game_over', 'level_up', 'move', 'bg_music']}
    
    def create_chord(self, frequencies, duration):
        """Create a chord with multiple frequencies"""
        sample_rate = 44100
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for freq in frequencies:
            # Create wave with envelope
            t = np.linspace(0, duration, frames)
            wave = np.sin(freq * 2 * np.pi * t)
            
            # Apply ADSR envelope (Attack, Decay, Sustain, Release)
            envelope = self.create_envelope(frames, attack=0.1, decay=0.2, sustain=0.7, release=0.3)
            wave *= envelope
            
            # Add to stereo channels
            arr[:, 0] += wave * 0.3  # Left channel
            arr[:, 1] += wave * 0.3  # Right channel
        
        # Convert to pygame sound
        arr = np.clip(arr * 16384, -32767, 32767).astype(np.int16)
        return pygame.sndarray.make_sound(arr)
    
    def create_sweep(self, start_freq, end_freq, duration):
        """Create a frequency sweep"""
        sample_rate = 44100
        frames = int(duration * sample_rate)
        t = np.linspace(0, duration, frames)
        
        # Linear frequency sweep
        freq_sweep = np.linspace(start_freq, end_freq, frames)
        phase = np.cumsum(freq_sweep) * 2 * np.pi / sample_rate
        wave = np.sin(phase)
        
        # Apply envelope
        envelope = self.create_envelope(frames, attack=0.1, decay=0.1, sustain=0.6, release=0.3)
        wave *= envelope
        
        # Convert to stereo
        arr = np.column_stack([wave, wave]) * 0.3
        arr = np.clip(arr * 16384, -32767, 32767).astype(np.int16)
        return pygame.sndarray.make_sound(arr)
    
    def create_click(self, duration):
        """Create a subtle click sound"""
        sample_rate = 44100
        frames = int(duration * sample_rate)
        
        # White noise burst with quick envelope
        noise = np.random.normal(0, 0.1, frames)
        envelope = np.exp(-10 * np.linspace(0, 1, frames))
        wave = noise * envelope
        
        arr = np.column_stack([wave, wave])
        arr = np.clip(arr * 16384, -32767, 32767).astype(np.int16)
        return pygame.sndarray.make_sound(arr)
    
    def create_ambient_loop(self):
        """Create ambient background music"""
        sample_rate = 44100
        duration = 4.0  # 4 second loop
        frames = int(duration * sample_rate)
        t = np.linspace(0, duration, frames)
        
        # Create ambient pad with multiple sine waves
        frequencies = [65.4, 82.4, 98.0, 130.8]  # C2, E2, G2, C3
        wave = np.zeros(frames)
        
        for i, freq in enumerate(frequencies):
            # Add slight detuning and phase offset
            detune = 1 + (i * 0.001)
            phase_offset = i * 0.5
            sine_wave = np.sin((freq * detune) * 2 * np.pi * t + phase_offset)
            
            # Apply slow LFO (Low Frequency Oscillator)
            lfo = np.sin(0.3 * 2 * np.pi * t) * 0.1 + 0.9
            sine_wave *= lfo
            
            wave += sine_wave * (0.8 / len(frequencies))
        
        # Apply gentle envelope to avoid clicks
        fade_samples = int(0.1 * sample_rate)
        wave[:fade_samples] *= np.linspace(0, 1, fade_samples)
        wave[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        arr = np.column_stack([wave, wave]) * 0.15
        arr = np.clip(arr * 16384, -32767, 32767).astype(np.int16)
        return pygame.sndarray.make_sound(arr)
    
    def create_envelope(self, frames, attack=0.1, decay=0.2, sustain=0.7, release=0.3):
        """Create ADSR envelope"""
        envelope = np.ones(frames)
        
        attack_frames = int(attack * frames)
        decay_frames = int(decay * frames)
        release_frames = int(release * frames)
        sustain_frames = frames - attack_frames - decay_frames - release_frames
        
        if attack_frames > 0:
            envelope[:attack_frames] = np.linspace(0, 1, attack_frames)
        
        if decay_frames > 0:
            start_idx = attack_frames
            end_idx = start_idx + decay_frames
            envelope[start_idx:end_idx] = np.linspace(1, sustain, decay_frames)
        
        if sustain_frames > 0:
            start_idx = attack_frames + decay_frames
            end_idx = start_idx + sustain_frames
            envelope[start_idx:end_idx] = sustain
        
        if release_frames > 0:
            envelope[-release_frames:] = np.linspace(sustain, 0, release_frames)
        
        return envelope
    
    def play(self, sound_name, volume=1.0):
        if sound_name in self.sounds and self.sounds[sound_name]:
            sound = self.sounds[sound_name]
            sound.set_volume(volume)
            sound.play()
    
    def play_background_music(self, loop=True):
        if self.sounds['bg_music']:
            if loop:
                self.music_channel = self.sounds['bg_music'].play(-1)  # Loop indefinitely
            else:
                self.music_channel = self.sounds['bg_music'].play()
    
    def stop_background_music(self):
        if self.music_channel:
            self.music_channel.stop()

particles = []
sound_manager = None
input_buffer = []  # Buffer for input commands
game_timer = 0  # For smooth game logic timing
trail_particles = []  # Snake trail particles

# Smooth movement interpolation
class SmoothSnake:
    def __init__(self, initial_positions):
        self.positions = initial_positions.copy()
        self.target_positions = initial_positions.copy()
        self.interpolation_progress = 1.0
        
    def update_targets(self, new_positions):
        self.positions = self.target_positions.copy()
        self.target_positions = new_positions.copy()
        self.interpolation_progress = 0.0
        
    def get_interpolated_positions(self, dt):
        if self.interpolation_progress >= 1.0:
            return self.target_positions
        
        # Smooth interpolation using easing
        self.interpolation_progress = min(1.0, self.interpolation_progress + dt * 8.0)
        t = self.ease_out_cubic(self.interpolation_progress)
        
        interpolated = []
        for i, (current, target) in enumerate(zip(self.positions, self.target_positions)):
            if i == 0:  # Head gets special treatment
                x = current[0] + (target[0] - current[0]) * t
                y = current[1] + (target[1] - current[1]) * t
                interpolated.append((x, y))
            else:
                interpolated.append(target)  # Body follows instantly
        
        return interpolated
    
    def ease_out_cubic(self, t):
        return 1 - pow(1 - t, 3)

def draw_grid(surface):
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

def draw_snake_smooth(surface, snake_positions):
    """Draw snake with smooth interpolated positions"""
    for idx, pos in enumerate(snake_positions):
        color = SNAKE_HEAD if idx == 0 else SNAKE_BODY
        
        # Convert float positions to pixel coordinates
        pixel_x = pos[0] * CELL_SIZE
        pixel_y = pos[1] * CELL_SIZE
        
        rect = pygame.Rect(pixel_x, pixel_y, CELL_SIZE, CELL_SIZE)
        
        # Add glow effect for head
        if idx == 0:
            # Pulsing glow effect
            glow_intensity = 0.7 + 0.3 * math.sin(time.time() * 8)
            glow_size = int(4 * glow_intensity)
            glow_rect = pygame.Rect(pixel_x - glow_size, pixel_y - glow_size, 
                                  CELL_SIZE + 2*glow_size, CELL_SIZE + 2*glow_size)
            glow_color = (int(GLOW_COLOR[0] * glow_intensity), 
                         int(GLOW_COLOR[1] * glow_intensity), 
                         int(GLOW_COLOR[2] * glow_intensity))
            pygame.draw.rect(surface, glow_color, glow_rect)
            
            # Head with gradient effect
            pygame.draw.rect(surface, color, rect)
            
            # Enhanced eyes with direction awareness
            eye_offset = 5
            if idx < len(snake_positions) - 1:
                # Determine eye direction based on movement
                next_pos = snake_positions[min(idx + 1, len(snake_positions) - 1)]
                dx = pos[0] - next_pos[0]
                dy = pos[1] - next_pos[1]
                
                if abs(dx) > abs(dy):  # Moving horizontally
                    eye1 = (pixel_x + eye_offset, pixel_y + 5)
                    eye2 = (pixel_x + eye_offset, pixel_y + 15)
                else:  # Moving vertically
                    eye1 = (pixel_x + 5, pixel_y + eye_offset)
                    eye2 = (pixel_x + 15, pixel_y + eye_offset)
            else:
                eye1 = (pixel_x + 5, pixel_y + 5)
                eye2 = (pixel_x + 15, pixel_y + 5)
            
            pygame.draw.circle(surface, (255, 255, 255), eye1, 3)
            pygame.draw.circle(surface, (255, 255, 255), eye2, 3)
            pygame.draw.circle(surface, (0, 0, 0), eye1, 2)
            pygame.draw.circle(surface, (0, 0, 0), eye2, 2)
            
            # Add highlight to eyes
            pygame.draw.circle(surface, (255, 255, 255), (eye1[0]-1, eye1[1]-1), 1)
            pygame.draw.circle(surface, (255, 255, 255), (eye2[0]-1, eye2[1]-1), 1)
        else:
            # Body segments with slight variations
            body_color = (color[0] + random.randint(-10, 10), 
                         color[1] + random.randint(-10, 10), 
                         color[2] + random.randint(-10, 10))
            body_color = tuple(max(0, min(255, c)) for c in body_color)
            pygame.draw.rect(surface, body_color, rect)
            
        # Add border for definition
        pygame.draw.rect(surface, BG_COLOR, rect, 1)

def draw_enhanced_ui(surface, font, small_font, score, level, speed, high_score):
    """Draw enhanced UI with animations and effects"""
    # Animated score with scaling effect
    score_scale = 1.0 + 0.1 * math.sin(time.time() * 4)
    scaled_font_size = int(36 * score_scale)
    dynamic_font = pygame.font.SysFont(None, scaled_font_size)
    
    # Score with glow effect
    score_surf = dynamic_font.render(f"Score: {score}", True, TEXT_COLOR)
    score_glow = dynamic_font.render(f"Score: {score}", True, (100, 255, 100))
    
    # Draw glow first
    surface.blit(score_glow, (12, 12))
    surface.blit(score_surf, (10, 10))
    
    # Level indicator with color coding
    level_color = (255, 200 + min(55, level * 5), 100)
    level_surf = small_font.render(f"Level: {level}", True, level_color)
    surface.blit(level_surf, (10, 50))
    
    # Speed indicator
    speed_color = (200, 200, 255)
    speed_surf = small_font.render(f"Speed: {speed:.1f}", True, speed_color)
    surface.blit(speed_surf, (10, 75))
    
    # High score
    hs_surf = small_font.render(f"High Score: {high_score}", True, (255, 255, 100))
    surface.blit(hs_surf, (10, 100))
    
    # Add progress bar for next level
    next_level_progress = (score % 5) / 5.0
    bar_width = 100
    bar_height = 5
    bar_x = 10
    bar_y = 125
    
    # Background bar
    pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
    # Progress bar
    progress_width = int(bar_width * next_level_progress)
    pygame.draw.rect(surface, (100, 255, 100), (bar_x, bar_y, progress_width, bar_height))
    
    # Progress text
    progress_text = small_font.render("Next Level", True, (150, 150, 150))
    surface.blit(progress_text, (bar_x, bar_y + 10))

def place_food(snake, obstacles=[]):
    while True:
        pos = (random.randint(0, GRID_WIDTH-1),
               random.randint(0, GRID_HEIGHT-1))
        if pos not in snake and pos not in obstacles:
            # Mark if this food is fake (unfair mechanic)
            is_fake = UNFAIR_MODE and random.random() < FAKE_FOOD_CHANCE
            return pos, is_fake

def create_food_particles(x, y):
    """Create particles when food is eaten"""
    for _ in range(12):
        particles.append(EnhancedParticle(x * CELL_SIZE + CELL_SIZE//2, y * CELL_SIZE + CELL_SIZE//2, "food"))

def create_explosion_particles(x, y):
    """Create explosion particles when game over"""
    for _ in range(20):
        particles.append(EnhancedParticle(x * CELL_SIZE + CELL_SIZE//2, y * CELL_SIZE + CELL_SIZE//2, "explosion"))

def create_trail_particle(x, y):
    """Create trail particles behind snake"""
    if random.random() < 0.3:  # 30% chance
        trail_particles.append(EnhancedParticle(x * CELL_SIZE + CELL_SIZE//2, y * CELL_SIZE + CELL_SIZE//2, "trail"))

def update_particles():
    """Update all particles"""
    global particles, trail_particles
    particles = [p for p in particles if p.life > 0]
    trail_particles = [p for p in trail_particles if p.life > 0]
    
    for particle in particles:
        particle.update()
    for particle in trail_particles:
        particle.update()

def draw_particles(surface):
    """Draw all particles"""
    for particle in trail_particles:
        particle.draw(surface)
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
    title = font.render("🐍 UNFAIR SNAKE GAME �", True, title_color)
    
    warning_color = (255, 50, 50) if time.time() % 0.5 < 0.25 else (255, 150, 150)
    warning = font.render("⚠️ WARNING: THIS GAME CHEATS! ⚠️", True, warning_color)
    
    hs_text = font.render(f"🏆 High Score: {high_score}", True, TEXT_COLOR)
    instr = font.render("Press any key to start (good luck!)", True, TEXT_COLOR)
    controls = font.render("Arrow keys to move (when they work properly)", True, (150, 150, 150))
    disclaimer = font.render("Expect: Fake food, teleporting walls, invisible snake, fog of war...", True, (200, 100, 100))
    
    surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//3 - 30))
    surface.blit(warning, (SCREEN_WIDTH//2 - warning.get_width()//2, SCREEN_HEIGHT//3))
    surface.blit(hs_text, (SCREEN_WIDTH//2 - hs_text.get_width()//2, SCREEN_HEIGHT//3 + 40))
    surface.blit(instr, (SCREEN_WIDTH//2 - instr.get_width()//2, SCREEN_HEIGHT//3 + 80))
    surface.blit(controls, (SCREEN_WIDTH//2 - controls.get_width()//2, SCREEN_HEIGHT//3 + 110))
    surface.blit(disclaimer, (SCREEN_WIDTH//2 - disclaimer.get_width()//2, SCREEN_HEIGHT//3 + 140))
    
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif e.type == pygame.KEYDOWN:
                return

def generate_obstacles(snake, food_pos):
    obs = []
    while len(obs) < OBSTACLE_COUNT:
        pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        if pos not in snake and pos != food_pos and pos not in obs:
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

def draw_food_with_glow(surface, food_pos, is_fake=False):
    """Draw food with pulsing glow effect - fake food looks suspicious"""
    if is_fake:
        # Fake food flickers and has a different color
        glow_intensity = 0.3 + 0.7 * abs(math.sin(time.time() * 15))  # Faster flicker
        base_color = (255, 150, 50)  # Orange-ish
    else:
        glow_intensity = 0.5 + 0.5 * math.sin(time.time() * 5)
        base_color = FOOD_COLOR
    
    # Draw glow
    glow_size = int(CELL_SIZE + 6 * glow_intensity)
    glow_rect = pygame.Rect(
        food_pos[0]*CELL_SIZE - (glow_size-CELL_SIZE)//2,
        food_pos[1]*CELL_SIZE - (glow_size-CELL_SIZE)//2,
        glow_size, glow_size
    )
    glow_color = (int(base_color[0] * glow_intensity * 0.5), 
                  int(base_color[1] * glow_intensity * 0.2), 
                  int(base_color[2] * glow_intensity * 0.2))
    pygame.draw.rect(surface, glow_color, glow_rect)
    
    # Draw food
    food_rect = pygame.Rect(food_pos[0]*CELL_SIZE, food_pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, base_color, food_rect)
    
    # Add shine effect
    if is_fake:
        # Fake food has an ominous dark spot
        shine_rect = pygame.Rect(food_pos[0]*CELL_SIZE+6, food_pos[1]*CELL_SIZE+6, CELL_SIZE//4, CELL_SIZE//4)
        pygame.draw.rect(surface, (100, 50, 50), shine_rect)
    else:
        shine_rect = pygame.Rect(food_pos[0]*CELL_SIZE+2, food_pos[1]*CELL_SIZE+2, CELL_SIZE//3, CELL_SIZE//3)
        pygame.draw.rect(surface, (255, 200, 200), shine_rect)

def apply_unfair_mechanics(snake_positions, obstacles):
    """Apply various unfair mechanics"""
    global particles
    
    # Teleport obstacles randomly
    if UNFAIR_MODE and random.random() < TELEPORT_OBSTACLES_CHANCE:
        for i in range(len(obstacles)):
            new_pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            if new_pos not in snake_positions:
                # Create teleport particles at old position
                create_explosion_particles(obstacles[i][0], obstacles[i][1])
                obstacles[i] = new_pos
                # Create teleport particles at new position
                create_explosion_particles(new_pos[0], new_pos[1])

def draw_unfair_warnings(surface, small_font, invisible_snake, speed_boost_active, fog_of_war):
    """Draw warnings about active unfair mechanics"""
    warnings = []
    if invisible_snake > 0:
        warnings.append("SNAKE INVISIBLE!")
    if speed_boost_active > 0:
        warnings.append("SPEED TRAP ACTIVE!")
    if fog_of_war > 0:
        warnings.append("FOG OF WAR ACTIVE!")
    
    for i, warning in enumerate(warnings):
        color = (255, 50, 50) if time.time() % 0.5 < 0.25 else (255, 150, 150)  # Flashing red
        warning_surf = small_font.render(warning, True, color)
        surface.blit(warning_surf, (SCREEN_WIDTH - warning_surf.get_width() - 10, 10 + i * 25))

def process_input_buffer(current_direction):
    """Process buffered input"""
    global input_buffer
    
    for buffered_direction in input_buffer:
        if is_valid_direction_change(current_direction, buffered_direction):
            input_buffer.clear()
            return buffered_direction
    
    input_buffer.clear()
    return current_direction

def draw_snake_unfair(surface, snake_positions, invisible_snake):
    """Draw snake with potential invisibility"""
    if invisible_snake > 0:
        # Snake is partially invisible but more visible than before
        alpha = max(0.1, 0.2 * abs(math.sin(time.time() * 8)))  # Flickering visibility (10% to 30%)
        for idx, pos in enumerate(snake_positions):
            color = SNAKE_HEAD if idx == 0 else SNAKE_BODY
            # Make it translucent but still visible
            faint_color = tuple(int(c * alpha) for c in color)
            rect = pygame.Rect(pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, faint_color, rect)
            
            # Add a flickering outline to help visibility
            if alpha > 0.5:
                outline_color = tuple(int(c * 0.8) for c in color)
                pygame.draw.rect(surface, outline_color, rect, 2)
    else:
        # Normal snake drawing but call the smooth version
        draw_snake_smooth(surface, snake_positions)

def create_fake_walls(snake_positions, food_pos):
    """Create fake walls that look real but aren't"""
    fake_walls = []
    if UNFAIR_MODE and random.random() < FAKE_WALLS_CHANCE:
        for _ in range(3):  # Create 3 fake walls
            pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            if pos not in snake_positions and pos != food_pos:
                fake_walls.append(pos)
    return fake_walls

def draw_fake_walls(surface, fake_walls):
    """Draw fake walls that look like real obstacles"""
    for pos in fake_walls:
        rect = pygame.Rect(pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        # Make them look slightly different (more transparent)
        fake_color = (100, 100, 100)  # Slightly different gray
        pygame.draw.rect(surface, fake_color, rect)
        pygame.draw.rect(surface, (120, 120, 120), rect, 2)
        # Add a subtle "fake" indicator - very small dot
        pygame.draw.circle(surface, (150, 0, 0), (pos[0]*CELL_SIZE + CELL_SIZE//2, pos[1]*CELL_SIZE + CELL_SIZE//2), 1)

def draw_fog_of_war(surface, snake_head_pos, fog_active):
    """Draw fog of war that only shows area around snake head"""
    if fog_active <= 0:
        return
    
    # Create a black overlay for the entire screen
    fog_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fog_overlay.fill((0, 0, 0))
    
    # Create circular visibility around snake head
    head_pixel_x = int(snake_head_pos[0] * CELL_SIZE + CELL_SIZE // 2)
    head_pixel_y = int(snake_head_pos[1] * CELL_SIZE + CELL_SIZE // 2)
    
    # Draw visible area as a circle
    vision_radius_pixels = FOG_VISION_RADIUS * CELL_SIZE
    
    # Create a mask for the visible area
    mask = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    mask.fill((255, 255, 255))
    
    # Draw black circle to make area transparent
    pygame.draw.circle(mask, (0, 0, 0), (head_pixel_x, head_pixel_y), vision_radius_pixels)
    
    # Apply alpha to make fog semi-transparent for dramatic effect
    fog_intensity = 0.8 + 0.2 * abs(math.sin(time.time() * 2))  # Pulsing fog
    fog_overlay.set_alpha(int(255 * fog_intensity))
    
    # Use the mask to create the fog effect
    fog_overlay.blit(mask, (0, 0), special_flags=pygame.BLEND_MULT)
    
    # Draw the fog overlay on the main surface
    surface.blit(fog_overlay, (0, 0))

# ...existing code...
def main():
    global sound_manager, input_buffer, game_timer
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 24)
    pygame.display.set_caption("🐍 UNFAIR Snake Game - Prepare to Rage! 😈")
    
    # Initialize enhanced sound
    sound_manager = EnhancedSoundManager()

    snake_positions = [(GRID_WIDTH//2, GRID_HEIGHT//2),
                      (GRID_WIDTH//2-1, GRID_HEIGHT//2),
                      (GRID_WIDTH//2-2, GRID_HEIGHT//2)]
    smooth_snake = SmoothSnake(snake_positions)
    direction = RIGHT
    food_pos, is_fake_food = place_food(snake_positions)
    score = 0
    level = 1
    high_score = load_highscore()
    show_title_screen(screen, font, high_score)
    obstacles = generate_obstacles(snake_positions, food_pos)
    
    # Unfair game state variables
    invisible_snake = 0
    speed_boost_active = 0
    fog_of_war = 0
    fake_walls = []
    
    # Start background music
    sound_manager.play_background_music()
    
    # Clear input buffer at start
    input_buffer.clear()
    game_timer = 0
    last_move_time = 0
    last_unfair_check = 0

    while True:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
        game_timer += dt
        
        # Apply unfair mechanics every few seconds
        if game_timer - last_unfair_check > 2.0:  # Check every 2 seconds
            last_unfair_check = game_timer
            apply_unfair_mechanics(snake_positions, obstacles)
            
            # Invisible snake chance
            if UNFAIR_MODE and random.random() < INVISIBLE_SNAKE_CHANCE:
                invisible_snake = 180  # 3 seconds at 60fps
            
            # Fog of war chance
            if UNFAIR_MODE and random.random() < FOG_OF_WAR_CHANCE:
                fog_of_war = 240  # 4 seconds at 60fps
            
            # Create fake walls
            if len(fake_walls) == 0:  # Only if no fake walls exist
                fake_walls = create_fake_walls(snake_positions, food_pos)
        
        # Decrease unfair effect timers
        invisible_snake = max(0, invisible_snake - 1)
        speed_boost_active = max(0, speed_boost_active - 1)
        fog_of_war = max(0, fog_of_war - 1)
        
        # Event handling
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sound_manager.stop_background_music()
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

        # Process buffered input
        direction = process_input_buffer(direction)

        # Game logic timing (affected by speed boost trap and fog of war)
        speed_multiplier = 2.0 if speed_boost_active > 0 else 1.0
        fog_multiplier = 0.6 if fog_of_war > 0 else 1.0  # Slower during fog
        current_speed = (GAME_SPEED + score // 3) * speed_multiplier * fog_multiplier
        move_interval = 1.0 / current_speed
        
        if game_timer - last_move_time >= move_interval:
            last_move_time = game_timer
            
            # Move snake
            head = (snake_positions[0][0] + direction[0], snake_positions[0][1] + direction[1])
            
            # Wrap around borders
            head = (head[0] % GRID_WIDTH, head[1] % GRID_HEIGHT)

            # Check collisions (fake walls don't cause death!)
            if head in snake_positions or head in obstacles:
                # Create explosion particles
                create_explosion_particles(head[0], head[1])
                sound_manager.play('game_over')
                sound_manager.stop_background_music()
                break

            snake_positions.insert(0, head)
            
            # Create trail particles
            if len(snake_positions) > 1:
                create_trail_particle(snake_positions[1][0], snake_positions[1][1])
            
            if head == food_pos:
                if is_fake_food:
                    # Fake food - player loses a segment instead!
                    if len(snake_positions) > 3:  # Don't make it impossible
                        snake_positions.pop()
                        snake_positions.pop()  # Lose 2 segments
                    sound_manager.play('game_over', 0.3)  # Sad sound
                    create_explosion_particles(food_pos[0], food_pos[1])
                else:
                    # Real food
                    score += 1
                    old_level = level
                    level = score // 5 + 1
                    
                    sound_manager.play('eat')
                    create_food_particles(food_pos[0], food_pos[1])
                    
                    # Speed boost trap chance
                    if UNFAIR_MODE and random.random() < SPEED_BOOST_TRAP_CHANCE:
                        speed_boost_active = 240  # 4 seconds of unwanted speed
                    
                    # Level up sound
                    if level > old_level:
                        sound_manager.play('level_up')
                
                # Generate new food regardless
                food_pos, is_fake_food = place_food(snake_positions, obstacles)
                obstacles = generate_obstacles(snake_positions, food_pos)
                fake_walls = []  # Clear fake walls when new food appears
            else:
                snake_positions.pop()
            
            # Update smooth snake with new positions
            smooth_snake.update_targets(snake_positions)

        # Update particles
        update_particles()
        
        # Get smooth interpolated snake positions
        smooth_positions = smooth_snake.get_interpolated_positions(dt)

        # Draw everything
        screen.fill(BG_COLOR)
        
        draw_grid(screen)
        
        # Draw snake with unfair mechanics
        if invisible_snake > 0:
            draw_snake_unfair(screen, [pos for pos in smooth_positions], invisible_snake)
        else:
            draw_snake_smooth(screen, smooth_positions)
            
        draw_obstacles(screen, obstacles)
        draw_fake_walls(screen, fake_walls)
        
        # Draw food with fake food indication
        draw_food_with_glow(screen, food_pos, is_fake_food)
        
        # Draw particles
        draw_particles(screen)

        # Draw enhanced UI
        draw_enhanced_ui(screen, font, small_font, score, level, current_speed, high_score)
        
        # Draw fog of war (this should be drawn after everything else)
        draw_fog_of_war(screen, snake_positions[0], fog_of_war)
        
        # Draw unfair mechanics warnings
        draw_unfair_warnings(screen, small_font, invisible_snake, 
                           speed_boost_active, fog_of_war)

        pygame.display.flip()

    # Game over screen with better visuals
    if score > high_score:
        save_highscore(score)
        high_score = score
    
    # Game over screen
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    screen.blit(overlay, (0, 0))
    
    game_over = font.render("💀 GAME OVER! YOU'VE BEEN PRANKED! �", True, (255, 100, 100))
    final_score = font.render(f"Final Score: {score}", True, TEXT_COLOR)
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 0))
    unfair_text = font.render("This game was rigged from the start! 🎭", True, (255, 150, 150))
    restart_text = font.render("Press R to get pranked again or Q to quit", True, TEXT_COLOR)
    
    screen.blit(game_over, (SCREEN_WIDTH//2 - game_over.get_width()//2, SCREEN_HEIGHT//2 - 80))
    screen.blit(final_score, (SCREEN_WIDTH//2 - final_score.get_width()//2, SCREEN_HEIGHT//2 - 40))
    screen.blit(high_score_text, (SCREEN_WIDTH//2 - high_score_text.get_width()//2, SCREEN_HEIGHT//2 - 10))
    screen.blit(unfair_text, (SCREEN_WIDTH//2 - unfair_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
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