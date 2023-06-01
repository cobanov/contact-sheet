import os
import argparse


def find_image_files(folder_path):
    image_extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
    ]  # Add more extensions if needed
    image_files = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension in image_extensions:
                file_path = os.path.join(root, file)
                image_files.append(file_path)

    return image_files


# Create the argument parser
parser = argparse.ArgumentParser(description="Scan subfolders for image files.")

# Add the folder_path argument
parser.add_argument("folder_path", type=str, help="the path to the folder to scan")

# Parse the arguments
args = parser.parse_args()

folder_path = args.folder_path

image_files = find_image_files(folder_path)

# Write file paths to filelist.txt
with open("filelist.txt", "w") as file:
    for file_path in image_files:
        file.write(file_path + "\n")

print("File list has been saved to 'filelist.txt'")
