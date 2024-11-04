""" Starting point for the application. """
import re
import click
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from collections import defaultdict
import hashlib
from pprint import pprint

from .connection import get_server_response


@click.command()
@click.option(
    "--epub-file",
    type=click.Path(exists=True),
    help="The epub file to process.",
    required=True,
)
def cli_main(epub_file: str):
    """Process an epub file."""
    print(f"Processing {epub_file}...")

    book = epub.read_epub(epub_file, options={"ignore_ncx": True})
    print(f"Title: {book.get_metadata('DC', 'title')[0][0]}")
    print(f"Author: {book.get_metadata('DC', 'creator')[0][0]}")

    items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

    for item in items:
        print(f"Item: {item.get_name()}")
        paragraphs = process_body_paragraphs(item)
        for key, value in paragraphs.items():
            print(value)
            print("_" * 80)
            for par in value:
                # The JSON data payload
                data = {
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are helpful assistant who is able to translate 19 century English text. You are answering briefly and minimal as possible. Every text input is a text sequence which needs to be converted. You are only returning translated text and nothing more. Returned text should be modern English any young people would prefer. Output text should be as minimalistic as possible.",
                        },
                        {"role": "user", "content": par},
                    ],
                    "temperature": 0.7,
                    "max_tokens": -1,
                    "stream": False,
                }
                response = get_server_response(data)
                pprint(response)
                break
            break
        break


def process_body_paragraphs(document):
    soup = BeautifulSoup(document.get_body_content(), "html.parser")
    results = defaultdict(list)
    label_key = None
    for row in soup.select("h4,p"):
        if row.name == "h4":
            # detect if roman numeral pattern in text
            # if they are detected then remove them from head text
            # and use them as hashed key for the paragraph
            if re.match(r"^(I|V|X)+\.", row.text):
                head_text = row.text.split(".")[1].strip()
                label_key = hashlib.shake_128(row.text.encode()).hexdigest(4)

        elif row.name == "p" and label_key:
            results[label_key].append(f"{head_text} {row.text}")
            label_key = None

    return results


if __name__ == "__main__":
    cli_main()
