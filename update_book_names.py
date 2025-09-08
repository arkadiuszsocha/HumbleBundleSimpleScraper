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
                # Switch first and last names for each author
                switched_authors = []
                for author in authors:
                    name_parts = author.split()
                    if len(name_parts) > 1:
                        # Take the last name and put it first
                        switched_name = f"{name_parts[-1]} {' '.join(name_parts[:-1])}"
                    else:
                        switched_name = author
                    safe_author = "".join(c for c in switched_name if c.isalnum() or c in "- _.")
                    switched_authors.append(safe_author)
                
                new_filename = f"{', '.join(switched_authors)} - {safe_title}.epub"
                new_filename_pdf = f"{', '.join(switched_authors)} - {safe_title}.pdf"
                new_filepath = os.path.join(folder_path, new_filename)
                new_filepath_pdf = os.path.join(folder_path, new_filename_pdf)
                
                try:
                    if not os.path.exists(new_filepath):
                        os.rename(epub_path, new_filepath)
                        print(f"Renamed '{filename}' to '{new_filename}'")
                    else:
                        print(f"Skipping '{filename}': Target file already exists")
                        
                    # Check for corresponding PDF file
                    pdf_filename = filename.replace('.epub', '.pdf')
                    pdf_path = os.path.join(folder_path, pdf_filename)
                    if os.path.exists(pdf_path):
                        if not os.path.exists(new_filepath_pdf):
                            os.rename(pdf_path, new_filepath_pdf)
                            print(f"Renamed '{pdf_filename}' to '{new_filename_pdf}'")
                        else:
                            print(f"Skipping '{pdf_filename}': Target file already exists")
                except OSError as e:
                    print(f"Error renaming '{filename}': {str(e)}")
                    

if __name__ == "__main__":
    folder_path = '/Users/arek/Documents/_aDoWgrania/_kupione/Ultimate Programming Languages Bundle by Pact to fix'
    print('start')
    rename_epub_files(folder_path)