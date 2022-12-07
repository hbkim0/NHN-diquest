import typer
import logging

app = typer.Typer(name="registerer", help="Model registerer")

def main():
    logging.basicConfig(
        format = '%(asctime)s:%(name)s:%(levelname)s:%(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        level = logging.DEBUG
    )
    app()
