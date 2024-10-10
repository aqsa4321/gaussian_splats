import os
import numpy as np
import math
from PIL import Image  # To read image size

# Function to calculate FOV (Field of View)
def calculate_fov(focal_length, dimension):
    return 2 * math.atan(dimension / (2 * focal_length))

# Function to parse camera intrinsic file
def parse_intrinsics(file_path):
    intrinsics = {}
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('Camera'):
                cam_id = int(line.split()[1])
                focal_length = float(line.split(':')[1].strip())
                intrinsics[cam_id] = focal_length
    return intrinsics

# Function to parse camera extrinsic file
# Function to parse camera extrinsic file
def parse_extrinsics(file_path):
    extrinsics = {}
    cam_id = None
    matrix = []

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('Camera'):  # Start of new camera data
                if cam_id is not None and len(matrix) == 3:  # If we've read a previous camera's data (3 rows)
                    extrinsics[cam_id] = np.array(matrix)  # Save the 3x4 matrix
                cam_id = int(line.split()[1])  # Now set the new cam_id
                matrix = []  # Reset matrix for the new camera
            elif 'tensor([' in line:  # Handle the first row embedded in the 'tensor([' line
                clean_line = line.split('tensor([')[1].strip('[]').replace(',', '').replace(')', '').replace(']', '').strip()
                row = [float(x) for x in clean_line.split()]
                matrix.append(row)  # Add the first row
            elif line.startswith('['):  # Handle subsequent rows
                clean_line = line.strip('[]').replace(',', '').replace(')', '').replace(']', '').strip()
                row = [float(x) for x in clean_line.split()]
                if len(row) == 4 and len(matrix) < 3:  # Only take first 3 rows with 4 elements
                    matrix.append(row)
            elif 'tensor' in line or line.startswith(']'):
                continue  # Skip lines with 'tensor' or closing brackets

        # Add the last camera's data
        if cam_id is not None and len(matrix) == 3:
            extrinsics[cam_id] = np.array(matrix)  # Save the 3x4 matrix

    return extrinsics


def parse_extrinsics1(file_path):
    extrinsics = {}
    cam_id = None
    matrix = []

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('Camera'):  # Start of new camera data
                if cam_id is not None:  # If we've read a previous camera's data
                    extrinsics[cam_id] = np.array(matrix).reshape(3, 4)  # Save the previous camera's matrix
                cam_id = int(line.split()[1])  # Now set the new cam_id
                matrix = []  # Reset matrix for the new camera
            elif line.startswith('tensor'):  # Skip 'tensor' lines
                continue
            elif line:  # Matrix data line
                # Clean the line by removing unwanted characters
                clean_line = line.strip('[]').replace(',', '').replace(']', '').replace('(', '').replace(')', '').strip()
                try:
                    matrix.append([float(x) for x in clean_line.split()])
                except ValueError as e:
                    print(f"Error converting to float: {e}")
                    print(f"Offending line: {clean_line}")
                    continue

        # Add the last camera's data
        if cam_id is not None and matrix:
            extrinsics[cam_id] = np.array(matrix).reshape(3, 4)

    return extrinsics

# Main function to generate camera info file in the correct format
def generate_camera_info(images_path, cam_intrinsics_file, cam_extrinsics_file, output_path):
    # Parse intrinsic and extrinsic data
    intrinsics = parse_intrinsics(cam_intrinsics_file)
    extrinsics = parse_extrinsics(cam_extrinsics_file)

    # Get the list of images
    image_files = sorted([f for f in os.listdir(images_path) if f.endswith('.jpg') or f.endswith('.png')])

    # Ensure the number of images matches the intrinsic/extrinsic data
    if len(image_files) != len(intrinsics) or len(image_files) != len(extrinsics):
        raise ValueError("Mismatch between the number of images and camera data.")
    output_file = os.path.join(output_path, 'cam_infos_created.txt')
    with open(output_file, 'w') as f_out:
        for i, image_file in enumerate(image_files):
            # Load the image to get its dimensions
            image_path = os.path.join(images_path, image_file)
            with Image.open(image_path) as img:
                width, height = img.size

            # Get focal length for current camera
            focal_length = intrinsics[i]

            # Calculate FOVX and FOVY
            fov_x = calculate_fov(focal_length, width)
            fov_y = calculate_fov(focal_length, height)

            # Get extrinsic data for the current camera
            extrinsic_matrix = extrinsics[i]
            rotation_matrix = extrinsic_matrix[:, :3]  # Get the rotation matrix (no need to convert to list)
            translation_vector = extrinsic_matrix[:, 3].tolist()  # Convert translation vector to a list

            # Write the camera info to the output file in the desired format
            f_out.write(f"Camera {i} Info:\n")
            f_out.write(f"UID: {i}\n")
            f_out.write("Rotation Matrix (R):\n")
            for row in rotation_matrix:  # Write the rotation matrix row by row, no commas
                f_out.write(f"[{' '.join([f'{val:.8f}' for val in row])}]\n")
            f_out.write(f"Translation Vector (T): [{' '.join([f'{val:.8f}' for val in translation_vector])}]\n")
            f_out.write(f"FOVY: {fov_y:.10f}\n")
            f_out.write(f"FOVX: {fov_x:.10f}\n")
            f_out.write(f"Image Path: {image_path}\n")
            f_out.write(f"Image Name: {os.path.basename(image_path)}\n")
            f_out.write(f"Width: {width}\n")
            f_out.write(f"Height: {height}\n")
            f_out.write("\n" + "-"*50 + "\n\n")

# Example usage
subdir = '/home/csslab/Documents/Aqsa/GS/dataexamples/family/mast3r/'
images_folder = os.path.join(subdir, 'images')
cam_intrinsics_file = os.path.join(subdir, 'sparse/0/cam_intrinsics.txt')
cam_extrinsics_file = os.path.join(subdir, 'sparse/0/cam_extrinsics.txt')
output_path = os.path.join(subdir, 'sparse/0/')

generate_camera_info(images_folder, cam_intrinsics_file, cam_extrinsics_file, output_path)
