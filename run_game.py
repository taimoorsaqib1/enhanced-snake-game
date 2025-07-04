#!/usr/bin/env python3
"""
Enhanced Snake Game Launcher
Automatically installs dependencies and runs the game
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        print("🔧 Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def run_game():
    """Run the enhanced snake game"""
    try:
        print("🐍 Starting Enhanced Snake Game...")
        import game
        print("🎮 Game started! Enjoy playing!")
    except ImportError as e:
        print(f"❌ Failed to import game: {e}")
        print("🔧 Trying to install dependencies...")
        if install_requirements():
            try:
                import game
                print("🎮 Game started! Enjoy playing!")
            except Exception as e2:
                print(f"❌ Still failed to start game: {e2}")
        else:
            print("❌ Could not install dependencies. Please run: pip install -r requirements.txt")

if __name__ == "__main__":
    print("🚀 Enhanced Snake Game Launcher")
    print("=" * 40)
    
    # Check if we're in the right directory
    game_file = os.path.join(os.path.dirname(__file__), "game.py")
    if not os.path.exists(game_file):
        print("❌ game.py not found. Please ensure game.py is in the same directory.")
        sys.exit(1)
    
    run_game()
