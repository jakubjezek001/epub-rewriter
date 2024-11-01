""" Starting point for the application. """
import click


@click.command()
@click.option(
    "--epub-file",
    type=click.Path(exists=True),
    help="The epub file to process.",
)
def cli_main(epub_file: str):
    """Process an epub file."""
    print(f"Processing {epub_file}...")
    print("Hello, world!")
    print("Goodbye, world!")


if __name__ == "__main__":
    cli_main()
