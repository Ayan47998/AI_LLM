#!/usr/bin/env python3
"""
Test script to verify MSA Review App setup
"""

import sys
import importlib
import os

def test_imports():
    """Test if all required packages can be imported."""
    required_packages = [
        'streamlit',
        'openai',
        'PyPDF2',
        'docx',
        'langchain_openai',
        'langchain_core',
        'dotenv'
    ]
    
    missing_packages = []
    
    print("Testing package imports...")
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package} - {e}")
            missing_packages.append(package)
    
    return missing_packages

def test_env_setup():
    """Test environment setup."""
    print("\nTesting environment setup...")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
        
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check for OpenAI API key
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and api_key != 'your_openai_api_key_here':
            print("✅ OpenAI API key configured")
            if api_key.startswith('sk-'):
                print("✅ API key format looks correct")
            else:
                print("⚠️  API key format may be incorrect (should start with 'sk-')")
        else:
            print("❌ OpenAI API key not configured or still using template value")
            print("   Please edit .env file and add your actual OpenAI API key")
    else:
        print("❌ .env file not found")
        print("   Please copy .env.template to .env and configure your API key")

def main():
    """Main test function."""
    print("MSA Review App - Setup Test")
    print("=" * 40)
    
    # Test Python version
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    else:
        print("✅ Python version compatible")
    
    # Test imports
    missing_packages = test_imports()
    
    # Test environment
    test_env_setup()
    
    print("\n" + "=" * 40)
    
    if missing_packages:
        print("❌ Setup incomplete!")
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All packages installed successfully!")
        
        if os.path.exists('.env') and os.getenv('OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY') != 'your_openai_api_key_here':
            print("✅ Setup complete! You can run the app with:")
            print("   streamlit run msa_review_app.py")
            return True
        else:
            print("⚠️  Setup almost complete!")
            print("   Please configure your .env file with OpenAI API key")
            return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)