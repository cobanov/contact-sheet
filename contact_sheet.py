import os
from PIL import Image
from multiprocessing import Pool


def generate_thumbnail(image_path, output_dir, thumbnail_size):
    image = Image.open(image_path)

    # Center square crop
    width, height = image.size
    if width > height:
        left = (width - height) // 2
        right = left + height
        top = 0
        bottom = height
    else:
        top = (height - width) // 2
        bottom = top + width
        left = 0
        right = width

    image = image.crop((left, top, right, bottom))

    image.thumbnail(thumbnail_size)
    image.save(os.path.join(output_dir, os.path.basename(image_path)))


def create_contact_sheet(image_dir, output_file):
    image_paths = [os.path.join(image_dir, file) for file in os.listdir(image_dir)]

    # Create the output directory for thumbnails
    output_dir = "thumbnails"
    os.makedirs(output_dir, exist_ok=True)

    # Use multiprocessing to generate thumbnails
    pool = Pool()
    thumbnail_size = (100, 100)  # Adjust the size as per your requirement
    pool.starmap(
        generate_thumbnail,
        [(image_path, output_dir, thumbnail_size) for image_path in image_paths],
    )
    pool.close()
    pool.join()

    # Create the contact sheet
    thumbnails = [
        Image.open(os.path.join(output_dir, file)) for file in os.listdir(output_dir)
    ]
    num_thumbnails = len(thumbnails)
    contact_sheet_width = int(num_thumbnails**0.5)  # Number of thumbnails per row
    contact_sheet_height = (num_thumbnails // contact_sheet_width) + (
        num_thumbnails % contact_sheet_width > 0
    )

    # Calculate the square size based on the contact sheet dimensions
    thumbnail_size = max(thumbnail_size)
    square_size = (
        thumbnail_size * contact_sheet_width,
        thumbnail_size * contact_sheet_height,
    )

    contact_sheet = Image.new("RGB", square_size)
    x_offset, y_offset = 0, 0
    for thumbnail in thumbnails:
        contact_sheet.paste(thumbnail, (x_offset, y_offset))

        x_offset += thumbnail_size
        if x_offset >= thumbnail_size * contact_sheet_width:
            x_offset = 0
            y_offset += thumbnail_size

    # Save the contact sheet
    contact_sheet.save(output_file)

    # Clean up the temporary thumbnail directory
    for file in os.listdir(output_dir):
        os.remove(os.path.join(output_dir, file))
    os.rmdir(output_dir)


if __name__ == "__main__":
    # Usage example
    image_dir = "/Users/cobanov-air/Desktop/class_03"
    output_file = "output_contact_sheet.jpg"
    create_contact_sheet(image_dir, output_file)