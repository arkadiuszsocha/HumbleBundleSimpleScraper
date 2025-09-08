import os
from ebooklib  import epub

def get_epub_metadata(epub_path):
    try:
        book = epub.read_epub(epub_path)
        title_metadata = book.get_metadata('DC', 'title')
        title = title_metadata[0][0] if title_metadata and title_metadata[0] else 'Unknown Title'
        authors_metadata = book.get_metadata('DC', 'creator')
        # print(f"Extracted authors metadata: {authors_metadata}")
        # Process authors
        authors = []
        for author in authors_metadata:
            author_text = author[0]
            # authors = [author.strip() for author in author_text.split('|')]
            # Split authors by "and" or commas
            if " and " in author_text.lower():
                parts = [p.strip() for p in author_text.split(" and ")]
            elif "," in author_text:
                parts = [p.strip() for p in author_text.split(",")]
            else:
                parts = [author.strip() for author in author_text.split('|')]
            # print(f"Extracted author parts: {parts}")
            # Add each author to the list
            authors.extend(parts)
        # print(f"Extracted title: {title}")
        # print(f"Extracted authors: {authors}")
        return title, authors or ['Unknown Author']
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
                safe_authors = []
                
                # Process each author separately
                for author in authors:
                    name_parts = author.strip().split()
                    if len(name_parts) > 1:
                        last_name = name_parts[-1]
                        first_name = " ".join(name_parts[:-1])
                        formatted_name = f"{last_name} {first_name}"
                    else:
                        formatted_name = author
                    # print(f"Extracted author: {formatted_name}")
                    # Clean the formatted name
                    safe_author = "".join(c for c in formatted_name 
                                        if c.isalnum() or c in "- _." or c.isspace()).strip()
                    safe_authors.append(safe_author)
                
                # Ensure the first author is formatted as "LastName FirstName"
                authors_str = f"{safe_authors[0]}, " + ", ".join(safe_authors[1:]) if len(safe_authors) > 1 else safe_authors[0]
                new_filename = f"{authors_str} - {safe_title}.epub"
                new_filename_pdf = f"{authors_str} - {safe_title}.pdf"
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