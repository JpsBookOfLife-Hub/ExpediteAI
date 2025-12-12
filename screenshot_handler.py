"""Handles finding and reading the latest screenshot from the screenshots directory."""
import os
from pathlib import Path
from typing import Optional
from PIL import Image


def get_latest_screenshot(screenshot_dir: str) -> Optional[str]:
    """
    Get the path to the most recently created screenshot.
    
    Args:
        screenshot_dir: Path to the screenshots directory
        
    Returns:
        Path to the latest screenshot file, or None if no screenshots found
    """
    try:
        dir_path = Path(screenshot_dir)
        
        if not dir_path.exists():
            return None
        
        # Get all image files in the directory
        image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp'}
        image_files = [
            f for f in dir_path.iterdir()
            if f.is_file() and f.suffix.lower() in image_extensions
        ]
        
        if not image_files:
            return None
        
        # Sort by modification time, most recent first
        latest_file = max(image_files, key=lambda f: f.stat().st_mtime)
        
        return str(latest_file)
    
    except Exception as e:
        print(f"Error getting latest screenshot: {e}")
        return None


def read_screenshot(image_path: str) -> Optional[Image.Image]:
    """
    Read and return the screenshot image.
    
    Args:
        image_path: Path to the screenshot file
        
    Returns:
        PIL Image object, or None if reading fails
    """
    try:
        return Image.open(image_path)
    except Exception as e:
        print(f"Error reading screenshot: {e}")
        return None

