import requests
from bs4 import BeautifulSoup
import json
import os

# Set to 1 to enable debug mode - saving items to file in debug folder
DEBUG = 1
HUMBLE_FOLDER = "bundles"
DEBUG_FOLDER = "debug"
BUNDLE_TAG = "webpack-bundle-page-data"
BUNDLE_DATA_TAG = "bundleData"
TIER_ITEM_TAG = "tier_item_data"
ITEM_CONTENT_TYPE_TAG = "item_content_type"
TITLE_TAG = "human_name"
AUTHORS_TAG = "developers"
DEVELOPER_NAME_TAG = "developer-name"


def scrape_humble_bundle(bundle_name, output_file="humble_books.txt"):
    if not "-" in bundle_name:
        bundle_name = bundle_name.lower().replace(" ", "-")
    url = f"https://www.humblebundle.com/books/{bundle_name}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to retrieve the page")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("title")
    if title_tag:
        title_text = title_tag.text.strip()

        # Split the title and remove unwanted parts
        # We'll remove "Humble Tech Book Bundle:" and the part after "by"
        clean_title = title_text.split(" (pay")[
            0
        ].strip()  # Take everything before " by"
        clean_title = clean_title.split(": ", 1)[1]
        output_file = f"{clean_title}.txt"
        # Print the clean title
        # print(clean_title)
    else:
        print("No <title> tag found.")
    humble_path = os.path.join(HUMBLE_FOLDER, output_file)
    if not os.path.exists(HUMBLE_FOLDER):
        os.makedirs(HUMBLE_FOLDER)
    debug_path = os.path.join(DEBUG_FOLDER, output_file)
    # output_file = f"/bundles/{output_file}"
    script_tag = soup.find("script", id=BUNDLE_TAG)
    books = []
    if script_tag:
        # Extract the JSON data inside the script tag
        json_data = script_tag.string.strip()

        # Parse the JSON data
        data = json.loads(json_data)
        tier_items = data.get(BUNDLE_DATA_TAG , {})
        items = tier_items.get(TIER_ITEM_TAG, {})
        if DEBUG:
            with open(debug_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(items, indent=4))
        for item_key, item_data in items.items():
            item_content_type = item_data.get(ITEM_CONTENT_TYPE_TAG, "")
            if item_content_type != "ebook":
                continue
            title = item_data.get(TITLE_TAG, "No machine_name")
            authors = item_data.get(AUTHORS_TAG, [])
            # if title == "The Complete Developer":
            #     print(authors)
            book_authors = []
            for author in authors:
                book_authors.append(author.get(DEVELOPER_NAME_TAG, "Unknown"))
            if authors.__len__() == 1:
                books.append(f"{book_authors[0]} - {title}")
            else:
                books.append(f"{', '.join(book_authors)} - {title}")
            # print(title)
        with open(humble_path, "w", encoding="utf-8") as f:
            f.write("\n".join(books))
        # Print or process the data
        print("Bundle saved to", output_file)
    else:
        print(f"No script tag with id {BUNDLE_TAG} found")


# Example usage
scrape_humble_bundle("computer-science-fun-way-no-starch-books")
scrape_humble_bundle("full-stack-development-with-apress-books")
scrape_humble_bundle("ultimate-cybersecurity-career-packt-books")
