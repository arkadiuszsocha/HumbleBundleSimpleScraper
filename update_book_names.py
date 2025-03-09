import os
from ebooklib import epub

def get_epub_metadata(epub_path):
    try:
        book = epub.read_epub(epub_path)
        title_metadata = book.get_metadata('DC', 'title')
        title = title_metadata[0][0] if title_metadata and title_metadata[0] else 'Unknown Title'
        authors_metadata = book.get_metadata('DC', 'creator')
        authors = [author[0] for author in authors_metadata if author] if authors_metadata else ['Unknown Author']
        return title, authors
    except Exception as e:
        print(f"Error processing {epub_path}: {str(e)}")
        return None, None

def rename_epub_files(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist")
        return

    for filename in os.listdir(folder_path):
        if filename.endswith('.epub'):
            print(f"Processing '{filename}'")   
            epub_path = os.path.join(folder_path, filename)
            title, authors = get_epub_metadata(epub_path)
            
            if title and authors:
                safe_title = "".join(c for c in title if c.isalnum() or c in "- _")
                safe_authors = ["".join(c for c in author if c.isalnum() or c in "- _.")  # Added period here
                              for author in authors]
                new_filename = f"{' & '.join(safe_authors)} - {safe_title}.epub"
                new_filepath = os.path.join(folder_path, new_filename)
                
                try:
                    if not os.path.exists(new_filepath):
                        os.rename(epub_path, new_filepath)
                        print(f"Renamed '{filename}' to '{new_filename}'")
                    else:
                        print(f"Skipping '{filename}': Target file already exists")
                except OSError as e:
                    print(f"Error renaming '{filename}': {str(e)}")

if __name__ == "__main__":
    folder_path = '/Users/arek/Documents/_aDoWgrania/_kupione/Humble Tech Book Bundle Full Stack Development with Apress test/'
    print('start')
    rename_epub_files(folder_path)