#!/usr/bin/env python3
"""
🔧 Dependency Installation Script
Installs missing dependencies and checks system requirements.
"""

import subprocess
import sys
import importlib

def check_package(package_name):
    """Check if a package is installed."""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def install_package(package_name):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Main installation function."""
    print("🔧 Banking Text-to-SQL Agent - Dependency Checker")
    print("=" * 50)
    
    # List of required packages
    required_packages = [
        "tabulate",
        "pandas", 
        "numpy",
        "langchain",
        "langchain_openai",
        "faiss",
        "streamlit",
        "psycopg2",
        "pyyaml"
    ]
    
    missing_packages = []
    
    print("📦 Checking required packages...")
    for package in required_packages:
        if check_package(package):
            print(f"✅ {package} - Installed")
        else:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Found {len(missing_packages)} missing package(s)")
        response = input("Would you like to install them? (y/n): ")
        
        if response.lower() in ['y', 'yes']:
            print("\n📥 Installing missing packages...")
            for package in missing_packages:
                print(f"Installing {package}...")
                if install_package(package):
                    print(f"✅ {package} installed successfully")
                else:
                    print(f"❌ Failed to install {package}")
        else:
            print("Installation skipped. Please install manually:")
            print(f"pip install {' '.join(missing_packages)}")
    else:
        print("\n🎉 All required packages are installed!")
    
    print("\n💡 Quick fix for tabulate error:")
    print("pip install tabulate")
    
    print("\n🚀 You can now run:")
    print("python test_system.py")

if __name__ == "__main__":
    main() 