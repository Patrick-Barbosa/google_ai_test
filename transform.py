from PIL import Image
import os
from pathlib import Path

def resize_images(input_dir, output_dir, target_size):
    """
    Resize images from input directory and save them to output directory
    
    Args:
        input_dir (str): Input directory path
        output_dir (str): Output directory path
        target_size (tuple): Target size as (width, height)
    """
    Path(output_dir).mkdir(exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            with Image.open(input_path) as img:
                img = img.resize(target_size, Image.Resampling.LANCZOS)
                img.save(output_path, quality=95)