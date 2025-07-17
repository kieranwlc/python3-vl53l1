import os
import subprocess
import sys
import shutil

def _ensure_library_built():
    """Ensure the C library is built and available"""
    # Get the directory containing this __init__.py
    package_dir = os.path.dirname(os.path.abspath(__file__))
    lib_path = os.path.join(package_dir, "libtof.so")
    
    # If library already exists, we're good
    if os.path.exists(lib_path):
        return
    
    print("Building VL53L1 C library...")
    
    # Get the directory containing setup.py (parent of package_dir)
    setup_dir = os.path.dirname(package_dir)
    lib_dir = os.path.join(setup_dir, "STSW-IMG013", "user_lib")
    
    # Check if the library directory exists
    if not os.path.exists(lib_dir):
        raise FileNotFoundError(f"Library directory not found: {lib_dir}")
    
    # Build the library
    try:
        subprocess.check_call(
            ["make", "clean"], 
            cwd=lib_dir, 
            env=os.environ,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        print("✓ Cleaned previous build")
    except subprocess.CalledProcessError:
        print("⚠ Clean failed (expected if no previous build)")
    
    try:
        subprocess.check_call(
            ["make", "libtof"], 
            cwd=lib_dir, 
            env=os.environ,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        print("✓ C library built successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to build C library: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        raise
    
    # Copy the built library to the package directory
    source_lib = os.path.join(lib_dir, "libtof.so")
    if not os.path.exists(source_lib):
        raise FileNotFoundError(f"Built library not found: {source_lib}")
    
    shutil.copy2(source_lib, lib_path)
    print(f"✓ Library copied to: {lib_path}")

# Build the library when the package is imported
_ensure_library_built()
