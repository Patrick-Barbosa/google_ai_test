import os
from PIL import Image

class ImageUpscaler:
    def __init__(self, new_dpi=600):
        """
        Initialize the upscaler with a default DPI
        
        Args:
            new_dpi (int): Desired DPI for output images (default: 600)
        """
        self.new_dpi = new_dpi
    
    def upscale_image(self, input_path, output_path):
        """
        Upscale a single image
        
        Args:
            input_path (str): Path to input image
            output_path (str): Path to save processed image
        """
        with Image.open(input_path) as img:
            original_dpi = img.info.get('dpi', (72, 72))[0]
            original_width, original_height = img.size
            
            physical_width = original_width / original_dpi
            physical_height = original_height / original_dpi
            
            new_width = int(physical_width * self.new_dpi)
            new_height = int(physical_height * self.new_dpi)
            
            print(f"Processing: {os.path.basename(input_path)}")
            print(f"Original Size: {original_width}x{original_height} pixels at {original_dpi} DPI")
            print(f"New Size: {new_width}x{new_height} pixels at {self.new_dpi} DPI")
            
            upscaled_img = img.resize((new_width, new_height), resample=Image.LANCZOS)
            upscaled_img.save(output_path, dpi=(self.new_dpi, self.new_dpi))
    
    def upscale_folder(self, input_folder, output_folder):
        """
        Upscale all images in a folder
        
        Args:
            input_folder (str): Path to folder with input images
            output_folder (str): Path to save processed images
        """
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        
        # Process all files in input folder
        for filename in os.listdir(input_folder):
            input_path = os.path.join(input_folder, filename)
            
            # Skip directories
            if not os.path.isfile(input_path):
                continue
                
            try:
                output_path = os.path.join(output_folder, filename)
                self.upscale_image(input_path, output_path)
                print(f"Successfully processed: {filename}\n")
            except Exception as e:
                print(f"Failed to process {filename}: {str(e)}\n")

if __name__ == "__main__":
    # Example usage
    upscaler = ImageUpscaler(new_dpi=600)
    
    # Process a single image
    # upscaler.upscale_image("input.jpg", "output.jpg")
    
    # Process an entire folder
    upscaler.upscale_folder(
        input_folder="path/to/input/folder",
        output_folder="path/to/output/folder"
    )