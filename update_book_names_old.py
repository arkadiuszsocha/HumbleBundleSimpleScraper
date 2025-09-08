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
                # Clean author names and preserve the original separation
                safe_authors = []
                for author in authors:
                    # First split by comma to get individual authors
                    comma_parts = author.split(',')
                    for i, part in enumerate(comma_parts):
                        # Then split by 'and' if it's the last part
                        if ' and ' in part:
                            and_parts = part.split(' and ')
                            # Process first part of 'and'
                            clean_part = "".join(c for c in and_parts[0] if c.isalnum() or c in "- _." or c.isspace())
                            if clean_part:
                                name_parts = clean_part.strip().split()
                                if len(name_parts) >= 2:
                                    last_name = name_parts[-1]
                                    first_name = " ".join(name_parts[:-1])
                                    safe_authors.append(f"{last_name} {first_name}")
                                else:
                                    safe_authors.append(clean_part.strip())
                            # Process second part of 'and'
                            clean_part = "".join(c for c in and_parts[1] if c.isalnum() or c in "- _." or c.isspace())
                            if clean_part:
                                name_parts = clean_part.strip().split()
                                if len(name_parts) >= 2:
                                    last_name = name_parts[-1]
                                    first_name = " ".join(name_parts[:-1])
                                    safe_authors.append(f"{last_name} {first_name}")
                                else:
                                    safe_authors.append(clean_part.strip())
                        else:
                            # Process regular comma-separated author
                            clean_part = "".join(c for c in part if c.isalnum() or c in "- _." or c.isspace())
                            if clean_part:
                                name_parts = clean_part.strip().split()
                                if len(name_parts) >= 2:
                                    last_name = name_parts[-1]
                                    first_name = " ".join(name_parts[:-1])
                                    safe_authors.append(f"{last_name} {first_name}")
                                else:
                                    safe_authors.append(clean_part.strip())
                
                # Join authors with comma and 'and' for the last one
                if len(safe_authors) > 1:
                    authors_str = ", ".join(safe_authors)
                else:
                    authors_str = safe_authors[0]
                new_filename_base = f"{authors_str} - {safe_title}"
                new_epub_filename = f"{new_filename_base}.epub"
                new_pdf_filename = f"{new_filename_base}.pdf"
                
                # Handle EPUB file
                new_epub_filepath = os.path.join(folder_path, new_epub_filename)
                try:
                    if not os.path.exists(new_epub_filepath):
                        os.rename(epub_path, new_epub_filepath)
                        print(f"Renamed '{filename}' to '{new_epub_filename}'")
                    else:
                        print(f"Skipping '{filename}': Target file already exists")
                except OSError as e:
                    print(f"Error renaming '{filename}': {str(e)}")
                
                # Handle corresponding PDF file if it exists
                pdf_filename = os.path.splitext(filename)[0] + '.pdf'
                pdf_path = os.path.join(folder_path, pdf_filename)
                if os.path.exists(pdf_path):
                    new_pdf_filepath = os.path.join(folder_path, new_pdf_filename)
                    try:
                        if not os.path.exists(new_pdf_filepath):
                            os.rename(pdf_path, new_pdf_filepath)
                            print(f"Renamed '{pdf_filename}' to '{new_pdf_filename}'")
                        else:
                            print(f"Skipping '{pdf_filename}': Target file already exists")
                    except OSError as e:
                        print(f"Error renaming '{pdf_filename}': {str(e)}")

if __name__ == "__main__":
    folder_path = '/Users/arek/Documents/_aDoWgrania/_kupione/Humble Tech Book Bundle Machine Learning, AI, and Bots by OReilly 2025 pop'
    print('start')
    rename_epub_files(folder_path)