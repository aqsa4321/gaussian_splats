from PIL import Image
import os

def resize_images_in_folder(folder_path, target_size=(512, 272)):
    """
    Resizes all images in the specified folder to the target_size.
    
    Args:
        folder_path (str): Path to the folder containing the images to be resized.
        target_size (tuple): Target size (width, height) to resize the images to.
    """
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        # Construct the full file path
        file_path = os.path.join(folder_path, filename)
        
        # Check if the file is an image (you can expand the list of extensions if needed)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
            try:
                # Open the image
                with Image.open(file_path) as img:
                    # Resize the image
                    img_resized = img.resize(target_size, Image.ANTIALIAS)
                    # Save the resized image (overwrite the original image)
                    img_resized.save(file_path)
                    print(f"Resized: {filename}")
            except Exception as e:
                print(f"Error resizing {filename}: {e}")

# Example usage:
folder_path = '/home/csslab/Documents/Aqsa/GS/dataexamples/family/mast3r/images'  # Replace with the path to your folder
resize_images_in_folder(folder_path)

