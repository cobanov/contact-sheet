import os
from PIL import Image
from multiprocessing import Pool
from tqdm import tqdm
import argparse
from utils import create_contact_sheet_no_crop
accepted_extensions = (".jpg", ".jpeg", ".png")
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


def create_contact_sheet(image_dir, output_file, img_size):
    if img_size ==0:
        img_size = len(os.listdir(image_dir))
    image_paths = [os.path.join(image_dir, file) for file in os.listdir(image_dir)[0:img_size] if file.lower().endswith(accepted_extensions)]

    # Create the output directory for thumbnails
    output_dir = "thumbnails"
    os.makedirs(output_dir, exist_ok=True)

    # Use multiprocessing to generate thumbnails
    with Pool() as pool, tqdm(
        total=len(image_paths), desc="Generating Thumbnails"
    ) as pbar:
        thumbnail_size = (100, 100)  # Adjust the size as per your requirement
        results = []
        for image_path in image_paths:
            results.append(
                pool.starmap_async(
                    generate_thumbnail, [(image_path, output_dir, thumbnail_size)]
                )
            )
            pbar.update(1)

        for result in tqdm(results, desc="Processing Thumbnails"):
            result.wait()

    # Create the contact sheet
    thumbnails = [
        Image.open(os.path.join(output_dir, file)) for file in os.listdir(output_dir)
    ]
    num_thumbnails = len(thumbnails)
    contact_sheet_width = int(num_thumbnails ** 0.5)  # Number of thumbnails per row
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

def progress_no_crop(*args):
    print(args)
    # create no crop contact sheet from provided rectangles
    for rect in tqdm(args[1],desc='Processing images', unit='image'):
        b, x, y, w, h, rid = rect

        # resize image
        img = args[2][rid].resize((w, h))

        # paste image on contact_sheet
        args[0].paste(img, (x, y))

    # save the final image
    args[0].save(args[3])

    
def main(image_dir, output_file, no_crop, img_size):
    if no_crop:
        contact_sheet,all_rects,images = create_contact_sheet_no_crop(image_dir, output_file, img_size)
        progress_no_crop(contact_sheet,all_rects,images,output_file)
    else:
        create_contact_sheet(image_dir, output_file, img_size)


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Contact Sheet Generator")
    parser.add_argument("image_dir", type=str, help="Directory path containing images")
    parser.add_argument("output_file", type=str, help="Output file path for contact sheet")
    parser.add_argument("--img-size", type=int, help="Contact sheet image size",  default=0)
    parser.add_argument("--no-crop", help="No crop for generate contact sheet", action="store_true")
    args = parser.parse_args()

    # Run the main function with the provided arguments
    main(args.image_dir, args.output_file, args.no_crop, args.img_size)
