# Final complete Python script for converting .cbz files to .epub with specified naming
import os
import re
from zipfile import ZipFile
from ebooklib import epub


# Function to extract volume number and create a simplified name
def generate_epub_name(original_name):
    # Regular expression to find the volume number in the original file name
    volume_number_match = re.search(r'v(\d+)', original_name)

    if volume_number_match:
        volume_number = int(volume_number_match.group(1))
        return f"OP - Volume {volume_number}.epub"
    else:
        return None


# Function to convert a single CBZ file to EPUB format
def convert_cbz_to_epub(cbz_path, epub_path):
    # Create a new EPUB book
    book = epub.EpubBook()
    book.set_identifier(os.path.basename(epub_path))
    book.set_title(os.path.basename(epub_path))
    book.set_language('en')

    # Create a spine (mandatory element of EPUB book)
    book.spine = ['nav']

    # Open the CBZ file and extract images
    image_files = []
    with ZipFile(cbz_path, 'r') as zip_ref:
        image_files = sorted([n for n in zip_ref.namelist() if n.lower().endswith(('.png', '.jpg', '.jpeg'))])
        for img_file in image_files:
            img_data = zip_ref.read(img_file)

            # Add image to the EPUB book
            img_item = epub.EpubImage()
            img_item.file_name = img_file.split('/')[-1]
            img_item.content = img_data
            book.add_item(img_item)

    # Create a navigation page (mandatory)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Generate EPUB file
    epub.write_epub(epub_path, book)


# Main function to convert all CBZ files in a given directory to EPUB files
def convert_all_cbz_to_epub(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.cbz'):
            cbz_path = os.path.join(folder_path, filename)

            # Generate the new EPUB file name based on the volume number
            new_epub_name = generate_epub_name(filename)
            if new_epub_name is None:
                print(f"Skipping {filename} as volume number could not be determined.")
                continue

            epub_path = os.path.join(folder_path, new_epub_name)
            convert_cbz_to_epub(cbz_path, epub_path)
            print(f"Converted {filename} to {new_epub_name}.")

# Uncomment the line below to run the script on a real folder.
convert_all_cbz_to_epub('/Users/aamindehkordi/Downloads/one piece/colored/mana-one-piece-digital-colored-comics')
