import os
import re
from zipfile import ZipFile
from ebooklib import epub

# Function to extract volume number and create a simplified name for EPUB
def generate_epub_name(original_name):
    volume_number_match = re.search(r'v(\d+)', original_name)
    if volume_number_match:
        volume_number = int(volume_number_match.group(1))
        return f"Volume {volume_number}.epub"
    else:
        return f"One_Piece_{original_name}.epub"

# Additional function to convert CBZ to PDF
def convert_cbz_to_pdf(cbz_path, pdf_path):
    from PIL import Image
    import io

    if not os.path.exists(cbz_path):
        print(f"Error: {cbz_path} does not exist.")
        return

    image_list = []

    with ZipFile(cbz_path, 'r') as zip_ref:
        image_files = sorted([n for n in zip_ref.namelist() if n.lower().endswith(('.png', '.jpg', '.jpeg'))])
        for img_file in image_files:
            img_data = zip_ref.read(img_file)
            img = Image.open(io.BytesIO(img_data))
            image_list.append(img)

    if image_list:
        image_list[0].save(pdf_path, save_all=True, append_images=image_list[1:])
        print(f"Converted {cbz_path} to {pdf_path}.")
    else:
        print(f"Error: No images found in {cbz_path}.")

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
    chapters = []
    with ZipFile(cbz_path, 'r') as zip_ref:
        image_files = sorted([n for n in zip_ref.namelist() if n.lower().endswith(('.png', '.jpg', '.jpeg'))])
        for index, img_file in enumerate(image_files):
            img_data = zip_ref.read(img_file)

            # Add image to the EPUB book
            img_item = epub.EpubImage()
            img_item.file_name = img_file.split('/')[-1]
            img_item.content = img_data
            book.add_item(img_item)

            # Create a chapter for each image
            chapter = epub.EpubHtml(title=f'Page {index + 1}', file_name=f'page_{index + 1}.xhtml', lang='en')
            chapter.content = f'<img src="{img_item.file_name}" alt="Page {index + 1}" />'
            chapters.append(chapter)
            book.add_item(chapter)

    # Create a table of contents
    book.toc = chapters

    # Update the spine to include chapters
    book.spine = ['nav'] + chapters

    # Create a navigation page (mandatory)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Generate EPUB file
    epub.write_epub(epub_path, book)

# Main function to convert all CBZ files in a given directory
def convert_all_cbz(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.cbz'):
            cbz_path = os.path.join(folder_path, filename)

            # Convert to EPUB - works :)
            #new_epub_name = generate_epub_name(filename)
            #epub_path = os.path.join(folder_path, new_epub_name)
            #convert_cbz_to_epub(cbz_path, epub_path)
            #print(f"Converted {filename} to {new_epub_name}.")

            # Convert to PDF - Testing
            new_pdf_name = filename.replace('.cbz', '.pdf')
            pdf_path = os.path.join(folder_path, new_pdf_name)
            convert_cbz_to_pdf(cbz_path, pdf_path)
            print(f"Converted {filename} to {new_pdf_name}.")

if __name__ == "__main__":
    folder_path = "/Users/aamindehkordi/Downloads/one piece/colored/cbz"
    convert_all_cbz(folder_path)
