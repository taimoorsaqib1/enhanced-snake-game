# 🐍 UNFAIR Snake Game - Prepare to Rage! 😈

A **deviously enhanced** Snake game that **deliberately cheats** and frustrates players with unfair mechanics, while featuring advanced visual effects, procedural audio, and smooth animations. This game is designed to prank and entertain!

## ⚠️ WARNING: THIS GAME CHEATS! ⚠️

This is not your typical Snake game. Expect the unexpected and prepare for frustration! The game includes several "unfair" mechanics designed to surprise and challenge players in unexpected ways.

## 😈 Unfair Mechanics

### 🍎 Fake Food (15% chance)
- Some food items are **fake** and will actually **remove** snake segments instead of adding them
- Fake food has a slightly different appearance (orange color, faster flicker)
- Creates explosion particles when eaten instead of growth

### 📦 Teleporting Obstacles (10% chance) 
- Obstacles randomly **teleport** to new positions during gameplay
- Creates explosion particles at old and new positions
- Keeps players on their toes!

### 👻 Invisible Snake (8% chance)
- Your snake becomes **partially invisible** for several seconds
- Flickering visibility makes navigation challenging
- Subtle outline helps maintain some visibility

### ⚡ Speed Boost Trap (10% chance)
- Some real food triggers an **unwanted speed boost**
- Forces players to move faster than comfortable
- Lasts for 4 seconds of chaos

### 🧱 Fake Walls (5% chance)
- Walls that **look real but aren't deadly**
- You can pass through them safely
- Designed to create false panic

### 🌫️ Fog of War (6% chance)
- **Limited visibility** around your snake head only
- Everything outside the vision radius becomes black
- Movement speed is **reduced during fog**
- Pulsating fog effect for extra disorientation

## ✨ Enhanced Features (When the game isn't cheating)

### 🎨 Advanced Visual Effects
- **Smooth Movement Interpolation**: 60 FPS rendering with fluid snake movement
- **Enhanced Particle System**: 
  - Rainbow food particles with physics simulation
  - Explosion effects on game over
  - Snake trail particles with procedural noise
- **Dynamic Visual Effects**:
  - Pulsing glow effects on food and snake head
  - Direction-aware snake eyes
  - Animated UI elements with scaling effects
  - Level progress bar with smooth animations

### 🔊 Professional Audio System
- **Advanced Sound Synthesis**: Using NumPy and SciPy for high-quality audio
- **Musical Chords**: Food eating plays pleasant C major chords
- **Frequency Sweeps**: Game over sound with descending sweep
- **Ambient Background Music**: Procedurally generated atmospheric pad sounds
- **ADSR Envelopes**: Professional attack/decay/sustain/release for all sounds

### 🎮 Enhanced Gameplay
- **Smooth Input Buffering**: Prevents accidental reverse deaths from quick inputs
- **Dynamic Difficulty**: Speed increases progressively with score
- **Level System**: Visual level progression with color-coded indicators
- **Enhanced UI**: Real-time speed display, level progress, animated score

### � Technical Improvements
- **NumPy Integration**: Fast mathematical calculations for smooth effects
- **Procedural Noise**: Organic particle movement using Perlin noise
- **60 FPS Rendering**: Separate game logic and rendering loops
- **Memory Optimized**: Efficient particle system with automatic cleanup

## 🎮 Controls

- **Arrow Keys**: Move the snake
- **Any Key**: Start game from title screen
- **R**: Restart after game over
- **Q**: Quit game

## 🚀 Quick Start

### Option 1: Auto-Launcher (Recommended)
```bash
python run_game.py
```
The launcher will automatically install dependencies and start the game!

### Option 2: Manual Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/taimoorsaqib1/enhanced-snake-game.git
   cd enhanced-snake-game
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**
   ```bash
   python game.py
   ```

## 📦 Enhanced Dependencies

- `pygame>=2.5.0` - Advanced game development library
- `numpy>=1.21.0` - Fast numerical computations for smooth animations
- `scipy>=1.7.0` - Signal processing for advanced audio synthesis
- `noise>=1.2.2` - Perlin noise for organic particle movement
- `colorama>=0.4.4` - Enhanced terminal output

## 🎯 Game Rules (When They Apply!)

1. **Objective**: Eat red food to grow your snake and increase your score *(unless it's fake!)*
2. **Avoid**: Hitting yourself, obstacles *(real ones)*, or going off-screen (wraps around)
3. **Growth**: Each **real** food item makes your snake longer
4. **Speed**: Game speed increases every 5 points *(plus random speed traps!)*
5. **Obstacles**: Gray blocks that regenerate when you eat food *(and may teleport randomly)*
6. **Survival**: Try to maintain your sanity while the game pranks you

## 🤡 What Makes This Game "Unfair"

- **Fake Food**: Looks like real food but steals your progress
- **Random Teleportation**: Obstacles move when you least expect it  
- **Invisible Snake**: Good luck seeing where you're going!
- **Speed Traps**: Sudden unwanted acceleration
- **Fake Walls**: Psychological warfare at its finest
- **Visual Warnings**: The game tells you when it's being unfair (how generous!)

## 🏗️ Project Structure

```
unfair-snake-game/
├── game.py              # Main unfair game file
├── README.md            # This file
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore file
├── LICENSE             # MIT License
├── run_game.py         # Auto-launcher script
└── highscore.txt       # High score storage (auto-generated)
```

## 🎨 Customization

You can adjust the unfairness level by modifying constants in `game.py`:

- **FAKE_FOOD_CHANCE**: Probability of fake food (default: 0.15)
- **TELEPORT_OBSTACLES_CHANCE**: Obstacle teleportation rate (default: 0.1)
- **INVISIBLE_SNAKE_CHANCE**: Snake invisibility chance (default: 0.08)
- **SPEED_BOOST_TRAP_CHANCE**: Speed trap probability (default: 0.1)
- **FAKE_WALLS_CHANCE**: Fake wall appearance rate (default: 0.05)
- **UNFAIR_MODE**: Set to False to disable all unfair mechanics

## 🚀 Future Enhancements

- [ ] **Even More Unfair Mechanics**: We can always make it worse!
- [ ] **Difficulty Settings**: From "Slightly Annoying" to "Rage Quit Guaranteed"
- [ ] **Unfairness Analytics**: Track how much the game has pranked you
- [ ] **Multiplayer Pranking**: Sabotage your friends in real-time
- [ ] **Custom Pranks**: Let players create their own unfair mechanics
- [ ] **Achievement System**: "Survived 10 fake foods", "Played while invisible for 30 seconds"
- [ ] **Rage Meter**: Visual indicator of player frustration levels
- [ ] **Anti-Cheat System**: Detect when players try to cheat the cheating game
- [ ] **Psychological Profiles**: AI that learns your weaknesses and exploits them
- [ ] **VR Pranking**: Virtual reality unfairness for maximum immersion

## 🏆 Performance Features

- **60 FPS Rendering**: Buttery smooth gameplay
- **Optimized Particle System**: Handles hundreds of particles efficiently
- **Memory Management**: Automatic cleanup prevents memory leaks
- **Scalable Architecture**: Easy to add new features and effects

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎮 Screenshots

*Add screenshots of your game here*

## 🙏 Acknowledgments

- Built with [Pygame](https://www.pygame.org/)
- Inspired by the classic Snake game (and the desire to ruin it)
- Sound effects generated using pygame's sound synthesis
- Designed to test patience and create memorable gaming moments
- Special thanks to all the players who will rage quit this game

## ⚠️ Disclaimer

This game is designed for entertainment purposes and may cause:
- Mild to severe frustration
- Temporary loss of faith in fair gaming
- Uncontrollable urge to restart "just one more time"
- Appreciation for honest game mechanics

Play at your own risk! 😈

---

**Good luck... you'll need it! 🐍😈**
