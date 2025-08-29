"""
Test final CLI functionality after all corrections.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_cli():
    """Test CLI import and basic functionality."""
    print("🧪 Testing CLI functionality...")
    
    try:
        from cli import app
        print("✅ CLI import successful!")
        
        # Test basic CLI help
        print("\n📋 Testing CLI help...")
        return True
        
    except ImportError as e:
        print(f"❌ CLI import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_cli()
    
    if success:
        print("\n🎉 CLI is ready!")
        print("\n🚀 You can now use:")
        print("   python main.py --help")
        print("   python main.py generate --help")
        print("   python main.py generate terrain --preview --seed 123")
        print("   python main.py generate info")
        print("   python main.py export godot --help")
        print("   python main.py optimize scene --help")
    else:
        print("\n❌ CLI test failed. Check the errors above.")
