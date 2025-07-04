# 🐍 Enhanced Snake Game

A visually enhanced Snake game built with Python and Pygame featuring particle effects, sound effects, and modern visual design.

## ✨ Features

### Visual Enhancements
- 🎨 Modern dark theme with vibrant colors
- 👁️ Snake head with animated eyes and glow effect
- ✨ Particle effects when eating food
- 🌟 Pulsing glow effects on food
- 🎯 3D-style obstacles with highlights
- 📊 Enhanced UI with level and speed display

### Audio Features
- 🔊 Sound effects for eating food
- 💥 Game over sound
- 🎵 Simple background music (generated tones)

### Gameplay Features
- 🎮 Classic Snake mechanics
- 🚧 Random obstacles that regenerate
- 📈 Increasing difficulty (speed increases with score)
- 🏆 High score persistence
- 🔄 Wrap-around screen edges
- ⌨️ Smooth controls with direction locking

## 🎮 Controls

- **Arrow Keys**: Move the snake
- **Any Key**: Start game from title screen
- **R**: Restart after game over
- **Q**: Quit game

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/enhanced-snake-game.git
   cd enhanced-snake-game
   ```

2. **Install dependencies**
   ```bash
   pip install pygame
   ```

3. **Run the game**
   ```bash
   python game.py
   ```

## 📦 Dependencies

- `pygame` - Game development library for graphics and sound
- `math` - Mathematical functions for effects
- `random` - Random number generation
- `os` - File operations for high score
- `sys` - System operations
- `time` - Time-based animations

## 🎯 Game Rules

1. **Objective**: Eat red food to grow your snake and increase your score
2. **Avoid**: Hitting yourself, obstacles, or going off-screen (wraps around)
3. **Growth**: Each food item makes your snake longer
4. **Speed**: Game speed increases every 5 points
5. **Obstacles**: Gray blocks that regenerate when you eat food

## 🏗️ Project Structure

```
enhanced-snake-game/
├── game.py              # Main game file
├── README.md            # This file
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore file
└── highscore.txt       # High score storage (auto-generated)
```

## 🎨 Customization

You can easily customize the game by modifying constants in `game.py`:

- **Colors**: Modify the color constants (BG_COLOR, SNAKE_HEAD, etc.)
- **Game Speed**: Change FPS value
- **Grid Size**: Adjust GRID_WIDTH and GRID_HEIGHT
- **Cell Size**: Modify CELL_SIZE for larger/smaller game elements
- **Obstacles**: Change OBSTACLE_COUNT for more/fewer obstacles

## 🚀 Future Enhancements

- [ ] Multiple game modes (Time Attack, Survival, Multiplayer)
- [ ] Power-ups and special abilities
- [ ] More sophisticated sound effects and music
- [ ] Snake customization (skins, colors)
- [ ] Achievement system
- [ ] Online leaderboards
- [ ] Mobile version with touch controls

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
- Inspired by the classic Snake game
- Sound effects generated using pygame's sound synthesis

---

**Enjoy playing! 🐍🎮**
