#!/usr/bin/env python3
"""
Simple script to run the Streamlit personal website application.
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit application."""
    try:
        # Check if streamlit is installed
        import streamlit
        print("🚀 Starting Personal Portfolio Website...")
        print("📱 The website will open in your default browser")
        print("🔗 Local URL: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Run streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
        
    except ImportError:
        print("❌ Streamlit is not installed!")
        print("📦 Please install it using: pip install streamlit")
        print("📦 Or install all requirements: pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Thanks for using the portfolio website.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 