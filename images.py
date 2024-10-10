import os

def filter_and_rename_images(folder_path):
    # List all files in the directory
    image_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".jpg")])

    # Keep every second image (starting from the first)
    selected_images = image_files[::2]

    # Delete images that are not selected
    for image in image_files:
        if image not in selected_images:
            os.remove(os.path.join(folder_path, image))

    # Rename remaining images in sequential order
    for index, image in enumerate(selected_images):
        new_name = f"{index+1:06}.jpg"
        os.rename(os.path.join(folder_path, image), os.path.join(folder_path, new_name))
        print(f"Renamed {image} to {new_name}")

# Example usage
folder_path = "/home/csslab/Documents/Aqsa/GS/dataexamples/family/mast3r/images"  # Replace with your actual folder path
filter_and_rename_images(folder_path)

